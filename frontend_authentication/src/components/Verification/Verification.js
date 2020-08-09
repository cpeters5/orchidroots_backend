import React, { Component } from "react";
import ReactCodeInput from "react-verification-code-input";
import { Link } from "react-router-dom";
import { errorsToList } from "../../constants";

class Verification extends Component {
  constructor(props) {
    super(props);

    this.state = {
      code: "",
      email: "",
    };
  }

  onCompleteCodeInput = (value) => {
    this.setState({ code: value, isLoading: true });
    this.props.verificationInit(
      { code: value, email: this.props.email },
      this.props.history,
      this.onVerificationFail,
      this.onVerificationSuccess
    );
  };
  onVerificationFail = (errors) => {
    errors = errorsToList(errors);
    this.setState({ errors: errors, isLoading: false });
  };
  onVerificationSuccess = () => {
    this.setState({ isLoading: false });
  };
  onClickResendCode = () => {
    this.props.resendVerificationInit(
      { email: this.props.email },
      this.onResendVerificationFail,
      this.onResendVerificationSuccess
    );
  };
  onResendVerificationFail = (errors) => {
    errors = errorsToList(errors);
    alert("Verification Email Error \n " + errors);
  };
  onResendVerificationSuccess = (response) => {
    alert(errorsToList(response));
  };

  render() {
    return (
      <div className="loginform col-md-6">
        <h3>Email Verification</h3>
        <h5>Please check your email and enter your verification code.</h5>

        <form onSubmit={this.submit}>
          <label htmlFor="exampleInputPassword1">Verification Code</label>
          <div className="form-group ">
            <ReactCodeInput
              onComplete={this.onCompleteCodeInput}
              value={this.state.code}
              disabled={this.state.isLoading}
              fields={5}
            />
          </div>
          <div>
            Didn't recive the code{" "}
            <Link to={this.props.myroute} onClick={this.onClickResendCode}>
              resend
            </Link>
          </div>
          <div className="error text-danger my-1">{this.state.errors}</div>
        </form>
      </div>
    );
  }
}
export default Verification;
