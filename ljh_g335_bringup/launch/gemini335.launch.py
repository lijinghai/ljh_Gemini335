#!/usr/bin/env python3
# 作者：算个文科生吧
# 联系方式：lijinghailjh@163.com
# 作用：Gemini 335 一键启动入口，按 profile 加载配置并拉起官方驱动与 RViz
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

PROFILES = {
    'balanced': 'gemini335.yaml',
    'performance': 'gemini335_performance.yaml',
    'quality': 'gemini335_quality.yaml',
}


def launch_setup(context, *args, **kwargs):
    profile = LaunchConfiguration('profile').perform(context)
    bringup = get_package_share_directory('ljh_g335_bringup')
    cfg = os.path.join(bringup, 'config', PROFILES.get(profile, PROFILES['balanced']))
    rviz_cfg = os.path.join(bringup, 'rviz', 'gemini335.rviz')
    orbbec_launch = os.path.join(
        get_package_share_directory('orbbec_camera'), 'launch', 'gemini_330_series.launch.py')

    args = {
        'config_file_path': cfg,
        'rviz_config_file': rviz_cfg,
        'rviz': LaunchConfiguration('rviz').perform(context),
        'rviz_delay': LaunchConfiguration('rviz_delay').perform(context),
        'serial_number': LaunchConfiguration('serial_number').perform(context),
        'usb_port': LaunchConfiguration('usb_port').perform(context),
        'align_mode': 'SW',
        'enable_point_cloud': 'true',
        'enable_colored_point_cloud': 'true',
        'depth_registration': 'true',
        'ordered_pc': 'true',
        'point_cloud_decimation_filter_factor': LaunchConfiguration(
            'point_cloud_decimation_filter_factor').perform(context),
        'color.image_raw.enable_pub_plugins': '["image_transport/raw"]',
        'depth.image_raw.enable_pub_plugins': '["image_transport/raw"]',
    }
    pc = LaunchConfiguration('enable_point_cloud').perform(context)
    if pc:
        args['enable_point_cloud'] = pc
    colored = LaunchConfiguration('enable_colored_point_cloud').perform(context)
    if colored:
        args['enable_colored_point_cloud'] = colored
    return [IncludeLaunchDescription(
        PythonLaunchDescriptionSource(orbbec_launch), launch_arguments=args.items())]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('profile', default_value='balanced'),
        DeclareLaunchArgument('serial_number', default_value=''),
        DeclareLaunchArgument('usb_port', default_value=''),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('rviz_delay', default_value='4.0'),
        DeclareLaunchArgument('enable_point_cloud', default_value='true'),
        DeclareLaunchArgument('point_cloud_decimation_filter_factor', default_value='1',
                              description='1=full density, 2=half (faster)'),
        DeclareLaunchArgument('enable_colored_point_cloud', default_value='true'),
        OpaqueFunction(function=launch_setup),
    ])
