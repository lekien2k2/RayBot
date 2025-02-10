<template>
  <v-container fluid>
    <!-- <h2 class="mb-3 text-grey-darken-3"></h2> -->

    <v-data-table-virtual
      class="rounded-lg elevation-1"
      style="height: 80vh; overflow-y: auto"
      :headers="headers"
      :items="commandList"
      :loading="loading"
      fixed-header
    >
    </v-data-table-virtual>
    <v-pagination
      :length="totalPage"
      v-model="page"
      :total-visible="7"
      @update:model-value="findcommands()"
    ></v-pagination>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { CommandType } from "@/types/command";
import commandService from "@/services/command";
// import { convertTimetampToDate } from "@/utils/time";

const commandList = ref<CommandType[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const totalPage = ref(0);
const page = ref(1);

onMounted(async () => {
  loading.value = true;
  try {
    const res = await commandService.get();
    commandList.value = res.data;
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
    title: "Type",
    value: "type",
  },
  {
    title: "Data",
    value: "data",
  },
  {
    title: "Status",
    value: "status",
  },
  {
    title: "Created At",
    value: "created_at",
  },
  {
    title: "Updated At",
    value: "updated_at",
  },
];

const findcommands = async () => {
  loading.value = true;
  try {
    const res = await commandService.get({ page: page.value });
    commandList.value = res.data;
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
