import React from "react";
import { connect } from "react-redux";
import { logoutInit } from "../../Actions/authActions";
import { Link } from "react-router-dom";
import { isLoggedIn } from "../../constants";

function UserGreeting(props) {
  return (
    <>
      <li className="nav-item">
        <div className="nav-item dropdown">
          <a
            className="nav-link dropdown-toggle"
            href="/"
            id="navbarDropdown"
            role="button"
            data-toggle="dropdown"
          >
            <span style={{ color: "white" }}>{/* {{ user }}&nbsp; */}</span>
          </a>
          <ul className="dropdown-menu">
            {/* {% if user.tier.tier == 5 %} */}
            <li>
              <a className="dropdown-item" href="{% url 'admin:index' %}">
                Admin
              </a>
            </li>
            <li>
              <a
                className="dropdown-item"
                href="https://analytics.google.com/analytics/web/?utm_source=marketingplatform.google.com&utm_medium=et&utm_campaign=marketingplatform.google.com%2Fabout%2Fanalytics%2F#/realtime/rt-location/a128957305w207417477p200133280/&att="
              >
                Google Analytics
              </a>
            </li>
            {/* {% endif %} */}
            <li>
              <a
                className="dropdown-item"
                href="{% url 'update_profile' %}?next=/&att="
              >
                Update profile
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="/logout">
                Logout
              </a>
            </li>
          </ul>
        </div>
      </li>
    </>
  );
}

function GuestGreeting(props) {
  return (
    <>
      <li className="nav-item" style={{ marginTop: 8 }}>
        <Link className="nav-link" to="/signup">
          Register
        </Link>
      </li>
      <li className="nav-item" style={{ marginTop: 8 }}>
        <Link className="nav-link" to="/login">
          Login
        </Link>
      </li>
    </>
  );
}
function Header(props) {
  return (
    <nav className="navbar navbar-expand-md navbar-dark bg-dark">
      <div className="container-fluid">
        <div className="navbar-header">
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#nav-content"
            aria-controls="nav-content"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <a
            className="navbar-brand mb-0 bannerfont"
            href="/"
            style={{ color: "#ffff07", lineHeight: "11px" }}
          >
            <b>
              Orchid
              <br />R<span style={{ fontSize: 18 }}>oots</span>
            </b>
            <span
              style={{ fontSize: 12, color: "darkgrey", fontFamily: "Lucida" }}
            >
              {" "}
              ©2019
            </span>
          </a>
        </div>

        <div className="collapse navbar-collapse" id="nav-content">
          <ul className="navbar-nav">
            {isLoggedIn() ? <UserGreeting {...props} /> : <GuestGreeting />}
          </ul>
        </div>
      </div>
    </nav>
  );
}
const mapStateToProps = (state) => ({});
const mapDispatchToProps = {
  logout: logoutInit,
};
export default connect(mapStateToProps, mapDispatchToProps)(Header);
