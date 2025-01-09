export interface Network {
  interface: string;
  ip?: string;
  gateway?: string;
  netmask?: string;
  dns?: string;
  type: string;
  ip_mode: string;
}

export type NetworkUpdate = Omit<Partial<Network>, "type">;
