# This .py contains all the information about the flight controller needed for
# autocoding the FSW controller

import random
from decimal import Decimal
from sympy import *

x, c_1, c_2 = symbols('x c_1 c_2')
v_0, v_1 = symbols('v_0 v_1')

# A set of sigmoid functions to choose from
sigmoids = [(c_2 + exp(-1 * x)) ** (-1 * c_1), 
            c_1 * tanh(x) + c_2,
            c_1 * atan(x) + c_2,
            x / (1 + abs(x) ** c_1) ** (-1 * c_2),
            c_1 * x / (c_1 + abs(x))]

# Dummy curve fitting equations
curve_fitters = [v_0 * 360 / v_1]

# Base class for all systems
class SoftwareSystem:
    # Type of system this is
    system_type = 'system'

    # Number of FSW cycles per loop, assuming ~120Hz
    cycles_hz = 120

    # Definition for Pi
    pi_calculation = 'acos(-1.0)'

    # Whether to use JPL quaternion standard
    jpl_quaternion = True

    # Sigmoid function variables
    sigmoid = ''
    curve_fitter = ''
    c_1_init = '-1'
    c_2_init = '-1'
    s_curve_calc = ''
    curve_fit_calc = ''
    lean_angle_calc = ''
    max_speed_calc = ''

    # Maximums in software
    max_roll = '0.25 * SYS_PI'
    max_pitch = '0.25 * SYS_PI'
    max_yaw = '0.25 * SYS_PI'
    max_rotation = 'SYS_PI'
    max_climb = '15'

    autonav_enable = 1
    imu_enable = 1
    kalman_enable = 1
    sensor_enable = 1

    # Constructor and assigning a sigmoid curve
    def __init__(self, system_type, sigmoid=-1):
        self.system_type = system_type
        if sigmoid == -1:
            self.sigmoid = random.choice(sigmoids)
        else:
            self.sigmoid = sigmoid

        self.curve_fitter = random.choice(curve_fitters)

    # Generate a calculation for lean angles
    def generate_lean_angles(self, max_speed):
        print('Generating lean angles...')
        print('Max speed: ' + str(max_speed))
        print()

        self.lean_angle_calc += '  Vec3D direction_euler = quat2vec(input_waypoint.rotation);\n'
        self.lean_angle_calc += ''

        # Basic limit checking for planes and helicopters
        if self.system_type == 'plane' or self.system_type == 'helicopter':
            self.lean_angle_calc += '  if (direction_euler.x >= ATT_MAX_ROLL_ANGLE) direction_euler.x = ATT_MAX_ROLL_ANGLE;\n'
            self.lean_angle_calc += '  if (direction_euler.y >= ATT_MAX_PITCH_ANGLE) direction_euler.y = ATT_MAX_PITCH_ANGLE;\n'
            self.lean_angle_calc += '  if (direction_euler.z >= ATT_MAX_YAW_ANGLE) direction_euler.z = ATT_MAX_YAW_ANGLE;\n\n'

        self.lean_angle_calc += '  return direction_euler;\n'

    # Generate a calculation for max speed
    def generate_max_speed(self, max_speed):
        print('Generating max speed...')
        print('Max speed: ' + str(max_speed))
        print()

        self.max_speed_calc += '  double max_speed = {};\n'.format(max_speed)

        # Check for stall speed if plane
        if self.system_type == 'plane':
            self.max_speed_calc += '  double stall_speed = STALL_SPEED / sqrt(cos(direction_euler.x));\n'
            self.max_speed_calc += '  if (stall_speed > max_speed) return stall_speed;\n'

    # Generate a sigmoid curve to navigate with
    def generate_s_curve_nav(self):
        derv = simplify(diff(self.sigmoid, x))

        print('Generating S-curve for navigation...')
        print(str(ccode(derv)))
        print()

        for var in ['x', 'y', 'z']:
            self.s_curve_calc += '  ret.' + var + ' = '

            # Replace a and x with required variables
            to_add = str(ccode(derv)).replace(
                'x', var
            ).replace(
                'c_1', 'pos_autocode_s_curve_constant_{}_1'.format(var)
            ).replace(
                'c_2', 'pos_autocode_s_curve_constant_{}_2'.format(var)
            )

            self.s_curve_calc += to_add + ';\n'

    # Make a curve fitter
    def generate_curve_fitter(self):
        derv = simplify(self.curve_fitter)

        self.curve_fit_calc += '  Vec3D v_0, v_1;\n'
        self.curve_fit_calc += '  if (target.size() == 0) {\n'
        self.curve_fit_calc += '    return;\n'
        self.curve_fit_calc += '  } else if (target.size() > 1) {\n'
        self.curve_fit_calc += '    v_0 = target[0].position;\n'
        self.curve_fit_calc += '    v_1 = target[1].position;\n'
        self.curve_fit_calc += '  } else if (target.size() == 1) {\n'
        self.curve_fit_calc += '    v_0 = target[0].position;\n'
        self.curve_fit_calc += '    v_1 = v_0;\n'
        self.curve_fit_calc += '  }\n\n'

        for var in ['x', 'y', 'z']:
            # Replace a and x with required variables
            to_add = str(ccode(derv)).replace(
                'x', 'pos_autocode_s_curve_constant_{}_1'.format(var)
            ).replace(
                'v_0', 'v_0.{}'.format(var)
            ).replace(
                'v_1', 'v_1.{}'.format(var)
            )

            self.curve_fit_calc += '  pos_autocode_s_curve_constant_' + var + '_1 = '
            self.curve_fit_calc += to_add + ';\n'

            self.curve_fit_calc += '  pos_autocode_s_curve_constant_' + var + '_2 = '
            self.curve_fit_calc += to_add + ';\n'
