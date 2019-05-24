import { clone, findIndex } from "lodash";

import { PanelState } from "./types";
import { AbstractPanel } from "./AbstractPanel";
import { WidgetInstance } from "../WidgetInstance";

import { getNextActiveWidget } from "./common";
import { omitIndex, uuid } from "../../utility";

export interface ExpandoPanelState extends PanelState {
    collapsed: boolean[];
    activeWidget: WidgetInstance | null;
}

export interface ExpandoPanelOpts {
    id?: string;
    title?: string;
    widgets?: WidgetInstance[];
    collapsed?: boolean[];
    activeWidget?: WidgetInstance;
}

export class ExpandoPanel extends AbstractPanel<ExpandoPanelState> {
    constructor(type: "accordion" | "portal", opts: ExpandoPanelOpts = {}) {
        super({
            id: opts.id || uuid(),
            title: opts.title || "",
            type,
            widgets: opts.widgets || [],
            collapsed: calcCollapsed(opts.widgets, opts.collapsed),
            activeWidget: opts.activeWidget || null
        });
    }

    setCollapsed(instanceId: string, value: boolean): void {
        const prev = this.state$.value;
        const { widgets, collapsed } = prev;

        const widgetIdx = findIndex(widgets, (w) => w.id === instanceId);
        const nextCollapsed = clone(collapsed);
        nextCollapsed[widgetIdx] = value;

        this.state$.next({
            ...prev,
            collapsed: nextCollapsed
        });
    }

    closeWidget(instanceId: string): void {
        const prev = this.state$.value;
        const { activeWidget, widgets, collapsed } = prev;

        const widgetIdx = findIndex(widgets, (w) => w.id === instanceId);
        const nextWidgets = omitIndex(widgets, widgetIdx);
        const nextCollapsed = omitIndex(collapsed, widgetIdx);
        const nextActive = getNextActiveWidget(activeWidget, instanceId, nextWidgets);

        this.state$.next({
            ...prev,
            widgets: nextWidgets,
            collapsed: nextCollapsed,
            activeWidget: nextActive
        });
    }
}

function calcCollapsed(widgets: WidgetInstance[] = [], collapsed: boolean[] = []) {
    if (collapsed.length === 0 || widgets.length !== collapsed.length) {
        return Array(widgets.length).fill(false);
    }
    return collapsed;
}
