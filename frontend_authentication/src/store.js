import { createStore, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";
import { routerMiddleware } from "connected-react-router";
import { createBrowserHistory } from "history";
import createRootReducer from "./reducers";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // defaults to localStorage for web

export default (url = "/") => {
  // Create a history depending on the environment
  const history = createBrowserHistory();
  const middlewares = [routerMiddleware(history), thunk];

  const persistConfig = {
    key: "root",
    storage,
    whitelist: ["authReducer"],
  };

  const persistedReducer = persistReducer(
    persistConfig,
    createRootReducer(history)
  );

  const composedEnhancers = compose(applyMiddleware(...middlewares));

  const store = createStore(
    persistedReducer,
    window.__PRELOADED_STATE__,
    composedEnhancers
  );
  let persistor = persistStore(store);
  return {
    store,
    persistor,
    history,
  };
};
