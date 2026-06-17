#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

#include <array>
#include <random>

#include "geometry_msgs/msg/point_stamped.hpp"
#include "std_msgs/msg/color_rgba.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/header.hpp"

class PublisherDemo : public rclcpp::Node
{
public:
  PublisherDemo()
  : Node("publisher_demo"), rng_(std::random_device{}())
  {
    RCLCPP_INFO(this->get_logger(), "Publisher demo node started...");

    //Create publishers objects for each message type, the 2nd argument relates to QoS settings, 10 is the default queue size for messages
    string_publisher = this->create_publisher<std_msgs::msg::String>("text_data", 10);
    float_publisher = this->create_publisher<std_msgs::msg::Float32>("float_data", 10);
    header_publisher = this->create_publisher<std_msgs::msg::Header>("header_data", 10);
    color_publisher = this->create_publisher<std_msgs::msg::ColorRGBA>("color_data", 10);
    point_publisher = this->create_publisher<geometry_msgs::msg::PointStamped>("point_data", 10);

    //Create timers to call the publisher functions at a fixed rate
    //Timers automatically run in independent threads (they don't block each other or the main thread)
    //The first argument is the timer period in seconds, so (1/5.0) means 5 Hz
    timer1 = this->create_wall_timer(500ms, std::bind(&PublisherDemo::string_publisher_timer, this));  // (1/2.0)
    timer2 = this->create_wall_timer(1000ms, std::bind(&PublisherDemo::float_publisher_timer, this));  // (1/1.0)
    timer3 = this->create_wall_timer(1000ms, std::bind(&PublisherDemo::header_publisher_timer, this)); // (1/1.0)
    timer4 = this->create_wall_timer(1000ms, std::bind(&PublisherDemo::color_publisher_timer, this));  // (1/1.0)
    timer5 = this->create_wall_timer(
      std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::duration<double>(1.0 / 1.5)),
      std::bind(&PublisherDemo::point_publisher_timer, this));
  }

private:
  void string_publisher_timer()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "this is text data from " + std::string(this->get_name());
    string_publisher->publish(msg);
  }

  void float_publisher_timer()
  {
    auto msg = std_msgs::msg::Float32();
    msg.data = random_uniform(-100.0f, 100.0f); //random float between -100 and 100
    float_publisher->publish(msg);
  }

  void header_publisher_timer()
  {
    auto msg = std_msgs::msg::Header();
    msg.stamp = this->get_clock()->now(); //current time as a ROS2 timestamp
    msg.frame_id = "global"; //typically indicates the coordinate frame of reference for the data
    header_publisher->publish(msg);
  }

  void color_publisher_timer()
  {
    auto msg = std_msgs::msg::ColorRGBA();
    std::array<float, 4> rgba = {
      random_uniform(0.0f, 1.0f),
      random_uniform(0.0f, 1.0f),
      random_uniform(0.0f, 1.0f),
      random_uniform(0.0f, 1.0f)}; //4 random RGBA values between 0 and 1
    msg.r = rgba[0];
    msg.g = rgba[1];
    msg.b = rgba[2];
    msg.a = rgba[3];
    color_publisher->publish(msg);
  }

  void point_publisher_timer()
  {
    auto msg = geometry_msgs::msg::PointStamped();
    msg.header.stamp = this->get_clock()->now();
    msg.header.frame_id = "map";
    msg.point.x = random_uniform(-10.0f, 10.0f);
    msg.point.y = random_uniform(-10.0f, 10.0f);
    msg.point.z = random_uniform(-10.0f, 10.0f);
    point_publisher->publish(msg);
  }

  float random_uniform(float low, float high)
  {
    std::uniform_real_distribution<float> dist(low, high);
    return dist(rng_);
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr string_publisher;
  rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr float_publisher;
  rclcpp::Publisher<std_msgs::msg::Header>::SharedPtr header_publisher;
  rclcpp::Publisher<std_msgs::msg::ColorRGBA>::SharedPtr color_publisher;
  rclcpp::Publisher<geometry_msgs::msg::PointStamped>::SharedPtr point_publisher;

  rclcpp::TimerBase::SharedPtr timer1;
  rclcpp::TimerBase::SharedPtr timer2;
  rclcpp::TimerBase::SharedPtr timer3;
  rclcpp::TimerBase::SharedPtr timer4;
  rclcpp::TimerBase::SharedPtr timer5;

  std::mt19937 rng_;  // Mersenne Twister random number generator, standard in C++ for generating random numbers
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto publisher_demo = std::make_shared<PublisherDemo>();
  rclcpp::spin(publisher_demo);
  publisher_demo.reset();
  rclcpp::shutdown();

  return 0;
}