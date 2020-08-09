import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import Login from "./components/Login";
import ForgetPassword from "./components/ForgetPassword";
import Signup from "./components/Signup";
import Verification from "./components/Verification";
import { isLoggedIn } from "./constants";
import ResetPassword from "./components/ResetPassword";
import Header from "./components/Header/Header";

export default (props) => (
  <Router>
    <>
      <Header />
      {!isLoggedIn() ? (
        <>
          <Route exact path="/login">
            <Login />
          </Route>
          <Route exact path="/forgetpassword">
            <ForgetPassword />
          </Route>
          <Route exact path="/resetpassword">
            <ResetPassword />
          </Route>
          <Route exact path="/signup">
            <Signup />
          </Route>
          <Route exact path="/verification">
            <Verification />
          </Route>
        </>
      ) : (
        (window.location.href = "/")
      )}
    </>
  </Router>
);
