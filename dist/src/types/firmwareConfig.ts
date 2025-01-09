export interface FirmwareConfigType {
  min_distance_move: number;
  max_distance_move: number;
  min_distance_lift: number;
  max_distance_lift: number;
  home_location: string;
  max_pwm_movement: number;
  max_pwm_lift: number;
  parameter_motor: number;
}

export interface FirmwareConfigUpdate {
  min_distance_move?: number;
  max_distance_move?: number;
  min_distance_lift?: number;
  max_distance_lift?: number;
  home_location?: string;
  max_pwm_movement?: number;
  max_pwm_lift?: number;
  parameter_motor?: number;
}
