# 作者：算个文科生吧
# 联系方式：lijinghailjh@163.com
# 作用：ljh_g335_bringup 的 CMake 构建脚本，安装 config、launch、rviz 到 share 目录
cmake_minimum_required(VERSION 3.8)
project(ljh_g335_bringup)
find_package(ament_cmake REQUIRED)
install(DIRECTORY config launch rviz DESTINATION share/${PROJECT_NAME})
ament_package()
