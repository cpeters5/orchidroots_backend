import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import Router from "./Router.js";
import Header from "./components/Header/Header";
import * as serviceWorker from "./serviceWorker";
import createStore from "./store";
import { Provider } from "react-redux";

import { ConnectedRouter } from "connected-react-router";

const { store, history } = createStore();
ReactDOM.render(
  <Provider store={store}>
    <ConnectedRouter history={history}>
      <Router />
    </ConnectedRouter>
  </Provider>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
