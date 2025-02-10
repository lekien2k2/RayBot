<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-data-table :headers="headers" :items="network" item-key="id">
          <template v-slot:top>
            <v-toolbar flat density="compact">
              <v-toolbar-title class="font-weight-bold text-h5"
                >Interfaces</v-toolbar-title
              >
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="tonal"
                dark
                class="text-capitalize"
                @click="addConnectionDialog = true"
              >
                Add Wifi
              </v-btn>
            </v-toolbar>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-icon small @click="editConnection(item)"> mdi-pencil </v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
  <!-- Dialog for adding/editing connection -->
  <v-dialog v-model="editConnectionDialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h5 font-weight-bold">Config Interface</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="editedConnection.interface"
                label="Interface"
                hide-details
                variant="outlined"
                disabled
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="editedConnection.ip_mode"
                :items="['dhcp', 'static']"
                hide-details
                variant="outlined"
                label="IP Mode"
              ></v-select>
            </v-col>
            <v-col cols="12" v-if="editedConnection.ip_mode === 'static'">
              <v-text-field
                v-model="editedConnection.ip"
                hide-details
                variant="outlined"
                label="IP Address"
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="editedConnection.netmask"
                label="Subnet Mask"
                hide-details
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="editedConnection.gateway"
                label="Gateway"
                hide-details
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="editedConnection.dns"
                label="DNS Servers"
                hide-details
                variant="outlined"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="darken-1" variant="tonal" @click="closeConnectionDialog">
          Cancel
        </v-btn>
        <v-btn color="primary" variant="tonal" @click="saveConnection">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Dialog for add new wifi -->
  <v-dialog v-model="addConnectionDialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h5 font-weight-bold">Add Wifi</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="newWifi.ssid"
                label="SSID"
                hide-details
                variant="outlined"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="newWifi.password"
                label="Password"
                hide-details
                variant="outlined"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color=" darken-1" variant="tonal" @click="closeConnectionDialog">
          Cancel
        </v-btn>
        <v-btn color="primary" variant="tonal" @click="addWifi"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
// import { Network, NetworkUpdate } from "@/types/network";
// import SystemService from "@/services/system";
import { useNotificationStore } from "@/stores/notificationStore";
const SystemService = {
  getNetworkInterfaces: async () => {
    return [
      {
        interface: "eth0",
        type: "Ethernet",
        ip: "aaaaaaaa",
        gateway: "bbbbbbbb",
        ip_mode: "dhcp",
      },
    ];
  },
  setNetworkInterfaces: async (data: any) => {
    console.log(data);
  },
  createWifi: async (data: any) => {
    console.log(data);
  },
};

interface Network {
  interface: string;
  type: string;
  ip: string;
  gateway: string;
  ip_mode: string;
}

interface NetworkUpdate {
  interface: string;
  ip_mode: string;
  ip: string;
  netmask: string;
  gateway: string;
  dns: string;
}
const { addNotification } = useNotificationStore();

onMounted(async () => {
  // Fetch connections from API
  // network.value = await SystemService.getNetworkInterfaces();
  console.log(network.value);
});
const headers = [
  { title: "Interface", value: "interface" },
  { title: "Type", value: "type" },
  { title: "IP Address", value: "ip" },
  { title: "Gateway", value: "gateway" },

  { title: "IP Mode", value: "ip_mode" },
  { title: "Actions", value: "actions", sortable: false },
];

interface Wifi {
  ssid: string;
  password: string;
}

const newWifi = ref<Wifi>({ ssid: "", password: "" });
const network = ref<Network[]>([]);

const editConnectionDialog = ref(false);
const addConnectionDialog = ref(false);
const editedConnection = ref<NetworkUpdate>({} as NetworkUpdate);

const editConnection = (connection: any) => {
  editedConnection.value = { ...connection };
  editConnectionDialog.value = true;
};

const closeConnectionDialog = () => {
  editConnectionDialog.value = false;
  addConnectionDialog.value = false;
};

const saveConnection = async () => {
  console.log(editedConnection.value);
  closeConnectionDialog();
  await SystemService.setNetworkInterfaces(editedConnection.value);
  network.value = await SystemService.getNetworkInterfaces();
  addNotification(
    "success",
    "Success",
    "Network interface updated successfully"
  );
};

const addWifi = async () => {
  console.log(newWifi.value);
  closeConnectionDialog();
  await SystemService.createWifi(newWifi.value);
  network.value = await SystemService.getNetworkInterfaces();
  addNotification("success", "Success", "Wifi added successfully");
};
</script>
