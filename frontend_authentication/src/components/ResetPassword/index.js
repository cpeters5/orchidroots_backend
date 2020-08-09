import { connect } from "react-redux";
import {
  forgetPasswordVerifyCode,
  forgetPasswordSendCodeInit,
  resetPassword,
} from "../../Actions/authActions";
import ResetPassword from "./ResetPassword";
import { withRouter } from "react-router";

const mapDispatchToProps = {
  forgetPasswordSendCodeInit,
  forgetPasswordVerifyCode,
  resetPassword,
};

const mapStateToProps = (state) => {
  return {
    username: state.authReducer.resetPasswordUsername,
  };
};

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(ResetPassword)
);
