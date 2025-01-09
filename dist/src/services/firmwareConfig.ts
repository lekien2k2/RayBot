import { apiClient } from "@/utils/request";
import type {
  FirmwareConfigType,
  FirmwareConfigUpdate,
} from "@/types/firmwareConfig";
// import { SortOrder } from "@/types/data";
// import { ResponseWithMetaData } from "@/types/metaData";

export default class LogService {
  static get entity() {
    return "config";
  }

  static async get(): Promise<FirmwareConfigType> {
    return await apiClient.get(`/${this.entity}`);
  }

  static async update(data: FirmwareConfigUpdate): Promise<FirmwareConfigType> {
    return await apiClient.put(`/${this.entity}/raybot`, data);
  }
}
