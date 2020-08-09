import React, { Component } from "react";
import "./forgetpassword.css";
import { Link } from "react-router-dom";

class ForgetPassword extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      errors: [],
      isLoading: false,
    };
  }
  changeUsername = (event) => {
    this.setState({ username: event.target.value });
  };
  submit = (event) => {
    event.preventDefault();
    this.setState({ isLoading: true });
    let { username } = this.state;
    this.props.forgetPasswordSendCodeInit({ username }, this.props.history);
  };
  render() {
    return (
      <div className="forgetpasswordform col-md-6">
        <h3>ForgetPassword</h3>

        <form onSubmit={this.submit}>
          <div className="form-group ">
            <label className="col-form-label  requiredField">
              Enter usernem or email
            </label>
            <input
              type="text"
              name="username"
              className="form-control"
              onChange={this.changeUsername}
              value={this.state.username}
              placeholder="username or email"
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
          <div className="forgetpassword_message row d-flex justify-content-between align-items-center">
            <div>
              Have an account ? <Link to="/login">Login</Link>
            </div>
            <div>
              Don't have an account? <Link to="/signup">Sign up</Link>
            </div>
            <div className="">
              <br></br>
              <br></br>
            </div>
          </div>
        </form>
      </div>
    );
  }
}
export default ForgetPassword;
