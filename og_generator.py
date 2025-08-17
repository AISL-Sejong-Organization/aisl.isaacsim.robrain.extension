import omni.graph.core as og

og.Controller.edit(
    {"graph_path": "/pick_and_place", "evaluator_name": "execution"},
    {
        og.Controller.Keys.CREATE_NODES: [
            ("on_playback_tick", "omni.graph.action.OnPlaybackTick"),
            ("gripper_open_value", "omni.graph.nodes.ConstantDouble"),
            ("gripper_close_value", "omni.graph.nodes.ConstantDouble"),
            ("gripper_select_if", "omni.graph.nodes.SelectIf"),
            ("gripper_write_prim_attribute", "omni.graph.nodes.WritePrimAttribute"),
            ("gripper_attribute_name", "omni.graph.nodes.ConstantToken"),
            ("gripper_path", "omni.graph.nodes.ConstantToken"),
            ("pickandplace_recv_custom_event", "omni.graph.action.OnCustomEvent"),
            ("manipulator_path", "omni.graph.nodes.ConstantToken"),
            ("pickandplace_read_attribute", "omni.graph.core.ReadVariable"),
            ("pickandplace_write_attribute", "omni.graph.core.WriteVariable"),
            ("boolean_or", "omni.graph.nodes.BooleanOr"),
            ("pickandplace_command_not", "omni.graph.nodes.ConstantToken"),
            ("pickandplace_command", "omni.graph.nodes.ConstantToken"),
            ("pickandplace_select_if", "omni.graph.nodes.SelectIf"),
            ("pickandplace_send_custom_event", "omni.graph.action.SendCustomEvent"),
            ("pickandplace_recv_custom_event_01", "omni.graph.action.OnCustomEvent"),
            ("target_follow_node", "aisl.robrain.extension.targetfollownode"),
            ("script_node", "omni.graph.scriptnode.ScriptNode"),
            ("constant_token", "omni.graph.nodes.ConstantToken"),
            ("constant_token_01", "omni.graph.nodes.ConstantToken"),
            ("write_prim_attribute", "omni.graph.nodes.WritePrimAttribute"),
            ("write_prim_attribute_01", "omni.graph.nodes.WritePrimAttribute"),
            ("pick_and_place_node_01", "aisl.robrain.extension.pickandplacenode"),
        ],
        og.Controller.Keys.CONNECT: [
            (
                "pick_and_place_node_01.outputs:gripper_grasp_command",
                "gripper_select_if.inputs:condition",
            ),
            ("gripper_close_value.inputs:value", "gripper_select_if.inputs:ifFalse"),
            ("gripper_open_value.inputs:value", "gripper_select_if.inputs:ifTrue"),
            (
                "on_playback_tick.outputs:tick",
                "gripper_write_prim_attribute.inputs:execIn",
            ),
            (
                "gripper_attribute_name.inputs:value",
                "gripper_write_prim_attribute.inputs:name",
            ),
            (
                "gripper_path.inputs:value",
                "gripper_write_prim_attribute.inputs:primPath",
            ),
            (
                "gripper_select_if.outputs:result",
                "gripper_write_prim_attribute.inputs:value",
            ),
            (
                "on_playback_tick.outputs:tick",
                "pickandplace_write_attribute.inputs:execIn",
            ),
            ("script_node.outputs:ppcmd", "pickandplace_write_attribute.inputs:value"),
            (
                "pick_and_place_node_01.outputs:pick_and_place_command",
                "boolean_or.inputs:a",
            ),
            ("pickandplace_read_attribute.outputs:value", "boolean_or.inputs:b"),
            ("boolean_or.outputs:result", "pickandplace_select_if.inputs:condition"),
            (
                "pickandplace_command_not.inputs:value",
                "pickandplace_select_if.inputs:ifFalse",
            ),
            (
                "pickandplace_command.inputs:value",
                "pickandplace_select_if.inputs:ifTrue",
            ),
            (
                "pickandplace_select_if.outputs:result",
                "pickandplace_send_custom_event.inputs:eventName",
            ),
            (
                "on_playback_tick.outputs:tick",
                "pickandplace_send_custom_event.inputs:execIn",
            ),
            (
                "pickandplace_recv_custom_event_01.outputs:execOut",
                "target_follow_node.inputs:execIn",
            ),
            (
                "constant_token.inputs:value",
                "target_follow_node.inputs:robot_prim_path",
            ),
            (
                "constant_token_01.inputs:value",
                "target_follow_node.inputs:target_prim_path",
            ),
            ("on_playback_tick.outputs:tick", "script_node.inputs:execIn"),
            ("script_node.outputs:execOut", "write_prim_attribute.inputs:execIn"),
            ("constant_token_01.inputs:value", "write_prim_attribute.inputs:primPath"),
            ("script_node.outputs:target_pos", "write_prim_attribute.inputs:value"),
            ("script_node.outputs:execOut", "write_prim_attribute_01.inputs:execIn"),
            (
                "constant_token_01.inputs:value",
                "write_prim_attribute_01.inputs:primPath",
            ),
            ("script_node.outputs:target_ori", "write_prim_attribute_01.inputs:value"),
            (
                "pickandplace_recv_custom_event.outputs:execOut",
                "pick_and_place_node_01.inputs:execIn",
            ),
            (
                "script_node.outputs:grasp_point_ori",
                "pick_and_place_node_01.inputs:grasp_point_ori",
            ),
            (
                "script_node.outputs:grasp_point_pos",
                "pick_and_place_node_01.inputs:grasp_point_pos",
            ),
            (
                "script_node.outputs:place_point_ori",
                "pick_and_place_node_01.inputs:place_point_ori",
            ),
            (
                "script_node.outputs:place_point_pos",
                "pick_and_place_node_01.inputs:place_point_pos",
            ),
            (
                "manipulator_path.inputs:value",
                "pick_and_place_node_01.inputs:robot_prim_path",
            ),
        ],
        og.Controller.Keys.CREATE_ATTRIBUTES: [
            ("script_node.outputs:grasp_point_ori", "double[4]"),
            ("script_node.outputs:grasp_point_pos", "double[3]"),
            ("script_node.outputs:place_point_ori", "double[4]"),
            ("script_node.outputs:place_point_pos", "double[3]"),
            ("script_node.outputs:ppcmd", "bool"),
            ("script_node.outputs:target_pos", "double[3]"),
            ("script_node.outputs:target_ori", "double[4]"),
        ],
        og.Controller.Keys.SET_VALUES: [
            ("gripper_open_value.inputs:value", 40.0),
            ("gripper_close_value.inputs:value", 0.0),
            ("gripper_write_prim_attribute.inputs:usePath", True),
            (
                "gripper_attribute_name.inputs:value",
                "drive:angular:physics:targetPosition",
            ),
            (
                "gripper_path.inputs:value",
                "/World/kinova_robot/robotiq_edited/Robotiq_2F_85/finger_joint",
            ),
            ("pickandplace_recv_custom_event.inputs:eventName", "pickandplace"),
            ("manipulator_path.inputs:value", "/World/kinova_robot"),
            ("pickandplace_read_attribute.inputs:variableName", "pickandplace"),
            ("pickandplace_write_attribute.inputs:variableName", "pickandplace"),
            ("pickandplace_command_not.inputs:value", "target_follow"),
            ("pickandplace_command.inputs:value", "pickandplace"),
            ("pickandplace_recv_custom_event_01.inputs:eventName", "target_follow"),
            (
                "script_node.inputs:script",
                'import rclpy\nfrom rclpy.node import Node\nfrom std_msgs.msg import String\nimport threading\nimport time\nimport numpy as np\nfrom scipy.spatial.transform import Rotation as R\n\n# === 글로벌 변수들 ===\nlast_received_data = None\nppcmd_active = False\nppcmd_timer = 0.0\ntarget_pos = None\ntarget_ori = None\nros_node = None\n\n# === 콜백 함수 ===\n\n\ndef string_callback(msg):\n    global last_received_data, ppcmd_active, ppcmd_timer\n    try:\n        floats = list(map(float, msg.data.strip().split()))\n        if len(floats) != 14:\n            print("Received data does not have 14 floats.")\n            return\n        last_received_data = floats\n        ppcmd_active = True\n        ppcmd_timer = time.time()\n        print("Pose command received. Activating ppcmd for 1 second.")\n    except Exception as e:\n        print(f"Error parsing ppcmd message: {e}")\n\n\ndef target_follow_callback(msg):\n    global target_pos, target_ori\n    try:\n        floats = list(map(float, msg.data.strip().split()))\n        if len(floats) != 6:\n            print("target_follow data does not have 6 floats.")\n            return\n        x, y, z, roll, pitch, yaw = floats\n\n\n        # RPY (degree) → quaternion (xyzw 순서)\n        r = R.from_euler("xyz", [roll, pitch, yaw], degrees=True)\n        quat = r.as_quat()  # returns [x, y, z, w]\n\n        # target_ori는 [x, y, z, w] 그대로 사용\n        target_ori = np.array(quat)\n        target_pos = np.array([x, y, z])\n\n        print("Updated target pos and orientation (xyzw, degrees input).")\n    except Exception as e:\n        print(f"Error parsing target_follow message: {e}")\n\n\n# === ROS Node 정의 ===\n\n\nclass MinimalSubscriber(Node):\n    def __init__(self):\n        super().__init__("ppcmd_listener")\n        self.create_subscription(String, "ppcmd", string_callback, 10)\n        self.create_subscription(String, "target_follow", target_follow_callback, 10)\n        self.get_logger().info("ppcmd & target_follow Subscribers initialized.")\n\n\n# === OmniGraph ScriptNode 필수 함수 ===\n\n\ndef setup(db):\n    global ros_node\n    rclpy.init()\n    ros_node = MinimalSubscriber()\n    threading.Thread(target=rclpy.spin, args=(ros_node,), daemon=True).start()\n    print("[ROS2] Subscribers and node initialized.")\n\n\ndef compute(db):\n    global last_received_data, ppcmd_active, ppcmd_timer\n    global target_pos, target_ori\n\n    if last_received_data:\n        db.outputs.grasp_point_ori = np.array(last_received_data[0:4])\n        db.outputs.grasp_point_pos = np.array(last_received_data[4:7])\n        db.outputs.place_point_ori = np.array(last_received_data[7:11])\n        db.outputs.place_point_pos = np.array(last_received_data[11:14])\n\n    if ppcmd_active and (time.time() - ppcmd_timer <= 1.0):\n        db.outputs.ppcmd = True\n    else:\n        db.outputs.ppcmd = False\n        ppcmd_active = False\n\n    if target_pos is not None and target_ori is not None:\n        db.outputs.target_pos = target_pos\n        db.outputs.target_ori = target_ori\n\n    return True\n\n\ndef cleanup(db):\n    global ros_node\n    if ros_node is not None:\n        ros_node.destroy_node()\n        rclpy.shutdown()\n    print("[ROS2] ppcmd cleanup done.")\n',
            ),
            ("constant_token.inputs:value", "/World/kinova_robot"),
            ("constant_token_01.inputs:value", "/World/kinova_robot/target_point"),
            ("write_prim_attribute.inputs:name", "xformOp:translate"),
            ("write_prim_attribute.inputs:usePath", True),
            ("write_prim_attribute_01.inputs:name", "xformOp:orient"),
            ("write_prim_attribute_01.inputs:usePath", True),
            ("pickandplace_read_attribute.inputs:graph", "/pick_and_place"),
            ("pickandplace_read_attribute.inputs:variableName", "pickandplace"),
            ("pickandplace_write_attribute.inputs:graph", "/pick_and_place"),
            (
                "pickandplace_write_attribute.inputs:variableName",
                "pickandplace",
            ),
        ],
        og.Controller.Keys.CREATE_VARIABLES: [
            ("pickandplace", "bool"),
        ],
    },
)
