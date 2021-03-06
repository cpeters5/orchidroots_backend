import Axios from "axios";
import "dotenv/config";
import { BASEURL } from "../constants";

const AxiosInstance = Axios.create({
  baseURL: BASEURL + "/api/",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
    "Accept-Language": "en",
  },
});

AxiosInstance.interceptors.request.use((config) => {
  // after migrate all modules to react we can move back to Auth based on Tokens
  // if (isLoggedIn())
  //   config.headers.Authorization = localStorage.getItem("auth-token") || "";
  return config;
});

AxiosInstance.interceptors.response.use((response) => response.data);

export default AxiosInstance;
