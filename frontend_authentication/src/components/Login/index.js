import { connect } from "react-redux";
import { loginInit, socialLoginFaceBookInit } from "../../Actions/authActions";
import Login from "./Login";
import { withRouter } from "react-router";

const mapDispatchToProps = {
  loginInit,
  socialLoginFaceBookInit,
};

const mapStateToProps = (state) => {
  return {
    errors: state.authReducer.loginErrors,
  };
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Login));
