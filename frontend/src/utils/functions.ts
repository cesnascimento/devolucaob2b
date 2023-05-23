import { notification } from "antd";
import { USERTOKEN } from "../layout/MainLayout";
import Axios from "axios";

export const redirectToLogin = (history: any) => {
  history.push("/login");
};

export const logout = (history: any) => {
  localStorage.removeItem(USERTOKEN);
  redirectToLogin(history);
};

export const errorHandler = (e: any) => {
  if (!e.response) {
    return "Network error, Please check your network and try again";
  }
  let errorMessage = "";
  Object.values(e.response.data).map((item: any) => {
    errorMessage += item;
    return null;
  });
  return errorMessage;
};

export enum NotificationTypes {
  SUCCESS = "success",
  INFO = "info",
  ERROR = "error",
  WARNING = "warning",
}

export const openNotificationWithIcon = (
  type: NotificationTypes,
  title: string,
  description?: string
) => {
  notification[type]({
    message: title,
    description: description,
  });
};