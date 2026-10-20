import rclpy, random
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import cv2

class ImageProc(Node):
    def __init__(self):
        super().__init__("sample1")
        self.sub = self.create_subscription(Image, "/image_raw", self.get_image, 10)
        self.bridge = CvBridge()
        file = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
        self.classifier = cv2.CascadeClassifier(file)
        self.pub = self.create_publisher(Image, "face", 10)


    def get_image(self, data):
        try:
            org = self.bridge.imgmsg_to_cv2(data, "bgr8")
            gray = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
            faces = self.classifier.detectMultiScale(gray, 1.1, 1, cv2.CASCADE_FIND_BIGGEST_OBJECT)

            if len(faces) != 0:
                r = faces[0]
                cv2.rectangle(org, tuple(r[0:2]), tuple(r[0:2]+r[2:4]), (0, 255, 255), 4)
                cv2.imwrite("/tmp/image.jpg", org)
                out = self.bridge.cv2_to_imgmsg(org, "bgr8")
                self.pub.publish(out)

        except CvBridgeError as e:
            print(e)


def main():
    rclpy.init()
    sample1 = ImageProc()
    rclpy.spin(sample1)
