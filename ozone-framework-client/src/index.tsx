import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css";
import "react-mosaic-component/react-mosaic-component.css";

import "./index.scss";

import "reflect-metadata";

import * as React from "react";
import * as ReactDOM from "react-dom";

import { configure as configureMobX } from "mobx";

import initializeIocContainerBindings from "./inject-bindings";
import registerServiceWorker from "./registerServiceWorker";

import App from "./App";

configureMobX({
    enforceActions: false
});

initializeIocContainerBindings();

ReactDOM.render(
  <App />,
  document.getElementById("root") as HTMLElement
);

registerServiceWorker();