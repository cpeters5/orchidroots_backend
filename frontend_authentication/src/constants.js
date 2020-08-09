export const BASEURL = "http://127.0.0.1:8000";

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

export const isLoggedIn = () => {
  return getCookie("is_loggedin") == 'true'
};
export const logout = () => {
  localStorage.removeItem("auth-token");
};

export const errorsToList = function __errorsToList(errors) {
  let error_list = [];
  for (const key in errors) {
    const errs = errors[key];
    if (typeof errs === "string")
      errors.error
        ? error_list.push(errors.error)
        : error_list.push(errors.detail);
    else if (Array.isArray(errs)) error_list.push(...errs);
    else {
      error_list.push(__errorsToList(errs));
    }
    return error_list;
  }
};
