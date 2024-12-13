<template>
  <v-layout>
    <v-app-bar color="" :elevation="1">
      <v-toolbar color="">
        <template v-slot:prepend>
          <a class="d-flex flex-row align-center"
            ><v-img :width="44" :src="TBELogo"></v-img>
            <a v-if="width > 960" class="text-h6 text-grey-darken-3 ml-2">
              {{ appTitle }}
            </a>
          </a>
          <v-btn
            v-if="width <= 960"
            @click="drawer = !drawer"
            class="ma-2"
            icon="mdi-menu"
            variant="text"
          ></v-btn>
        </template>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>mdi-bell-outline</v-icon>
        </v-btn>
        <v-card-item
          ><v-menu open-on-hover class="mr-2">
            <template v-slot:activator="{ props }">
              <v-icon v-bind="props">mdi-account-circle-outline</v-icon>
            </template>
            <v-list>
              <v-list-item
                v-for="item in ['Logout']"
                :key="item"
                @click="console.log(item)"
              >
                <v-list-item-title>{{ item }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></v-card-item
        >
      </v-toolbar>
    </v-app-bar>
    <v-navigation-drawer
      app
      v-model="drawer"
      location="left"
      :permanent="width > 960"
    >
      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in routeViewList"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.to"
          color="primary"
          router
        ></v-list-item>
      </v-list>
      <template v-slot:append>
        <v-divider> </v-divider>
        <div class="d-flex flex-row justify-end align-center py-4 px-4">
          <v-icon size="x-small" icon="mdi-tag-outline"></v-icon>
          <span class="ml-1 text-caption">{{ appVersion }}</span>
        </div>
      </template>
    </v-navigation-drawer>
    <v-main>
      <Notification></Notification>
      <router-view></router-view>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useWindowSize } from "@vueuse/core";
import TBELogo from "@/assets/images/logo.png";
import { routeViewList } from "@/layouts/navigationRoutes";
// import BreadCrumb from "@/components/BreadCrumb.vue";
// import AuthService from "@/services/auth";
const { width } = useWindowSize();
const drawer = ref(true);
const appTitle = import.meta.env.VITE_APP_TITLE;
const appVersion = import.meta.env.VITE_APP_VERSION;

watch([width], () => {
  if (width.value > 960) {
    drawer.value = true;
  } else {
    drawer.value = false;
  }
});
</script>

<style scoped></style>
