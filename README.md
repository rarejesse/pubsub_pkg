# ROS2 Publisher/Subscriber Example


Add this package to your ROS2 workspace. Then:

```
cd ros2_ws
```
```
colcon build --symlink-install --packages-select pubsub_pkg
```

```
source install/setup.bash
```

Run the Python version of the publisher and subscriber nodes:

```
ros2 run pubsub_pkg publisher_demo.py
```

```
ros2 run pubsub_pkg subsciber_demo.py
```

Or, run the C++ version of the publisher and subscriber nodes:

```
ros2 run pubsub_pkg publisher_demo_cpp
```

```
ros2 run pubsub_pkg subsciber_demo_cpp
```
