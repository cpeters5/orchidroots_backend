import { connect } from "react-redux";
import {
  verificationInit,
  resendVerificationInit,
} from "../../Actions/authActions";
import Verification from "./Verification";
import { withRouter } from "react-router";

const mapDispatchToProps = {
  verificationInit,
  resendVerificationInit,
};

const mapStateToProps = (state) => {
  return {
    email: state.authReducer.signUpEmail,
  };
};

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(Verification)
);
