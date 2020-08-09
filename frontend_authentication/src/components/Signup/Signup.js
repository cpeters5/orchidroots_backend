import React, { Component } from "react";
import "./signup.css";
import { errorsToList } from "../../constants";
import { Link } from "react-router-dom";
import MyFaceBookLogin from "../MyFaceBookLogin";

class Signup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      errors: [],
      isLoading: false,
      username: "",
      password: "",
      confirm_password: "",
      fullname: "",
      email: "",
      profile: {
        photo_credit_name: "",
        specialty: "",
        current_credit_name_id: "",
        country: "",
      },
    };
  }

  onSignupFail = (errors) => {
    let error_list = errorsToList(errors);
    this.setState({ errors: error_list, isLoading: false });
  };
  onSignupSuccess = () => {
    this.setState({ isLoading: false });
  };
  componentDidMount() {
    if (this.props.countries.length === 0) this.props.getCountries();
    if (this.props.photographers.length === 0) this.props.getPhotographers();
  }
  onChangeControlText = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };
  onChangeProfileControlText = (event) => {
    event.persist();
    this.setState((prevState) => {
      return {
        ...prevState,
        profile: {
          ...prevState.profile,
          [event.target.name]: event.target.value,
        },
      };
    });
  };
  submit = (event) => {
    event.preventDefault();
    this.props.signupInit(
      this.state,
      this.props.history,
      this.onSignupFail,
      this.onSignupSuccess
    );
  };
  render() {
    return (
      <div className="signupform col-md-6">
        <h3>signup</h3>

        <form onSubmit={this.submit}>
          <div className="form-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="validationCustomUsername">Username</label>
              <div className="input-group">
                <div className="input-group-prepend">
                  <span className="input-group-text" id="inputGroupPrepend">
                    @
                  </span>
                </div>
                <input
                  type="text"
                  name="username"
                  className="form-control"
                  id="validationCustomUsername"
                  placeholder="Username"
                  aria-describedby="inputGroupPrepend"
                  onChange={this.onChangeControlText}
                  value={this.state.username}
                  disabled={this.state.isLoading}
                  required
                />
                <div className="invalid-feedback">
                  Please choose a username.
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-3">
              <label htmlFor="password">Password</label>
              <input
                name="password"
                type="password"
                onChange={this.onChangeControlText}
                value={this.state.password}
                className="form-control"
                placeholder="Password"
                disabled={this.state.isLoading}
                required
              />
            </div>
            <div className="col-md-3 mb-3">
              <label htmlFor="confirm_password">Confirm Password</label>
              <input
                name="confirm_password"
                type="password"
                onChange={this.onChangeControlText}
                value={this.state.confirm_password}
                className="form-control"
                placeholder="Confirm Password"
                disabled={this.state.isLoading}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="fullname">Full name</label>
              <input
                name="fullname"
                type="text"
                onChange={this.onChangeControlText}
                value={this.state.fullname}
                className="form-control"
                placeholder="Full name"
                disabled={this.state.isLoading}
                required
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="email">Email</label>
              <input
                name="email"
                type="text"
                onChange={this.onChangeControlText}
                value={this.state.email}
                className="form-control"
                placeholder="Email"
                disabled={this.state.isLoading}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="col-md-12 mb-3">
              <label htmlFor="photo_credit_name">
                The name you prefer to use for credit attribution
              </label>
              <input
                name="photo_credit_name"
                type="text"
                onChange={this.onChangeProfileControlText}
                value={this.state.profile.photo_credit_name}
                className="form-control"
                placeholder="Photo Credit Name"
                disabled={this.state.isLoading}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="col-md-12 mb-3">
              <label htmlFor="current_credit_name_id">
                The name currently used for credit attribution in OrchidRoots.
                Leave blank if you do not see your name iin the list. WARNING:
                your account will be removed if you selected name that is not
                yours.
              </label>
              <select
                className=" form-control"
                name="current_credit_name_id"
                onChange={this.onChangeProfileControlText}
                value={this.state.profile.current_credit_name_id}
              >
                <option value="-1" selected>
                  --- Select your credit attribution ---
                </option>
                {this.props.photographers.map((photographer) => {
                  return (
                    <option value={photographer.author_id}>
                      {photographer.displayname}
                    </option>
                  );
                })}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="col-md-12 mb-3">
              <label htmlFor="specialty">
                Orchid related Interest. List genera or alliances of your
                interest
              </label>
              <input
                name="specialty"
                type="text"
                onChange={this.onChangeProfileControlText}
                value={this.state.profile.specialty}
                className="form-control"
                placeholder="Specialty"
                disabled={this.state.isLoading}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="col-md-12 mb-3">
              <label htmlFor="country">Select a country:</label>
              <select
                className=" form-control"
                name="country"
                onChange={this.onChangeProfileControlText}
                value={this.state.profile.country}
              >
                <option value="-1" selected>
                  --- Select Country ---
                </option>
                {this.props.countries.map((country) => {
                  return <option value={country.pk}>{country.country}</option>;
                })}
              </select>
            </div>
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
              Have an account? <Link to="/login">Login</Link>
            </div>
              <MyFaceBookLogin/>
          </div>
        </form>
      </div>
    );
  }
}
export default Signup;
