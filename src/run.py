import ast
import bdb
from copy import deepcopy
import ctypes
import json
import sys
import traceback
import types
import re

from core import *

# Execution limit to prevent infinite loops
MAX_TIME = 1000

# This is a terrible, horrible, no good, very bad hack
current_test = None
current_exp = None


# from PIL import Image

def add_html_escape(html):
	return f"```html\n{html}\n```"

def add_red_format(html):
	return f"<div style='color:red;'><small><small>{html}</small></small></div>"

def is_loop_str(str):
	return re.search("(for|while).*:\w*\n", str) != None

def is_break_str(str):
	return re.search("break", str.strip()) != None

def is_return_str(str):
	return re.search("return", str.strip()) != None

def indent(str):
	return len(str) - len(str.lstrip())

def remove_R(lineno):
	if isinstance(lineno, str):
		return int(lineno[1:])
	else:
		return lineno

class LoopInfo:
	def __init__(self, frame, lineno, indent):
		self.frame = frame
		self.lineno = lineno
		self.indent = indent
		self.iter = 0

	def __str__(self):
		return f'iter {self.iter}, frame {self.frame} at line {self.lineno} with indent {self.indent}'


class Logger(bdb.Bdb):
	def __init__(self, lines, writes, values = []):
		bdb.Bdb.__init__(self)
		self.lines = lines
		self.writes = writes
		self.time = 0
		self.prev_env = None
		self.data = {}
		self.active_loops = []
		self.preexisting_locals = None
		self.exception = None
		self.matplotlib_state_change = False

		# Optional dict from (lineno, time) to a dict of varname: value
		self.values = values

	def data_at(self, l):
		if l not in self.data:
			self.data[l] = []
		return self.data[l]
	def user_call(self, frame, args):
		if not ("__name__" in frame.f_globals):
			return
		if frame.f_globals["__name__"] == "matplotlib.pyplot":
			self.matplotlib_state_change = True

	def user_line(self, frame):
		# print("user_line ============================================")
		# print(frame.f_code.co_name)
		# print(frame.f_code.co_names)
		# print(frame.f_code.co_filename)
		# print(frame.f_code.co_firstlineno)
		# print(dir(frame.f_code))
		# print("lineno")
		# print(frame.f_lineno)
		# print(frame.__dir__())
		# print("globals")
		# print(frame.f_globals)
		# print("locals")
		# print(frame.f_locals)

		if frame.f_code.co_name == "<module>" and self.preexisting_locals == None:
			self.preexisting_locals = set(frame.f_locals.keys())

		if frame.f_code.co_name == "<listcomp>":
			return
		if frame.f_code.co_name == "<dictcomp>":
			return
		if frame.f_code.co_name == "<lambda>":
			return
		if not ("__name__" in frame.f_globals):
			return
		if frame.f_globals["__name__"] != "__main__":
			return

		self.exception = None
		adjusted_lineno = frame.f_lineno-1
		self.record_loop_end(frame, adjusted_lineno)
		self.record_env(frame, adjusted_lineno)
		self.record_loop_begin(frame, adjusted_lineno)

	def record_loop_end(self, frame, lineno):
		curr_stmt = self.lines[lineno]
		if self.prev_env != None and len(self.active_loops) > 0 and self.active_loops[-1].frame is frame:
			prev_lineno = remove_R(self.prev_env["lineno"])
			prev_stmt = self.lines[prev_lineno]

			loop_indent = self.active_loops[-1].indent
			curr_indent = indent(curr_stmt)
			curr_frame_name = frame.f_code.co_name
			prev_frame_name = self.prev_env["frame"].f_code.co_name
			if is_return_str(prev_stmt) and curr_frame_name == prev_frame_name:
				# we shouldn't record the end of a loop after
				# a call to another function with a return statement,
				# so we need to check whether prev stmt comes from the same frame
				# as the current one
				while len(self.active_loops) > 0:
					self.active_loops[-1].iter += 1
					for l in self.stmts_in_loop(self.active_loops[-1].lineno):
						self.data_at(l).append(self.create_end_loop_dummy_env())
					del self.active_loops[-1]
			elif (curr_indent <= loop_indent and lineno != self.active_loops[-1].lineno):
				# break statements don't go through the loop header, so we miss
				# the last increment in iter, which is why we have to adjust here
				if is_break_str(prev_stmt):
					self.active_loops[-1].iter += 1
				for l in self.stmts_in_loop(self.active_loops[-1].lineno):
					self.data_at(l).append(self.create_end_loop_dummy_env())
				del self.active_loops[-1]

	def record_loop_begin(self, frame, lineno):
		# for l in self.active_loops:
		#	 print("Active loop at line " + str(l.lineno) + ", iter " + str(l.iter))
		curr_stmt = self.lines[lineno]
		if is_loop_str(curr_stmt):
			if len(self.active_loops) > 0 and self.active_loops[-1].lineno == lineno:
				self.active_loops[-1].iter += 1
			else:
				self.active_loops.append(LoopInfo(frame, lineno, indent(curr_stmt)))
				for l in self.stmts_in_loop(lineno):
					self.data_at(l).append(self.create_begin_loop_dummy_env())

	def stmts_in_loop(self, lineno):
		result = []
		curr_stmt = self.lines[lineno]
		loop_indent = indent(curr_stmt)
		for l in range(lineno+1, len(self.lines)):
			line = self.lines[l]
			if line.strip() == "":
				continue
			if indent(line) <= loop_indent:
				break
			result.append(l)
		return result

	def active_loops_iter_str(self):
		return ",".join([str(l.iter) for l in self.active_loops])

	def active_loops_id_str(self):
		return ",".join([str(l.lineno) for l in self.active_loops])

	def add_loop_info(self, env):
		env["#"] = self.active_loops_iter_str()
		env["$"] = self.active_loops_id_str()

	def create_begin_loop_dummy_env(self):
		env = {"begin_loop":self.active_loops_iter_str()}
		self.add_loop_info(env)
		return env

	def create_end_loop_dummy_env(self):
		env = {"end_loop":self.active_loops_iter_str()}
		self.add_loop_info(env)
		return env

	def compute_repr(self, v):
		if isinstance(v, types.FunctionType):
			return None
		if isinstance(v, types.ModuleType):
			return None
		html = if_img_convert_to_html(v)
		if html == None:
			return repr(v)
		else:
			return add_html_escape(html)

	def record_env(self, frame, lineno):
		line_time = "(%s,%d)" % (lineno, self.time)
		print("Recording env for line " + str(lineno) + " at time " + str(self.time))

		vars = []
		adjusted_lineno = 0
		if str(lineno).find('R') != -1:
			adjusted_lineno = remove_R(lineno)
		else:
			adjusted_lineno = lineno -1
		print("adjusted_lineno = " + str(adjusted_lineno))
		if adjusted_lineno >= 0:
			print("Line: " + self.lines[adjusted_lineno])
			if (str(self.lines[adjusted_lineno].strip()).find("for") != -1
				or str(self.lines[adjusted_lineno].strip()).find("while") != -1):
				try:
					code = "".join(self.lines)
					tree = ast.parse(code)
					for node in ast.walk(tree):
						if isinstance(node, (ast.For, ast.While)):
							vars.append(node.target.id)
							for b in node.body:
								if isinstance(b, ast.AugAssign):
									vars.append(b.target.id)
									break
					#print("Vars: " + str(vars))
				except SyntaxError as e:
					print("Error: " + str(e))
					#return e.msg
			else:
				try:
					tree = ast.parse(self.lines[adjusted_lineno].strip())
					#print(ast.dump(tree))
					vars = sorted({node.id for node in ast.walk(tree) if isinstance(node, ast.Name)})
					#print("Vars: " + str(vars))
				except SyntaxError as e:
					print("Error: " + str(e))
					#return e.msg
		print ("Vars: " + str(vars))


		if line_time in self.values:
			# Replace the current values with the given ones first
			print('%s:' % line_time)
			env = self.values[line_time]
			print(frame.f_locals)

			for varname in frame.f_locals:
				if varname in env:
					new_value = eval(env[varname])
					print("\t'%s': '%s' -> '%s'" % (varname, repr(frame.f_locals[varname]), repr(new_value)))
					frame.f_locals.update({ varname: new_value })
					ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))

		if self.time >= MAX_TIME:
			self.set_quit()
			return
		env = {}
		env["frame"] = frame
		env["time"] = self.time
		self.add_loop_info(env)

		self.time = self.time + 1
		for k in frame.f_locals:
			#print("\t'%s': '%s'" % (k, repr(frame.f_locals[k])))
			if k != magic_var_name and (frame.f_code.co_name != "<module>" or not k in self.preexisting_locals):
					r = self.compute_repr(frame.f_locals[k])
					print("\t'%s': '%s'" % (k, r))
					if (r != None):
						#if k in vars or vars is []:
							env[k] = r
		env["lineno"] = lineno
		env["func_lineno"] = str(frame.f_code.co_firstlineno)

		if self.matplotlib_state_change:
			env["Plot"] = add_html_escape(matplotlib_fig_as_html())
			self.matplotlib_state_change = False

			if self.prev_env != None:
				prev_lineno = remove_R(self.prev_env["lineno"])
				if not (prev_lineno in self.writes):
					self.writes[prev_lineno] = []
				self.writes[prev_lineno].append("Plot")

		self.data_at(lineno).append(env)

		if (self.prev_env != None):
			self.prev_env["next_lineno"] = lineno
			env["prev_lineno"] = self.prev_env["lineno"]

		self.prev_env = env

	def user_exception(self, frame, e):
		self.exception = e[1]

	def user_return(self, frame, rv):
		# print("user_return ============================================")
		# print(frame.f_code.co_name)
		# print("lineno")
		# print(frame.f_lineno)
		# print(frame.__dir__())
		# print("globals")
		# print(frame.f_globals)
		# print("locals")
		# print(frame.f_locals)

		if frame.f_code.co_name == "<listcomp>":
			return
		if frame.f_code.co_name == "<dictcomp>":
			return
		if frame.f_code.co_name == "<lambda>":
			return

		if not ("__name__" in frame.f_globals):
			return
		if frame.f_globals["__name__"] != "__main__":
			return

		adjusted_lineno = frame.f_lineno-1

		self.record_env(frame, "R" + str(adjusted_lineno))
		if self.exception == None:
			r = self.compute_repr(rv)
			rv_name = "rv"
		else:
			r = format_exception(self.exception)
			rv_name = "Exception Thrown"
		if r != None:
			if frame.f_code.co_name != "<module>" or self.exception != None:
				self.data_at("R" + str(adjusted_lineno))[-1][rv_name] = r
			if self.exception != None and self.lines[adjusted_lineno].lstrip().startswith("return"):
				# No good, very bad hack
				# Only show test and expected value if an exception occurs and we are already on a return line,
				# since we have room for the test and exp columns in that case
				self.data_at("R" + str(adjusted_lineno))[-1]["test"] = current_test
				self.data_at("R" + str(adjusted_lineno))[-1]["exp"] = current_exp
		self.record_loop_end(frame, adjusted_lineno)

	def pretty_print_data(self):
		for k in self.data:
			print("** Line " + str(k))
			for env in self.data[k]:
				print(env)


def format_exception(exception):
	# Show full exception traceback (useful for debugging)
	# return repr(exception) + "\n" + "".join(traceback.format_tb(exception.__traceback__))
	html = add_red_format(exception.__class__.__name__ + ": " + str(exception))
	return add_html_escape(html)


class WriteCollector(ast.NodeVisitor):
	def __init__(self):
		ast.NodeVisitor()
		self.data = {}

	def data_at(self, l):
		if not(l in self.data):
			self.data[l] = []
		return self.data[l]

	def record_write(self, lineno, id):
		if (id != magic_var_name):
			self.data_at(lineno-1).append(id)

	def visit_Name(self, node):
		#print("Name " + node.id + " @ line " + str(node.lineno) + " col " + str(node.col_offset))
		if isinstance(node.ctx, ast.Store):
			self.record_write(node.lineno, node.id)

	def visit_Subscript(self, node):
		#print("Subscript " + str(node.ctx) + " " + str(node.value) + " " + str(node.col_offset))
		if isinstance(node.ctx, ast.Store):
			id = self.find_id(node)
			if id == None:
				print("Warning: did not find id in subscript")
			else:
				self.record_write(node.lineno, id)

	def find_id(self, node):
		if hasattr(node, "id"):
			return node.id
		if hasattr(node, "value"):
			return self.find_id(node.value)
		return None

def compute_writes(lines):
	exception = None
	try:
		done = False
		while not done:
			try:
				code = "".join(lines)
				root = ast.parse(code)
				done = True
			except Exception as e:
				lineno = e.lineno-1
				did_lines_change = False
				while lineno >= 0:
					if lines[lineno].find(magic_var_name) != -1:
						# (lisa) able to remove boxes at comment lines inside a function body,
						# but not top level -- needs to handle the latter in RTVDisplay
						lines[lineno] = "\n"
						did_lines_change = True
					lineno = lineno - 1
				if not did_lines_change:
					raise
	except Exception as e:
		exception = e

	writes = {}
	if exception == None:
		#print(ast.dump(root))
		write_collector = WriteCollector()
		write_collector.visit(root)
		writes = write_collector.data
	return (writes, exception)


def parse_test_line(line):
	try:
		tree = ast.parse(line)
	except SyntaxError as e:
		return e.msg
	if not isinstance(tree, ast.Module):
		return "Internal error: expected ast.Module"
	if len(tree.body) != 1:
		return "Test line may only contain a single statement"
	expr = tree.body[0]
	if not isinstance(expr, ast.Expr):
		return "Internal error: expected ast.Expr"

	if isinstance(expr.value, ast.Compare):
		compare = expr.value
		if len(compare.ops) == 1 and isinstance(compare.ops[0], ast.Eq):
			if isinstance(compare.left, ast.Call):
				actual = ast.Expression(compare.left)
				expected = ast.Expression(compare.comparators[0])
				return [actual, expected]
			else:
				return "Left-hand side of == must be a function call"
		else:
			return "Tests may only use a single == comparison"
	elif isinstance(expr.value, ast.Call):
		actual = ast.Expression(expr.value)
		return [actual, None]
	else:
		return "Test line must be a function call or == comparison"


class TestLine:
	def __init__(self, text, lineno):
		self.text = text
		self.lineno = lineno
		parsed = parse_test_line(text)
		if isinstance(parsed, str):
			error_msg = parsed + f" (line {self.lineno}): " + text
			raise SyntaxError(error_msg)
		self.actual, self.expected = parsed


def compute_runtime_data(lines, writes, values, test_comments):
	global current_test
	global current_exp

	exception = None
	if len(lines) == 0:
		return ({}, exception)
	code = "".join(lines)
	l = Logger(lines, writes, values)
	try:
		l.run(code)
	except Exception as e:
		exception = e

	#print(l.data)
	#filtering variable for each line
	"""
	for line_num in range(len(l.lines)):
		keywords = set(['frame', 'time', '#', '$', 'lineno', 'func_lineno', 'next_lineno', 'prev_lineno','Exception Thrown'])
		for num in l.data:
			if 'begin_loop' in l.data[num][0] or 'end_loop' in l.data[num][0]:
				continue
			for var in l.data[num][0]:
				if l.data[num][0]['lineno'] == line_num + 1:
					if l.lines[line_num].find(str(var)) != -1:
						keywords.add(var)
				elif l.data[num][0]['lineno'] == 'R' + str(line_num):
					if l.lines[line_num].find(str(var)) != -1:
						keywords.add(var)
				else:
					continue

			if l.data[num][0]['lineno'] == line_num + 1:
				for keys in l.data[num][0].copy():
					if keys not in keywords:
						del l.data[num][0][str(keys)]
				break
			elif l.data[num][0]['lineno'] == 'R' + str(line_num):
				for keys in l.data[num][0].copy():
					if keys not in keywords:
						del l.data[num][0][str(keys)]
			else:
				continue
	"""


	# Only show runtime data from test cases, not top-level executions
	if len(test_comments) > 0:
		l.data = {}

	# TODO handle exceptions properly
	tests = []
	for test_string, test_lineno in test_comments:
		try:
			tests.append(TestLine(test_string, test_lineno))
		except Exception as e:
			print(e)

	test_results=[]
	for test in tests:
		expected_value = 'No_expected_value_given_needs_to_be_added_later'
		test_src = ast.unparse(test.actual)
		if test.expected is not None:
			try:
				expected_value = repr(l.runeval(compile(test.expected, "", "eval")))
			except Exception as e:
				pass

		current_test = test_src
		current_exp = expected_value

		try:
			actual_value = l.runeval(compile(test.actual, "", "eval"))
			test_time = l.time - 1
			print(f"test time: {test_time}, test: {test.text}")
			test_results.append((test_time, expected_value, test_src))
		except Exception as e:
			test_time = l.time - 1
			func_lineno = None
			for env in get_envs_by_time(l.data, test_time):
				func_lineno = int(env["func_lineno"])
			if func_lineno is not None:
				l.data_at(func_lineno - 1).append({
					"time": test_time + 1,
					"#": "",
					"$": "",
					"show_exception_at_top": None,
					"test": test_src,
					"exp": expected_value,
					"Exception Thrown": format_exception(e),
				})
				l.time += 1

	l.data = adjust_to_next_time_step(l.data, l.lines)
	remove_frame_data(l.data)
	return (l.data, exception, test_results)

def adjust_to_next_time_step(data, lines):
	envs_by_time = {}
	for lineno in data:
		for env in data[lineno]:
			if "time" in env:
				envs_by_time[env["time"]] = env
	new_data = {}
	for lineno in data:
		next_envs = []
		for env in data[lineno]:
			if "begin_loop" in env:
				next_envs.append(env)
			elif "end_loop" in env:
				next_envs.append(env)
			elif "show_exception_at_top" in env:
				del env["show_exception_at_top"]
				next_envs.append(env)
			elif "time" in env:
				next_time = env["time"]+1
				while next_time in envs_by_time:
					next_env = envs_by_time[next_time]
					if "frame" in env and "frame" in next_env and env["frame"] is next_env["frame"]:
						curr_stmt = lines[env["lineno"]]
						next_stmt = lines[remove_R(next_env["lineno"])]
						if "Exception Thrown" in next_env or not is_loop_str(curr_stmt) or indent(next_stmt) > indent(curr_stmt):
							next_envs.append(next_env)
						break
					next_time = next_time + 1
				# next_time = env["time"]+1
				# if next_time in envs_by_time:
				# 	next_envs.append(envs_by_time[next_time])
		new_data[lineno] = next_envs
	return new_data

def remove_frame_data(data):
	for lineno in data:
		for env in data[lineno]:
			if "frame" in env:
				del env["frame"]

def main(file, values_file = None):
	test_comments = get_test_comment_lines(file)

	lines = load_code_lines(file)
	values = []

	if values_file:
		values = json.load(open(values_file))

	return_code = 0
	run_time_data = {}
	test_results = {}

	(writes, exception) = compute_writes(lines)

	if exception != None:
		return_code = 1
	else:
		(run_time_data, exception, test_results) = compute_runtime_data(lines, writes, values, test_comments)
		if (exception != None):
			return_code = 2

	for test_result in test_results:
		for env in get_envs_by_time(run_time_data, test_result[0]):
			env["exp"] = test_result[1]
			env["test"] = test_result[2]

	with open(file + ".out", "w") as out:
		out.write(json.dumps((return_code, writes, run_time_data)))
		print(f"wrote {file}.out")

	if exception != None:
		raise exception


def get_envs_by_time(data, time):
	matches = []
	for envs in data.values():
		for env in envs:
			if "time" in env and env["time"] == time:
				matches.append(env)
	return matches


if __name__ == '__main__':
	if len(sys.argv) > 2:
		main(sys.argv[1], sys.argv[2])
	else:
		main(sys.argv[1])
