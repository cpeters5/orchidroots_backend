import { connect } from "react-redux";
import {
  getCountries,
  getPhotographers,
  signupInit,
} from "../../Actions/authActions";
import Signup from "./Signup";
import { withRouter } from "react-router";

const mapDispatchToProps = {
  getCountries,
  getPhotographers,
  signupInit,
};

const mapStateToProps = (state) => ({
  errors: state.authReducer.signupErrors,
  countries: state.authReducer.countries,
  photographers: state.authReducer.photographers,
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Signup));
