import React, { useCallback } from "react";
import { Button } from "@blueprintjs/core";

import { Shortcuts, useHotkey } from "../../../shared/hotkeys";

import { mainStore } from "../../../stores/MainStore";
import { NavbarTooltip } from "./NavbarTooltip";

const _StoreButton: React.FC = () => {
    const toggleStore = () => {
        mainStore.toggleStore();
    };

    useHotkey({ combo: Shortcuts.showStore, onKeyDown: toggleStore });

    return (
        <NavbarTooltip title="AppsMall Center" shortcut={Shortcuts.showStore} description="Open AppsMall">
            <Button minimal icon="shopping-cart" onClick={toggleStore} data-element-id="store-button" />
        </NavbarTooltip>
    );
};

export const StoreButton = React.memo(_StoreButton);
