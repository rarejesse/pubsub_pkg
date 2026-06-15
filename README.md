# ROS2 Publisher/Subscriber Example


Add this package to your ROS2 workspace. Then:


```
cd ros2_ws
```

```
colcon build --symlink-install --packages-select pubsub_pkg
```

```
ros2 run pubsub_pkg publisher_demo.py
```
```
ros2 run pubsub_pkg subsciber_demo.py
```