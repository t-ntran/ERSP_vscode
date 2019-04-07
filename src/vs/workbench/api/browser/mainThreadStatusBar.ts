/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { IStatusbarService, StatusbarAlignment as MainThreadStatusBarAlignment, IStatusbarEntryAccessor } from 'vs/platform/statusbar/common/statusbar';
import { MainThreadStatusBarShape, MainContext, IExtHostContext } from '../common/extHost.protocol';
import { ThemeColor } from 'vs/platform/theme/common/themeService';
import { extHostNamedCustomer } from 'vs/workbench/api/common/extHostCustomers';
import { ExtensionIdentifier } from 'vs/platform/extensions/common/extensions';

@extHostNamedCustomer(MainContext.MainThreadStatusBar)
export class MainThreadStatusBar implements MainThreadStatusBarShape {

	private readonly entries: Map<number, IStatusbarEntryAccessor> = new Map();

	constructor(
		_extHostContext: IExtHostContext,
		@IStatusbarService private readonly statusbarService: IStatusbarService
	) { }

	dispose(): void {
		this.entries.forEach(entry => entry.dispose());
		this.entries.clear();
	}

	$setEntry(id: number, extensionId: ExtensionIdentifier, text: string, tooltip: string, command: string, color: string | ThemeColor, alignment: MainThreadStatusBarAlignment, priority: number): void {
		const props = { text, tooltip, command, color, extensionId };

		let entry = this.entries.get(id);
		if (!entry) {
			entry = this.statusbarService.addEntry(props, alignment, priority);
			this.entries.set(id, entry);
		} else {
			entry.update(props);
		}
	}

	$dispose(id: number) {
		const entry = this.entries.get(id);
		if (entry) {
			entry.dispose();
		}

		this.entries.delete(id);
	}
}
