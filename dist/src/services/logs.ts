import { apiClient } from "@/utils/request";
import type { LogType } from "@/types/logs";
import type { metaDataType } from "@/types/share";

export default class LogService {
  static get entity() {
    return "logs";
  }

  static async get(params?: {
    limit?: number;
    page?: number;
    // sort_order?: SortOrder;
  }): Promise<{ data: [LogType]; meta_data: metaDataType }> {
    return await apiClient.get(`/${this.entity}/`, { params });
  }
}
