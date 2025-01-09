<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card v-if="config">
          <v-card-title> Email Notifications Report </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="config.user_email"
                    label="Email Address"
                    hide-details
                    variant="outlined"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-combobox
                    v-model="config.email_send_in_days"
                    :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
                    label="Day Send"
                    hide-details
                    variant="outlined"
                  ></v-combobox>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="tonal"
              class="mr-2 text-subtitle-1 font-weight-bold"
              @click="save"
              >Save</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <!-- Dialog for adding/editing connection -->
</template>

<script setup lang="ts">
// import ConfigService from "@/services/config";
import { useNotificationStore } from "@/stores/notificationStore";
// import { Config } from "@/types/config";

interface Config {
  user_email: string;
  email_send_in_days: number;
}

const { addNotification } = useNotificationStore();

const config = defineModel<Config>();

const save = async () => {
  try {
    // if (config.value) await ConfigService.update(config.value);
    addNotification("success", "Success", "Save Config Success");
  } catch (error) {
    addNotification("error", "Error", "Save Config Failed");
  }
};
</script>
