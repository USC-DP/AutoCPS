#ifndef POS_CTRL_H
#define POS_CTRL_H

#include "datatypes.h"

struct PosOutputData {
  Vec3D position;
  Quaternion rotation;
};

// Choose whether to use curved waypoints
void pos_set_curved_waypoints(bool use_curved_waypoints);

// Calculate next waypoint to give to attitude control
PosOutputData pos_get_next_location();

#endif
