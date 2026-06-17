cmake_minimum_required(VERSION 3.8)
project(pubsub_pkg)
# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

# Install Python package
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  src/publisher_demo.py
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  src/subscriber_demo.py
  DESTINATION lib/${PROJECT_NAME}
)

# Add C++ executable
add_executable(publisher_demo_cpp src/publisher_demo_cpp.cpp)
ament_target_dependencies(publisher_demo_cpp rclcpp std_msgs geometry_msgs)

install(TARGETS
  publisher_demo_cpp
  DESTINATION lib/${PROJECT_NAME}
)

add_executable(subscriber_demo_cpp src/subscriber_demo_cpp.cpp)
ament_target_dependencies(subscriber_demo_cpp rclcpp std_msgs geometry_msgs)

install(TARGETS
  subscriber_demo_cpp
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
