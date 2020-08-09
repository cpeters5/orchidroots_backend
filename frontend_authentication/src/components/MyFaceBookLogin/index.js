import { connect } from "react-redux";
import { socialLoginFaceBookInit } from "../../Actions/authActions";
import MyFaceBookLogin from "./MyFaceBookLogin";
import { withRouter } from "react-router";

const mapDispatchToProps = {
  socialLoginFaceBookInit,
};

const mapStateToProps = (state) => {
  return {
  };
};

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(MyFaceBookLogin)
);
