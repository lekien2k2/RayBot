<template>
  <div class="pa-2">
    <h1>Home</h1>
    <p>Home page content</p>
    <p>Status: {{ status }}</p>
    <p>{{ res.qr_location }}</p>
    <v-row>
      <v-col cols="12" md="5"
        ><v-expansion-panels>
          <v-expansion-panel title="INFO" class="ma-1">
            <v-expansion-panel-text>
              <v-card>
                <v-card-text>
                  <v-row>
                    <v-col>
                      <p>Status: {{ res.status }}</p>
                      <p>Ram CPU: {{ res.ram_cpu }}</p>
                      <p>Command: {{ res.command }}</p>
                      <p>Log: {{ res.log }}</p>
                      <p>Weight Sensor: {{ res.weight_sensor }}</p>
                      <p>
                        Forward Distance:
                        {{ res.forward_distance_sensor }}
                      </p>
                      <p>
                        Backward Distance:
                        {{ res.backward_distance_sensor }}
                      </p>
                      <p>Lift Distance: {{ res.lift_distance_sensor }}</p>
                    </v-col>
                    <v-col
                      ><p>Movement Motor: {{ res.movement_motor }}</p>
                      <p>Movement PWM: {{ res.movement_pwm }}</p>
                      <p>Lift Motor: {{ res.lift_motor }}</p>
                      <p>Lift PWM: {{ res.lift_pwm }}</p>
                      <p>QR Door: {{ res.qr_door }}</p>
                      <p>QR Location: {{ res.qr_location }}</p>
                      <p>Battery: {{ res.battery }}</p>
                      <p>Safety: {{ res.safety }}</p>
                      <p>Door State: {{ res.door_state }}</p></v-col
                    >
                  </v-row>
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-expansion-panels>
          <v-expansion-panel title="Control" class="ma-1">
            <v-expansion-panel-text>
              <v-card>
                <v-card-title>Control</v-card-title>
                <v-card-text>
                  <v-btn
                    v-for="(command, index) in ctr_cmds"
                    :key="index"
                    @click="
                      command.id = uuid.v4();
                      send(JSON.stringify(command));
                    "
                    color="warning"
                    class="ma-2"
                  >
                    {{ command.type }}
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels></v-col
      >
      <v-col
        ><v-expansion-panels>
          <v-expansion-panel title="COMMAND" class="ma-1">
            <v-expansion-panel-text>
              <v-card>
                <v-card-text>
                  <v-list>
                    <v-list-item-group>
                      <v-list-item
                        v-for="(command, index) in commands"
                        :key="index"
                      >
                        <v-row>
                          <v-col>
                            <v-list-item-title>
                              {{
                                command.updated_at
                                  ? convertTime(command.updated_at)
                                  : convertTime(command.created_at)
                              }}
                            </v-list-item-title>
                          </v-col>
                          <v-col>
                            <v-list-item-title>
                              {{ command.type }}
                            </v-list-item-title>
                          </v-col>
                          <v-col>
                            <v-list-item-title>
                              {{ command.status }}
                            </v-list-item-title>
                          </v-col>
                        </v-row>
                        <v-divider class="mt-2"></v-divider>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-expansion-panels>
          <v-expansion-panel title="Task" class="ma-1">
            <v-expansion-panel-text>
              <v-card>
                <v-card-title></v-card-title>
                <v-card-text>
                  <p>Status: {{ res.task.status }}</p>
                  <p>Command: {{ res.task.name }}</p>
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-expansion-panels>
          <v-expansion-panel title="Camera" class="ma-1">
            <v-expansion-panel-text>
              <v-card>
                <v-card-title></v-card-title>
                <v-card-text>
                  <!-- <v-img
                    src="http://localhost:80/api/camera/video_feed?mode=camQrLocation"
                  /> -->
                  <v-img
                    src="http://192.168.1.195:8000/api/camera/video_feed?mode=camQrLocation"
                  />
                  <v-img
                    src="http://192.168.1.195:8000/api/camera/video_feed?mode=camQrCheckBox"
                  />
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { useWebSocket } from "@vueuse/core";
import { useNotificationStore } from "@/stores/notificationStore";
import { uuid } from "vue-uuid";
import Commandervice from "@/services/command";
import { convertTime } from "@/utils/time";
export interface DataRecieved {
  topic: string;
  data: string;
  op: string;
}
const res = ref<any>({});

const { addNotification } = useNotificationStore();
const { status, data, send, open, close } = useWebSocket(
  "ws://192.168.1.195:8765",
  // "ws://localhost:8765",
  {
    autoReconnect: true,
    onConnected: () => {
      addNotification("success", "WebSocket connection opened", "WebSocket");
      register_topics();
    },
  }
);

const register_topic = [
  "status",
  "ram_cpu",
  "command",
  "log",
  "battery",
  "weight_sensor",
  "forward_distance_sensor",
  "backward_distance_sensor",
  "lift_distance_sensor",
  "movement_motor",
  "movement_pwm",
  "lift_motor",
  "lift_pwm",
  "safety",
  "qr_location",
  "qr_door",
  "door_state",
  "task",
];

const ctr_cmds = {
  forward: {
    op: "command",
    id: "1",
    type: "move_forward",
    data: {},
  },
  backward: {
    op: "command",
    id: "1",
    type: "move_backward",
    data: {},
  },
  lift: {
    op: "command",
    id: "1",
    type: "lift_box",
    data: {},
  },
  drop: {
    op: "command",
    id: "1",
    type: "drop_box",
    data: {},
  },
  open_box: {
    op: "command",
    id: "1",
    type: "open_box",
    data: {},
  },
  close_box: {
    op: "command",
    id: "1",
    type: "close_box",
    data: {},
  },
  stop: {
    op: "command",
    id: "1",
    type: "stop",
    data: {},
  },
};
const commands = ref<any[]>([]);
const latets_command = ref<any>({});
watch(data, (newData: string) => {
  let respone = JSON.parse(newData);
  // if (
  //   respone.topic === "task" &&
  //   JSON.stringify(respone) !== JSON.stringify(latets_command.value)
  // ) {
  //   latets_command.value = respone;
  //   commands.value.push(respone);
  // }

  if (commands.value.length > 10) {
    commands.value.shift();
  }
  for (let i = 0; i < register_topic.length; i++) {
    if (respone.topic === register_topic[i]) {
      res.value[respone.topic] = respone.data;
    } else if (respone.topic === "status") {
      res.value["status"] = respone.data;
    }
  }
  console.log(res.value);
});
open();
addNotification("info", "WebSocket connection opened", "WebSocket");
function register_topics() {
  for (let i = 0; i < register_topic.length; i++) {
    const command = {
      op: "subscribe",
      id: "1",
      type: "ticker",
      data: {
        topic: register_topic[i],
      },
    };
    send(JSON.stringify(command));
  }
}
setInterval(async () => {
  let command = await Commandervice.get();
  console.log(commands);
  commands.value = command.data;
}, 1000);
</script>
