import { connect } from "react-redux";
import { forgetPasswordSendCodeInit } from "../../Actions/authActions";
import ForgetPassword from "./ForgetPassword";
import { withRouter } from "react-router";

const mapDispatchToProps = {
  forgetPasswordSendCodeInit,
};

const mapStateToProps = (state) => {
  return {
    errors: state.authReducer.forgetpasswordErrors,
  };
};

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(ForgetPassword)
);
