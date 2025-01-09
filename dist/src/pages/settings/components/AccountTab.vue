<template>
  <v-container fluid class="h-100">
    <v-card class="h-100">
      <v-row class="h-50">
        <v-col
          class="align-center justify-center"
          v-if="activeBreakpoint !== 'mobile' && activeBreakpoint !== 'tablet'"
        >
          <v-icon icon="mdi-account" :size="160"></v-icon>
        </v-col>
        <v-col>
          <v-card-title>
            <v-icon
              icon="mdi-account"
              v-if="activeBreakpoint === 'mobile'"
            ></v-icon
            >Account</v-card-title
          >
          <v-card-subtitle>Manage your account settings</v-card-subtitle>
          <v-card-text>
            <v-btn
              class="text-capitalize"
              color="success"
              prepend-icon="mdi-pencil"
              @click="isChangePassword = true"
              >Change Password</v-btn
            >
          </v-card-text>
        </v-col>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>
  </v-container>
  <v-dialog v-model="isChangePassword" width="500">
    <v-card>
      <v-card-title>Change Password</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="password"
          label="Old Password"
          type="password"
          variant="outlined"
          :rules="[rules.required, rules.min]"
        ></v-text-field>
        <v-text-field
          v-model="newPassword"
          label="New Password"
          type="password"
          variant="outlined"
          :rules="[rules.required, rules.min]"
        ></v-text-field>
        <v-text-field
          v-model="confirmPassword"
          label="Confirm Password"
          type="password"
          variant="outlined"
          :rules="[rules.required, rules.min, rules.isSame]"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="darken-1"
          variant="tonal"
          @click="isChangePassword = !isChangePassword"
          >Cancel</v-btn
        >
        <v-btn
          color="success"
          variant="tonal"
          class="mr-5"
          :disabled="!isConfirmPassword"
          @click="changePassword()"
          >Change Password</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
// import AuthService from "@/services/auth";
import { computed } from "vue";
import { ref } from "vue";
import { useNotificationStore } from "@/stores/notificationStore";
import { useBreakpoints } from "@vueuse/core";

const breakpoints = useBreakpoints({
  mobile: 0, // optional
  tablet: 480,
  laptop: 1024,
  desktop: 1280,
});

// Can be 'mobile' or 'tablet' or 'laptop' or 'desktop'
const activeBreakpoint = breakpoints.active();
const { addNotification } = useNotificationStore();
const isChangePassword = ref(false);

const password = ref("");
const newPassword = ref("");
const confirmPassword = ref("");

const rules = {
  required: (value: string) => !!value || "Required.",
  min: (v: string) => (v && v.length >= 4) || "Min 4 characters",
  isSame: (v: string) => v === newPassword.value || "Password does not match",
};

const isConfirmPassword = computed(
  () =>
    confirmPassword.value === newPassword.value &&
    confirmPassword.value.length >= 4 &&
    password.value.length >= 4
);

const changePassword = async () => {
  //   console.log(
  //     "Change Password",
  //     password.value,
  //     newPassword.value,
  //     confirmPassword.value
  //   );
  // const res = await AuthService.changePassword(
  //   password.value,
  //   newPassword.value
  // );
  // console.log(res);

  addNotification("success", "Success", "Password changed successfully");
  isChangePassword.value = false;
};
</script>

<style lang="scss" scoped></style>
