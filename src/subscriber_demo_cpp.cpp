#include <memory>
#include <chrono>
#include <iomanip>
#include <sstream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/header.hpp"
#include "std_msgs/msg/color_rgba.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"

using std::placeholders::_1;

class SubscriberDemo : public rclcpp::Node
{
public:
  SubscriberDemo()
  : Node("subscriber_demo")
  {
    RCLCPP_INFO(this->get_logger(), "Subscriber demo node started...");

    string_subscriber = this->create_subscription<std_msgs::msg::String>(
      "text_data", 10, std::bind(&SubscriberDemo::string_callback, this, _1));
    float_subscriber = this->create_subscription<std_msgs::msg::Float32>(
      "float_data", 10, std::bind(&SubscriberDemo::float_callback, this, _1));
    header_subscriber = this->create_subscription<std_msgs::msg::Header>(
      "header_data", 10, std::bind(&SubscriberDemo::header_callback, this, _1));
    color_subscriber = this->create_subscription<std_msgs::msg::ColorRGBA>(
      "color_data", 10, std::bind(&SubscriberDemo::color_callback, this, _1));
    point_subscriber = this->create_subscription<geometry_msgs::msg::PointStamped>(
      "point_data", 10, std::bind(&SubscriberDemo::point_callback, this, _1));
  }

private:
  void string_callback(const std_msgs::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received string: \"%s\" \n", msg->data.c_str());
  }


  void float_callback(const std_msgs::msg::Float32::SharedPtr msg)
  {
    std::string sign = (msg->data > 0) ? "POSITIVE" : "NEGATIVE"; //conditional ternary operator
    RCLCPP_INFO(this->get_logger(), "Received %s float value: %.3f \n", sign.c_str(), msg->data);
  }


  void header_callback(const std_msgs::msg::Header::SharedPtr msg)
  {
    // Convert the received timestamp to a human-readable format YYYY.MM.DD HH:MM:SS.ssssss
    double timestamp = msg->stamp.sec + msg->stamp.nanosec / 1e9;
    auto time_t_val = static_cast<time_t>(timestamp);
    auto tm = *std::localtime(&time_t_val);
    
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y.%m.%d %H:%M:%S");
    unsigned int microseconds = static_cast<unsigned int>((timestamp - std::floor(timestamp)) * 1e6);
    oss << "." << std::setfill('0') << std::setw(6) << microseconds;
    std::string time_str = oss.str();
    
    RCLCPP_INFO(this->get_logger(), "Received header with timestamp: %s and frame_id: %s \n", time_str.c_str(), msg->frame_id.c_str());
  }


  void color_callback(const std_msgs::msg::ColorRGBA::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received color r: %.2f, g: %.2f, b: %.2f, a: %.2f \n", msg->r, msg->g, msg->b, msg->a);
  }


  void point_callback(const geometry_msgs::msg::PointStamped::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received 3D point: [%.2f, %.2f, %.2f] \n", msg->point.x, msg->point.y, msg->point.z);
  }

   //declaring subscriber objects for each message type
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr string_subscriber;
  rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr float_subscriber;
  rclcpp::Subscription<std_msgs::msg::Header>::SharedPtr header_subscriber;
  rclcpp::Subscription<std_msgs::msg::ColorRGBA>::SharedPtr color_subscriber;
  rclcpp::Subscription<geometry_msgs::msg::PointStamped>::SharedPtr point_subscriber;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto subscriber_demo = std::make_shared<SubscriberDemo>();
  rclcpp::spin(subscriber_demo);
  subscriber_demo.reset();
  rclcpp::shutdown();

  return 0;
}
