<template>
  <v-card>
    <v-card-title>
      <h1>Camera</h1>
    </v-card-title>
    <v-row>
      <v-col>
        <v-card class="ma-1">
          <v-card-title class="text-center">RayCamera</v-card-title>
          <v-card-text class="mx-4">
            <v-img
              src="http://192.168.1.232:8000/api/camera/video_feed?mode=camQrLocation"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="ma-1">
        <v-card>
          <v-card-title class="text-center">BoxCamera</v-card-title>
          <v-card-text class="mx-4">
            <v-img
              src="http://192.168.1.232:8000/api/camera/video_feed?mode=camQrCheckBox"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
const tab = ref(0);
</script>

<style scoped></style>
