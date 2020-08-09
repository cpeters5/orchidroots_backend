import React, { Component } from "react";
import "./login.css";
import { Link } from "react-router-dom";
import MyFaceBookLogin from "../MyFaceBookLogin";

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      password: "",
      errors: [],
      isLoading: false,
    };
  }
  changeUsername = (event) => {
    this.setState({ username: event.target.value });
  };
  changePassword = (event) => {
    this.setState({ password: event.target.value });
  };
  onLoginFail = (errors) => {
    this.setState({ errors: errors, isLoading: false });
  };
  onLoginSuccess = () => {
    this.setState({ isLoading: false });
  };
  submit = (event) => {
    event.preventDefault();
    this.setState({ isLoading: true });
    let { username, password } = this.state;
    this.props.loginInit(
      { username, password },
      this.props.history,
      this.onLoginFail,
      this.onLoginSuccess
    );
  };
  render() {
    return (
      <div className="loginform col-md-6">
        <h3>Login</h3>

        <form onSubmit={this.submit}>
          <div className="form-group ">
            <label className="col-form-label  requiredField">Username</label>
            <input
              type="text"
              name="username"
              className="form-control"
              onChange={this.changeUsername}
              value={this.state.username}
              placeholder="Enter username"
              disabled={this.state.isLoading}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="exampleInputPassword1">Password</label>
            <input
              name="password"
              type="password"
              onChange={this.changePassword}
              value={this.state.password}
              className="form-control"
              placeholder="Password"
              disabled={this.state.isLoading}
              required
            />
          </div>
          <div className="error text-danger my-1">{this.state.errors}</div>
          {this.state.isLoading ? (
            <button className="btn btn-warning" type="button" disabled>
              <span
                className="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              Loading...
            </button>
          ) : (
            <button type="submit" className="btn btn-warning">
              Submit
            </button>
          )}
          <div className="login_message row d-flex justify-content-between align-items-center">
            <div>
              Don’t have an account ? <Link to="/signup">Sign up</Link>
            </div>
            <div>
              Can't Login? <Link to="/forgetpassword">Forget Password</Link>
            </div>
            <MyFaceBookLogin />
          </div>
        </form>
      </div>
    );
  }
}
export default Login;
