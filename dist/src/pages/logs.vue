<template>
  <v-container fluid>
    <!-- <h2 class="mb-3 text-grey-darken-3"></h2> -->

    <v-data-table-virtual
      class="rounded-lg elevation-1"
      style="height: 80vh; overflow-y: auto"
      :headers="headers"
      :items="logList"
      :loading="loading"
      fixed-header
    >
      <template #item.time="{ item }">
        {{ convertTime(item.time) }}
      </template>
    </v-data-table-virtual>
    <v-pagination
      :length="totalPage"
      v-model="page"
      :total-visible="7"
      @update:model-value="findLogs()"
    ></v-pagination>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { LogType } from "@/types/logs";
import LogService from "@/services/logs";
import { convertTime } from "@/utils/time";

const logList = ref<LogType[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const totalPage = ref(0);
const page = ref(1);

onMounted(async () => {
  loading.value = true;
  try {
    const res = await LogService.get();
    logList.value = res.data;
    totalPage.value = res.meta_data.total_pages;
    page.value = res.meta_data.page;
  } catch (err: any) {
    error.value = err.toString();
  } finally {
    loading.value = false;
  }
});

const headers = [
  {
    title: "ID",
    value: "id",
  },
  {
    title: "Username",
    value: "username",
  },
  {
    title: "Time",
    value: "time",
  },
  {
    title: "Message",
    value: "message",
  },
  {
    title: "Action",
    value: "action",
  },
  {
    title: "Status",
    value: "status",
  },
];

const findLogs = async () => {
  loading.value = true;
  try {
    const res = await LogService.get({ page: page.value });
    logList.value = res.data;
    totalPage.value = res.meta_data.total_pages;
    page.value = res.meta_data.page;
  } catch (err: any) {
    error.value = err.toString();
  } finally {
    loading.value = false;
  }
};
</script>
<style scoped></style>
