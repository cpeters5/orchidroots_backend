import * as types from "../actionTypes/authActionTypes";
import api from "../api/api";
import { logout } from "../constants";

export const loginInit = (
  payload,
  history,
  onLoginFail,
  onLoginSuccess
) => async (dispatch) => {
  dispatch({ type: types.LOGIN_INIT });
  api.auth
    .login(payload)
    .then((value) => {
      dispatch(loginSuccess());
      onLoginSuccess();
      window.location.href = "/";
    })
    .catch((err) => {
      dispatch(loginFailure(err.response.data));
      onLoginFail(err.response.data.error);
      if (err.response.data.error === "Please verify your email.") {
        history.push("/verification");
      }
    });
};

export const loginSuccess = () => ({
  type: types.LOGIN_SUCCESS,
});

export const loginFailure = (error) => ({
  type: types.LOGIN_FAILURE,
  error,
});

export const getCountries = () => async (dispatch) => {
  dispatch({ type: types.GET_COUNTRIES });
  api.auth
    .getCountries()
    .then((value) => {
      dispatch(getCountriesSuccess(value));
    })
    .catch((err) => {
      dispatch(getCountriesSuccess([]));
    });
};

export const getCountriesSuccess = (data) => ({
  type: types.GET_COUNTRIES_SUCCESS,
  countries: data,
});

export const getPhotographers = () => async (dispatch) => {
  dispatch({ type: types.GET_PHOTOGRAPHERS });
  api.auth
    .getPhotographers()
    .then((value) => {
      dispatch(getPhotographersSuccess(value));
    })
    .catch((err) => {
      dispatch(getPhotographersSuccess([]));
    });
};

export const getPhotographersSuccess = (data) => ({
  type: types.GET_PHOTOGRAPHERS_SUCCESS,
  photographers: data,
});

export const logoutInit = (history) => async (dispatch) => {
  dispatch({ type: types.LOGOUT_INIT });
  api.auth
    .logout()
    .then(() => {
      logout();
      dispatch(logoutDone());
      window.location.href = "/";
    })
    .catch((err) => {
      dispatch(logoutDone());
    });
};

export const logoutDone = (error) => ({
  type: types.LOGOUT_DONE,
  error,
});
export const signupInit = (
  payload,
  history,
  onSignupFail,
  onSignupSuccess
) => async (dispatch) => {
  dispatch({ type: types.SIGNUP_INIT });
  api.auth
    .signUp(payload)
    .then((value) => {
      dispatch(signupSuccess(payload.email));
      onSignupSuccess();
      history.push("/verification");
    })
    .catch((err) => {
      dispatch(signupFailure());
      onSignupFail(err.response.data);
    });
};

export const signupSuccess = (email) => ({
  type: types.SIGNUP_SUCCESS,
  email,
});
export const signupFailure = (error) => ({
  type: types.SIGNUP_FAILURE,
  error,
});

export const verificationInit = (
  payload,
  history,
  onVerificationFail,
  onVerificationSuccess
) => async (dispatch) => {
  dispatch({ type: types.VERIFICATION_INIT });
  api.auth
    .verifyCode(payload)
    .then(() => {
      dispatch(verificationSuccess());
      onVerificationSuccess();
      alert("Your account is verified please login.");
      history.push("/login");
    })
    .catch((err) => {
      dispatch(verificationFailure());
      onVerificationFail(err.response.data);
    });
};

export const verificationSuccess = () => ({
  type: types.VERIFICATION_SUCCESS,
});

export const verificationFailure = (error) => ({
  type: types.VERIFICATION_FAILURE,
  error,
});

export const resendVerificationInit = (
  payload,
  onResendVerificationFail,
  onResendVerificationSuccess
) => async (dispatch) => {
  dispatch({ type: types.RESEND_VERIFICATION_INIT });
  api.auth
    .resendVerifyCode(payload)
    .then((res) => {
      dispatch(verificationSuccess());
      onResendVerificationSuccess(res);
    })
    .catch((err) => {
      dispatch(verificationFailure());
      onResendVerificationFail(err.response.data);
    });
};

export const forgetPasswordSendCodeInit = (payload, history) => async (
  dispatch
) => {
  dispatch({ type: types.FORGET_PASSWORD_SEND_CODE_INIT });
  api.auth
    .forgetPasswordSendCode(payload)
    .then(() => {
      dispatch(forgetPasswordSendCodeSuccess(payload.username));
      history.push("/resetpassword");
    })
    .catch((err) => {});
};

export const forgetPasswordSendCodeSuccess = (username) => ({
  type: types.FORGET_PASSWORD_SEND_CODE_SUCCESS,
  username,
});

export const forgetPasswordVerifyCode = (
  payload,
  onForgetPasswordVerifyCodeFail,
  onForgetPasswordVerifyCodeSuccess
) => async (dispatch) => {
  dispatch({ type: types.FORGET_PASSWORD_SEND_CODE_INIT });
  api.auth
    .forgetPasswordVerifyCode(payload)
    .then(() => {
      onForgetPasswordVerifyCodeSuccess();
    })
    .catch((err) => {
      onForgetPasswordVerifyCodeFail(err.response.data);
    });
};
export const resetPassword = (payload, history) => async (dispatch) => {
  dispatch({ type: types.FORGET_PASSWORD_SEND_CODE_INIT });
  api.auth
    .resetPassword(payload)
    .then(() => {
      alert(
        "Password reset Successfully, You can login with your new password now."
      );
      history.push("/login");
    })
    .catch((err) => {});
};

export const socialLoginFaceBookInit = (payload, history) => async (
  dispatch
) => {
  dispatch({ type: types.SOCIAL_LOGIN_FACEBOOK_INIT });
  api.auth
    .socialFaceBookLogin(payload)
    .then((value) => {
      dispatch(loginSuccess());
      window.location.href = "/";
    })
    .catch((err) => {
      dispatch(loginFailure(err.response.data));
    });
};
