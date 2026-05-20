#!/usr/bin/env bash
# 作者：算个文科生吧
# 联系方式：lijinghailjh@163.com
# 作用：编译 ljh_G335 工作空间（orbbec 驱动 + ljh_g335_bringup）
set -eo pipefail
WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/humble/setup.bash
cd "${WS}"
colcon build \
  --paths OrbbecSDK_ROS2/orbbec_camera_msgs OrbbecSDK_ROS2/orbbec_description \
           OrbbecSDK_ROS2/orbbec_camera ljh_g335_bringup \
  --parallel-workers "${PARALLEL_WORKERS:-2}" \
  --cmake-args -DCMAKE_BUILD_TYPE=Release
echo "Done: source ${WS}/scripts/setup_env.sh"
