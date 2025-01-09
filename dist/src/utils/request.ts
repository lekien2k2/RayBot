import axios from "axios";
import { useNotificationStore } from "@/stores/notificationStore";
export const apiClient = axios.create({
  baseURL: `${import.meta.env.VITE_BASE_API || ""}/api`,
});

apiClient.interceptors.request.use(
  (config) => {
    // do something before request is sent
    const accessToken = localStorage.getItem("accessToken");

    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    // do something with request error
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  async (response) => {
    // do something with response data
    // await new Promise((r) => setTimeout(r, 500));
    return response.data;
  },
  (error) => {
    // do something with response error

    const { addNotification } = useNotificationStore();
    addNotification(
      "error",
      error.message,
      error.response?.data.message ||
        error.response?.data.detail ||
        "Something went wrong"
    );
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("accessToken");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export const apiDownloadClient = axios.create({
  baseURL: `${import.meta.env.VITE_BASE_API || ""}/api`,
});

apiDownloadClient.interceptors.request.use(
  (config) => {
    // do something before request is sent
    const accessToken = localStorage.getItem("accessToken");

    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    // do something with request error
    return Promise.reject(error);
  }
);

apiDownloadClient.interceptors.response.use(
  async (response) => {
    // do something with response data
    // await new Promise((r) => setTimeout(r, 500));
    return response;
  },
  (error) => {
    // do something with response error

    const { addNotification } = useNotificationStore();
    addNotification(
      "error",
      error.message,
      error.response?.data.message ||
        error.response?.data.detail ||
        "Something went wrong"
    );
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("accessToken");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);
