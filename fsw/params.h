/*
 * Common FSW parameters, autogenerated by Python
 */

#ifndef PARAMS_H
#define PARAMS_H

#define SYS_PI 3.1416

#define JPL_QUATERNION

#include "datatypes.h"

enum SystemType {SYS_ROVER, SYS_PLANE, SYS_ROCKET, SYS_HELICOPTER};

// Global
const double mass = 125.0;
const double dimensions[3] = {0.0, 0.0, 0.0};
const SystemType fsw_system = SYS_ROVER;

#define ATT_MAX_LEAN_ANGLE 100
#define ATT_MAX_ROTATION_RATE 100
#define ATT_MAX_CLIMB_RATE 100

#define ATT_MAX_ROLL 100
#define ATT_MAX_PITCH 100
#define ATT_MAX_YAW 100

#define CLOCK_TICKS_PER_SEC 100.0f

// Plane-only
#define NUM_ENGINES 2
const double engines[NUM_ENGINES][3] = {{0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}};

// Rover-only
#define NUM_MOTORS 2
const double motors[NUM_ENGINES][3] = {{0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}};
const double motor_max_speeds[NUM_ENGINES] = {0.0, 0.0};

// Rocket-only
const double i_sp = 100.0;
const double max_fuel = 100.0;
const double mass_flow_rate = 10.0;

// Helicopter-only
#define NUM_PROPS 2
const double PROPELLERS[NUM_PROPS][3] = {{0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}};
const double PROP_THRUSTS[NUM_PROPS] = {0.0, 0.0};
const double PROP_MAX_ANGLE = 0.133f * SYS_PI;

#endif
