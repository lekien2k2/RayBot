<template>
  <v-container fluid class="h-100">
    <v-tabs v-model="tab" bg-color="">
      <v-tab value="one">System</v-tab>
      <v-tab value="two">Network</v-tab>
      <v-tab value="three">Notify</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="one">
        <v-col class="h-100">
          <v-row class="">
            <v-col cols="12" sm="6" class="h-100">
              <v-row>
                <AccountTab />
              </v-row>
              <v-row class="h-100">
                <FirmwareConfigTab v-model="firmwareConfig" />
              </v-row>
            </v-col>
            <v-col cols="12" sm="6" class="h-100">
              <ConnectTab v-model="config" />
            </v-col>
          </v-row>
          <v-row>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="save"
              class="mr-3 text-subtitle-1 font-weight-bold"
              variant="tonal"
              >Save</v-btn
            >
          </v-row>
        </v-col>
      </v-window-item>

      <v-window-item value="two">
        <NetworkTab />
      </v-window-item>

      <v-window-item value="three">
        <!-- <NotifyTab v-model="config" /> -->
        <h1>NotifyTab</h1>
      </v-window-item>
    </v-window>
  </v-container>
</template>

<script setup lang="ts">
import AccountTab from "./components/AccountTab.vue";
// import ConnectTab from "./components/ConnectTab.vue";
import FirmwareConfigTab from "./components/FirmwareConfigTab.vue";
// import BackupTab from "./components/BackupTab.vue";
// import ConfigService from "@/services/config";
import { onMounted, ref } from "vue";
// import { Config } from "@/types/config";
import { useNotificationStore } from "@/stores/notificationStore";
import NetworkTab from "@/pages/settings/components/NetworkTab.vue";
// import NotifyTab from "@/pages/settings/components/NotifyTab.vue";
import firmwareConfigService from "@/services/firmwareConfig";
interface Config {
  mqtt_host: string;
  mqtt_port: number;
  username: string;
  password: string;
  client_id: string;
}

interface FirmwareConfig {
  min_distance_move: number;
  max_distance_move: number;
  min_distance_lift: number;
  max_distance_lift: number;
  home_location: string;
  max_pwm_movement: number;
  max_pwm_lift: number;
  parameter_motor: number;
}

const firmwareConfig = ref<FirmwareConfig>({
  min_distance_move: 0,
  max_distance_move: 0,
  min_distance_lift: 0,
  max_distance_lift: 0,
  home_location: "",
  max_pwm_movement: 0,
  max_pwm_lift: 0,
  parameter_motor: 0,
});

const { addNotification } = useNotificationStore();
const config = ref<Config>({
  mqtt_host: "",
  mqtt_port: 0,
  username: "",
  password: "",
  client_id: "",
});
const tab = ref<string>("one");

onMounted(async () => {
  firmwareConfig.value = await firmwareConfigService.get();
  // config.value = await ConfigService.get();
  // console.log(config.value);
});

const save = () => {
  // console.log('Save', config.value)
  // if (config.value) ConfigService.update(config.value);
  addNotification("success", "Success", "Save Config Success");
};
</script>

<style scoped></style>
