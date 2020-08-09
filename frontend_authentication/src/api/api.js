import Axios from "./Axios";

export default {
  auth: {
    login: (loginData) => Axios.post("v1/accounts/login/", loginData),
    logout: () => Axios.post("v1/accounts/logout/"),
    signUp: (signUpData) => Axios.post("v1/accounts/signup/", signUpData),
    verifyCode: (verificationData) =>
      Axios.post("v1/accounts/verify-code/", verificationData),
    resendVerifyCode: (resendVerificationData) =>
      Axios.post("v1/accounts/resend-verify-code/", resendVerificationData),
    getCountries: () => Axios.get("v1/accounts/countries/"),
    getPhotographers: () => Axios.get("v1/accounts/photographers/"),
    forgetPasswordSendCode: (forgetPasswordSendCodeData) =>
      Axios.post(
        "v1/accounts/forget-password-send-code/",
        forgetPasswordSendCodeData
      ),
    forgetPasswordVerifyCode: (forgetPasswordVerifyCodeData) =>
      Axios.post(
        "v1/accounts/forget-password-verify-code/",
        forgetPasswordVerifyCodeData
      ),
    resetPassword: (resetPasswordData) =>
      Axios.post("v1/accounts/reset-password/", resetPasswordData),
    socialFaceBookLogin: (socialFaceBookLoginData) =>
      Axios.post("v1/accounts/social-login/", socialFaceBookLoginData),
  },
};
