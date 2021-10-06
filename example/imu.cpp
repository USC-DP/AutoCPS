#include "imu.h"

std::shared_ptr<AXIStream> imu_input_st, imu_output_st;

// Recieve a quarternion from AXI stream
inline IMUInputData imu_receive_axi_stream() {
  IMUInputData input_data;
  AXIToken input;

  // Recieve linear velocity
  input = imu_input_st->get();
  input_data.linear = input.output_vec3d();

  // Recieve rotational velocity
  input = imu_input_st->get();
  input_data.rotational = input.output_vec3d();

  // Recieve GPS satellite locations
  input = imu_input_st->get();
  input_data.gps_satellite_a = input.output_vec3d();
  input = imu_input_st->get();
  input_data.gps_satellite_b = input.output_vec3d();
  input = imu_input_st->get();
  input_data.gps_satellite_c = input.output_vec3d();

  // Recieve GPS satellite distances
  input = imu_input_st->get();
  input_data.gps_distance_a = input.output_double();
  input = imu_input_st->get();
  input_data.gps_distance_b = input.output_double();
  input = imu_input_st->get();
  input_data.gps_distance_c = input.output_double();

  return input_data;
}

inline Vec3D imu_calculate_new_location(const IMUInputData input_data) {

}

inline Vec3D imu_calculate_new_linear_accel(const IMUInputData input_data) {

}

inline Vec3D imu_calculate_new_angular_accel(const IMUInputData input_data) {
  
}

// Main loop of IMU unit, continuously runs when called by startup script
void imu_main_loop(std::shared_ptr<AXIStream> input, std::shared_ptr<AXIStream> output) {
  imu_input_st = input;
  imu_output_st = output;

  // Recieve data from the IMU
  IMUInputData input_data = imu_receive_axi_stream();
  // Calculate 
    
}
