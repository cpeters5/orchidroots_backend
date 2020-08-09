import React, { Component } from "react";
import FacebookLogin from "react-facebook-login";

class MyFaceBookLogin extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }
  responseFacebook = (response) => {
    let payload = {
      social_type: "facebook",
      social_token: response.accessToken,
      social_id: response.id,
    };
    this.props.socialLoginFaceBookInit(payload, this.props.history);
  };
  render() {
    return (
      <FacebookLogin
        appId="2574533656097865"
        autoLoad={false}
        callback={this.responseFacebook}
      />
    );
  }
}
export default MyFaceBookLogin;
