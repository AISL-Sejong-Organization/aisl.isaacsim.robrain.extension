import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import time
import numpy as np
from scipy.spatial.transform import Rotation as R

# === 글로벌 변수들 ===
last_received_data = None
ppcmd_active = False
ppcmd_timer = 0.0
target_pos = None
target_ori = None
ros_node = None

# === 콜백 함수 ===


def string_callback(msg):
    global last_received_data, ppcmd_active, ppcmd_timer
    try:
        floats = list(map(float, msg.data.strip().split()))
        if len(floats) != 14:
            print("Received data does not have 14 floats.")
            return
        last_received_data = floats
        ppcmd_active = True
        ppcmd_timer = time.time()
        print("Pose command received. Activating ppcmd for 1 second.")
    except Exception as e:
        print(f"Error parsing ppcmd message: {e}")


def target_follow_callback(msg):
    global target_pos, target_ori
    try:
        floats = list(map(float, msg.data.strip().split()))
        if len(floats) != 6:
            print("target_follow data does not have 6 floats.")
            return
        x, y, z, roll, pitch, yaw = floats

        # roll += 180도 (degree 단위에서 180도)
        roll += 180.0

        # RPY (degree) → quaternion (xyzw 순서)
        r = R.from_euler("xyz", [roll, pitch, yaw], degrees=True)
        quat = r.as_quat()  # returns [x, y, z, w]

        # target_ori는 [x, y, z, w] 그대로 사용
        target_ori = np.array(quat)
        target_pos = np.array([x, y, z])

        print("Updated target pos and orientation (xyzw, degrees input).")
    except Exception as e:
        print(f"Error parsing target_follow message: {e}")


# === ROS Node 정의 ===


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__("ppcmd_listener")
        self.create_subscription(String, "ppcmd", string_callback, 10)
        self.create_subscription(String, "target_follow", target_follow_callback, 10)
        self.get_logger().info("ppcmd & target_follow Subscribers initialized.")


# === OmniGraph ScriptNode 필수 함수 ===


def setup(db):
    global ros_node
    rclpy.init()
    ros_node = MinimalSubscriber()
    threading.Thread(target=rclpy.spin, args=(ros_node,), daemon=True).start()
    print("[ROS2] Subscribers and node initialized.")


def compute(db):
    global last_received_data, ppcmd_active, ppcmd_timer
    global target_pos, target_ori

    if last_received_data:
        db.outputs.grasp_point_ori = np.array(last_received_data[0:4])
        db.outputs.grasp_point_pos = np.array(last_received_data[4:7])
        db.outputs.place_point_ori = np.array(last_received_data[7:11])
        db.outputs.place_point_pos = np.array(last_received_data[11:14])

    if ppcmd_active and (time.time() - ppcmd_timer <= 1.0):
        db.outputs.ppcmd = True
    else:
        db.outputs.ppcmd = False
        ppcmd_active = False

    if target_pos is not None and target_ori is not None:
        db.outputs.target_pos = target_pos
        db.outputs.target_ori = target_ori

    return True


def cleanup(db):
    global ros_node
    if ros_node is not None:
        ros_node.destroy_node()
        rclpy.shutdown()
    print("[ROS2] ppcmd cleanup done.")
