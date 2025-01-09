<template>
  <v-card class="h-100" v-if="firmwareConfig">
    <v-card-title>Server Connection</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.min_distance_move"
            label="Min Distance Move"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('min_distance_move', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.max_distance_move"
            label="Max Distance Move"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('max_distance_move', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.min_distance_lift"
            label="Min Distance Lift"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('min_distance_lift', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.max_distance_lift"
            label="Max Distance Lift"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('max_distance_lift', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.home_location"
            label="Home Location"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('home_location', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.max_pwm_movement"
            :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword ? 'text' : 'password'"
            @click:append-inner="showPassword = !showPassword"
            label="Max PWM Movement"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('max_pwm_movement', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.max_pwm_lift"
            label="Max PWM Lift"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('max_pwm_lift', $event.target.value)"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="firmwareConfig.parameter_motor"
            label="Parameter Motor"
            variant="outlined"
            dense
            hide-details
            @change="updateFirmware('parameter_motor', $event.target.value)"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
// import { Config } from "@/types/config";
import { ref } from "vue";
import firmwareConfigService from "@/services/firmwareConfig";
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

const firmwareConfig = defineModel<FirmwareConfig>();

const showPassword = ref(false);

function updateFirmware(key: string, value: any) {
  console.log(key, value);
  const data = {
    [key]: value,
  };
  firmwareConfigService.update(data);
}
</script>

<style scoped></style>
