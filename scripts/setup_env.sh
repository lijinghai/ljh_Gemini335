#!/usr/bin/env bash
# 作者：算个文科生吧
# 联系方式：lijinghailjh@163.com
# 作用：加载 ROS 2 Humble 与本工作空间 install，并清理无效 AMENT 路径
_WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
_INSTALL_SETUP="${_WS}/install/setup.bash"

if [ ! -f /opt/ros/humble/setup.bash ]; then
  echo "[ljh_G335] ERROR: ROS 2 Humble not found. Install ROS 2 Humble first." >&2
  return 1 2>/dev/null || exit 1
fi
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash

if [ ! -f "${_INSTALL_SETUP}" ]; then
  echo "[ljh_G335] ERROR: ${_INSTALL_SETUP} not found." >&2
  echo "[ljh_G335] Run: cd ${_WS} && PARALLEL_WORKERS=1 ./scripts/build.sh" >&2
  return 1 2>/dev/null || exit 1
fi
# shellcheck source=/dev/null
source "${_INSTALL_SETUP}"

# 清理曾用包名 ljh_gemini335_bringup 的残留路径
if [ -n "${AMENT_PREFIX_PATH:-}" ]; then
  _cleaned=""
  IFS=':' read -ra _ap <<< "${AMENT_PREFIX_PATH}"
  for _p in "${_ap[@]}"; do
  [ -z "${_p}" ] && continue
  case "${_p}" in *ljh_gemini335_bringup*) continue ;; esac
  [ -d "${_p}" ] || continue
  _cleaned="${_cleaned:+${_cleaned}:}${_p}"
  done
  export AMENT_PREFIX_PATH="${_cleaned}"
fi

export LJH_G335_WS="${_WS}"
echo "[ljh_G335] ready: ${LJH_G335_WS}"
echo "[ljh_G335] packages: $(ros2 pkg prefix ljh_g335_bringup 2>/dev/null || echo MISSING)"
