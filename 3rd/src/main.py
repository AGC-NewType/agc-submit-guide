#!/usr/bin/env python
import os
import json
import rospy
from urllib import request
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped

rospy.init_node('opencv_example', anonymous=True)
rate = rospy.Rate(0.2)
rospy.loginfo("SUBSCRIBING START")

MESSAGE_MISSION_START = {
        "team_id": "user30",
        "command": "MISSION_START"
        }

MISSION_API_URL = os.environ['REST_MISSION_URL']
ANSWER_API_URL = os.environ['REST_ANSWER_URL']
mission_trigger=True

class MissionStart:
    def __init__(self):
        self.armed_state=False
        self.pose_z=0.

    def cb_state(self, msg):
        self.armed_state = msg.armed

    def cb_pose(self, msg):
        self.pose_z = msg.pose.position.z

    def mission_start(self):
        global mission_trigger
        if mission_trigger==True:
            if self.armed_state == True and self.pose_z > 0.5:
                print("Take-Off and Mission Start!")
                data_mission = json.dumps(MESSAGE_MISSION_START).encode('utf-8')
                req = request.Request(MISSION_API_URL, data=data_mission)
                resp = request.urlopen(req)
                status = eval(resp.read().decode('utf-8'))
                print("received message: "+status['msg'])

                if "OK" == status['status']:
                    print("data requests successful!!")
                elif "ERROR" == status['status']:    
                    raise ValueError("Receive ERROR status. Please check your source code.")    

def main():
    data_path = r'/home/agc2022/dataset/'
    data_list = os.listdir(data_path)
    data_list.sort()
    print(f"Get resque text & image.. {data_list}")

    callbacks = MissionStart()
    sub_state=rospy.Subscriber("/scout/mavros/state", State, callbacks.cb_state)
    sub_pose=rospy.Subscriber("/scout/mavros/local_position/pose", PoseStamped, callbacks.cb_pose)
    global mission_trigger
    while mission_trigger == True:
        callbacks.mission_start()

    ## TODO : 답안지 생성 & 제출 ##
    temp={
    "team_id": "userxx",
    "secret": "!@#$%^&*()",
    "answer_sheet": 
        {
            "no": "1",
            "answer": "4"
        }
    }
    
    # post to API server
    data = json.dumps(temp).encode('utf-8')
    req =  request.Request(ANSWER_API_URL, data=data)

    # check API server return
    resp = request.urlopen(req)
    status = eval(resp.read().decode('utf-8'))
    print("received message: "+status['msg'])

    if "OK" == status['status']:
        print("data requests successful!!")
    elif "ERROR" == status['status']:    
        raise ValueError("Receive ERROR status. Please check your source code.")    
        
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == "__main__":
    main()
