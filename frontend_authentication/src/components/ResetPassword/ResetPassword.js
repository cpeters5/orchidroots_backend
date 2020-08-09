import React, { Component } from "react";
import ReactCodeInput from "react-verification-code-input";
import { Link } from "react-router-dom";
import { errorsToList } from "../../constants";

class ResetPassword extends Component {
  constructor(props) {
    super(props);
    this.state = {
      code: "",
      new_password: "",
      show_new_password: false,
    };
  }

  onCompleteCodeInput = (value) => {
    this.setState({ code: value, isLoading: true });
    this.props.forgetPasswordVerifyCode(
      { code: value, username: this.props.username },
      this.forgetPasswordVerifyCodeFail,
      this.forgetPasswordVerifyCodeSuccess
    );
  };
  forgetPasswordVerifyCodeFail = (errors) => {
    errors = errorsToList(errors);
    this.setState({ errors: errors, isLoading: false });
  };
  forgetPasswordVerifyCodeSuccess = () => {
    this.setState({ show_new_password: true, isLoading: false });
  };
  onClickResendCode = () => {
    this.props.forgetPasswordSendCodeInit(
      { username: this.props.username },
      this.onResendResetPasswordFail,
      this.onResendResetPasswordSuccess
    );
  };
  onResendResetPasswordFail = (errors) => {
    errors = errorsToList(errors);
    alert("ResetPassword Email Error \n " + errors);
  };
  onResendResetPasswordSuccess = (response) => {
    alert(errorsToList(response));
  };

  changePassword = (event) => {
    this.setState({ new_password: event.target.value });
  };
  submit = (event) => {
    event.preventDefault();
    this.setState({ isLoading: true });
    this.props.resetPassword(
      {
        code: this.state.code,
        new_password: this.state.new_password,
        username: this.props.username,
      },
      this.props.history
    );
  };

  render() {
    return (
      <div className="loginform col-md-6">
        {!this.state.show_new_password && (
          <>
            <h3>Reset Code Sent Successfully!</h3>
            <h5>
              Please check your email inbox releated with this account '
              {this.props.username}' and enter your reset password code.
            </h5>
          </>
        )}
        {this.state.show_new_password && (
          <>
            <h3>Correct Code!</h3>
            <h5>
              Please set a new password for your accout '{this.props.username}'.
            </h5>
          </>
        )}
        <form onSubmit={this.submit}>
          {!this.state.show_new_password && (
            <div className="form-group ">
              <label htmlFor="exampleInputPassword1">Reset Password Code</label>
              <ReactCodeInput
                onComplete={this.onCompleteCodeInput}
                value={this.state.code}
                disabled={this.state.isLoading}
                fields={5}
              />
            </div>
          )}
          <br />
          {this.state.show_new_password && (
            <div className="form-group">
              <label htmlFor="exampleInputPassword1">New Password</label>
              <input
                name="password"
                type="password"
                onChange={this.changePassword}
                value={this.state.new_password}
                className="form-control"
                placeholder="New Password"
                disabled={this.state.isLoading}
                required
              />
            </div>
          )}
          {!this.state.show_new_password && (
            <div className="forgetpassword_message row d-flex justify-content-between align-items-center">
              <div>
                Didn't recive the code{" "}
                <Link to={this.props.myroute} onClick={this.onClickResendCode}>
                  resend
                </Link>
              </div>
              <div>
                Try another username or email ?{" "}
                <Link to="/forgetpassword">Change</Link>
              </div>
              <div></div>
            </div>
          )}
          {this.state.show_new_password &&
            (this.state.isLoading ? (
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
            ))}

          <div className="error text-danger my-1">{this.state.errors}</div>
        </form>
      </div>
    );
  }
}
export default ResetPassword;
