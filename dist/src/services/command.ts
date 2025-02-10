import { apiClient } from "@/utils/request";
import type { CommandType } from "@/types/command";
import type { metaDataType } from "@/types/share";

export default class Commandervice {
  static get entity() {
    return "command";
  }

  static async get(params?: {
    limit?: number;
    page?: number;
    // sort_order?: SortOrder;
  }): Promise<{ data: [CommandType]; meta_data: metaDataType }> {
    return await apiClient.get(`/${this.entity}/`, { params });
  }
}
