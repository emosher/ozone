import { dropRight, isString, omit, pick, set } from "lodash";

import { BehaviorSubject } from "rxjs";
import { asBehavior } from "../observables";

import { MosaicDirection, MosaicNode, MosaicParent, MosaicPath } from "../features/MosaicDashboard/types";

import { MosaicDropTargetPosition } from "../features/MosaicDashboard/internalTypes";

import {
    Corner,
    getAndAssertNodeAtPathExists,
    getNodeAtPath,
    getOtherDirection,
    getPathToCorner
} from "../features/MosaicDashboard/util/mosaicUtilities";

import { createRemoveUpdate, updateTree } from "../features/MosaicDashboard/util/mosaicUpdates";


import { UserWidget } from "./UserWidget";

import { DashboardNode, DashboardPath } from "../components/widget-dashboard/types";
import { ProfileReference } from "../api/models/UserDTO";

import { ExpandoPanel, FitPanel, LayoutType, Panel, PanelState, TabbedPanel } from "./panel";
import { WidgetInstance } from "./WidgetInstance";

export interface DashboardLayout {
    tree: DashboardNode | null;
    panels: Dictionary<Panel<any>>;
}

export interface DashboardProps extends DashboardLayout {
    description?: string;
    guid: string;
    imageUrl?: string;
    isAlteredByAdmin: boolean;
    isDefault: boolean;
    isGroupDashboard: boolean;
    isLocked: boolean;
    isMarkedForDeletion: boolean;
    isPublishedToStore: boolean;
    metadata?: {
        createdBy: ProfileReference;
        createdDate: string;
        editedDate: string;
    };
    name: string;
    position: number;
    stackId: number;
    user: {
        username: string;
    };
}

export interface AddWidgetOpts {
    userWidget: UserWidget;
    title?: string;
    path?: MosaicPath;
    position?: MosaicDropTargetPosition;
}

export class Dashboard {
    private readonly state$: BehaviorSubject<DashboardProps>;

    constructor(props: PropertiesOf<DashboardProps>) {
        this.state$ = new BehaviorSubject(props);
    }

    get guid() {
        return this.state$.value.guid;
    }

    state = () => asBehavior(this.state$);

    /**
     * Find a Widget instance in any of the Dashboard Panels
     */
    findWidget(instanceId: string): WidgetInstance | undefined {
        const { panels } = this.state$.value;

        for (const panelId in panels) {
            if (panels.hasOwnProperty(panelId)) {
                const panel: Panel<any> = panels[panelId];
                const widget = panel.findWidget(instanceId);
                if (widget !== undefined) {
                    return widget;
                }
            }
        }

        return undefined;
    }

    addWidget(opts: AddWidgetOpts): boolean {
        const { userWidget, title, path, position } = opts;

        const prev = this.state$.value;
        const { panels, tree } = prev;

        const instance = WidgetInstance.create(userWidget);
        const panel = new FitPanel({ title, widget: instance });

        let newTree: DashboardNode;
        if (tree === null) {
            newTree = panel.id;
        } else if (path !== undefined && position !== undefined) {
            newTree = addToLayout(tree, panel.id, path, position);
        } else {
            newTree = addToTopRightOfLayout(tree, panel.id);
        }

        this.state$.next({
            ...prev,
            tree: newTree,
            panels: {
                ...panels,
                [panel.id]: panel
            }
        });

        return true;
    }

    addPanel(panel: Panel<PanelState>) {
        const prev = this.state$.value;
        const { panels, tree } = prev;

        const newTree = tree !== null ? addToTopRightOfLayout(tree, panel.id) : panel.id;

        this.state$.next({
            ...prev,
            tree: newTree,
            panels: {
                ...panels,
                [panel.id]: panel
            }
        });
    }

    /**
     * Set the new dashboard layout and check for changes to open/closed panels.
     */
    setLayout(tree: DashboardNode | null): void {
        const state = this.state$;
        const prev = state.value;

        const panelIds = findPanelIds(tree);
        const newPanels = pick(prev.panels, panelIds);

        state.next({
            ...prev,
            tree,
            panels: newPanels
        });
    }

    getPanelByPath(path: MosaicPath): Panel | null {
        const { tree, panels } = this.state$.value;
        if (tree === null) return null;

        const node = getNodeAtPath(tree, path);
        if (node === null) return null;

        if (typeof node !== "string") return null;

        const panel = panels[node];
        if (!panel) return null;

        return panel;
    }

    getPanelById(panelId: string): Panel | null {
        const { panels } = this.state$.value;

        const panel = panels[panelId];
        if (!panel) return null;

        return panel;
    }

    removeNode(path: MosaicPath): void {
        const { tree } = this.state$.value;
        if (tree === null) return;

        const removeUpdate = createRemoveUpdate(tree, path);
        const newTree = updateTree(tree, [ removeUpdate ]);

        this.setLayout(newTree);
    }


    /**
     * Set the new dashboard layout without checking for changes to the panels.
     */
    setLayoutFast(tree: DashboardNode | null): void {
        const state = this.state$;
        state.next({
            ...state.value,
            tree
        });
    }

    setPanelLayout(panel: Panel<PanelState>, path: DashboardPath, layout: LayoutType) {
        const prev = this.state$.value;
        const { tree, panels } = prev;

        if (!tree) throw new Error("setPanelLayout: no current Dashboard tree");

        const { widgets } = panel.state().value;
        let newPanel: Panel<PanelState> | undefined;
        if (layout === "fit") {
            const widget = widgets.length > 0 ? widgets[0] : undefined;
            newPanel = new FitPanel({ widget });
        } else if (layout === "tabbed") {
            newPanel = new TabbedPanel({ widgets });
        } else if (layout === "accordion") {
            newPanel = new ExpandoPanel("accordion", { widgets });
        } else if (layout === "portal") {
            newPanel = new ExpandoPanel("portal", { widgets });
        }

        if (newPanel !== undefined) {
            const newTree = updateTree(tree, [ { path, spec: { $set: newPanel.id } } ]);
            const newPanels = set(omit(panels, panel.id), newPanel.id, newPanel);

            this.state$.next({
                ...prev,
                tree: newTree,
                panels: newPanels
            });
        }
    }
}

function findPanelIds(node: DashboardNode | null): string[] {
    if (node === null) return [];
    if (isString(node)) return [ node ];
    return [ ...findPanelIds(node.first), ...findPanelIds(node.second) ];
}

function addToLayout(
    layout: DashboardNode,
    id: string,
    targetPath: MosaicPath,
    position: MosaicDropTargetPosition
): DashboardNode {
    const targetNode = getAndAssertNodeAtPathExists(layout, targetPath);

    const newNode = id;

    let first: DashboardNode;
    let second: DashboardNode;

    if (position === MosaicDropTargetPosition.LEFT || position === MosaicDropTargetPosition.TOP) {
        first = newNode;
        second = targetNode;
    } else {
        first = targetNode;
        second = newNode;
    }

    let direction: MosaicDirection = "column";
    if (position === MosaicDropTargetPosition.LEFT || position === MosaicDropTargetPosition.RIGHT) {
        direction = "row";
    }

    const update = {
        path: targetPath,
        spec: {
            $set: { first, second, direction }
        }
    };

    return updateTree(layout, [ update ]);
}

function addToTopRightOfLayout(layout: DashboardNode, id: string): DashboardNode {
    const path = getPathToCorner(layout, Corner.TOP_RIGHT);
    const parent = getNodeAtPath(layout, dropRight(path)) as MosaicParent<string>;
    const destination = getNodeAtPath(layout, path) as MosaicNode<string>;
    const direction: MosaicDirection = parent ? getOtherDirection(parent.direction) : "row";
    let first: MosaicNode<string>;
    let second: MosaicNode<string>;
    if (direction === "row") {
        first = destination;
        second = id;
    } else {
        first = id;
        second = destination;
    }

    const update = {
        path,
        spec: {
            $set: {
                direction,
                first,
                second
            }
        }
    };

    return updateTree(layout, [ update ]);
}

export const EMPTY_DASHBOARD = new Dashboard({
    guid: "",
    isAlteredByAdmin: false,
    isDefault: true,
    isGroupDashboard: false,
    isLocked: false,
    isMarkedForDeletion: false,
    isPublishedToStore: false,
    name: "",
    panels: {},
    position: 0,
    stackId: 0,
    tree: null,
    user: {
        username: ""
    }
});
