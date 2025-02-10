import type { UUID } from "vue-uuid";

export interface CommandType {
  id: UUID;
  type: string;
  data?: object;
  mode: string;
  status?: string;
  created_at?: string;
  updated_at?: string;
}
