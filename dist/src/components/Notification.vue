<template>
  <div class="notificationContainer">
    <v-slide-y-transition group>
      <v-alert
        v-for="[id, notification] of notifications"
        :key="id"
        :text="notification.message"
        :title="notification.title"
        :type="notification.type"
      ></v-alert>
    </v-slide-y-transition>
  </div>
</template>
<script setup lang="ts">
import { useNotificationStore } from "@/stores/notificationStore";

const { notifications } = useNotificationStore();
</script>
<style scoped>
.notificationContainer {
  position: fixed;
  top: 10px;
  right: 10px;
  display: grid;
  grid-gap: 0.5em;
  z-index: 9999;
}
</style>
