import { defineStore } from "pinia";

interface Notification {
  type: "success" | "info" | "warning" | "error";
  title: string;
  message: string;
  timeout: number;
}

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    notifications: new Map<string, Notification>(),
  }),
  actions: {
    addNotification(
      type: "success" | "info" | "warning" | "error",
      title: string,
      message: string,
      timeout = 5000
    ) {
      const id = Math.random().toString(36).substr(2, 9);
      this.notifications.set(id, { type, title, message, timeout });
      setTimeout(() => {
        this.removeNotification(id);
      }, timeout);
    },
    removeNotification(id: string) {
      this.notifications.delete(id);
    },
  },
});
