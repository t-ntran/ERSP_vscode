#!/usr/bin/env python3
import socket
import sys

s = "hello"
def main():
    if len(sys.argv) != 3:
        print("usage: python3" +
        "client.py <IP> <port")
        #sys.exit(1)
    #ip = sys.agrv[1]
    #port = int(sys.argv[2])
    sock = socket.socket(socket.AF_INET, 
    socket.SOCK_STREAM)
    print("connecting")
    sock.connect(("localhost", 4040))
    print("Welcome!")
    s = "how are you today"

main()
s = "goodbye"