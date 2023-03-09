import cv2
import time
from pyniryo import *

# stand pos: ned.move_joints([0, 0, 0, 0, 0, 0])
# [0.0072, 0.491, -1.330, 0.265, -0.0016, -0.022]
#[0.016610719777601205, -0.9264258628104207, 0.8382688690310327, 0.0031606151655640957, -1.4773161523236653, 0.02356022445625472]
#[0.004333231246330749, -0.9516503293720906, 0.7882077178030977, 0.05378198116579025, -1.340791862201843, 0.02356022445625472]
# [0.004333231246330749, -0.9516503293720906, 0.7882077178030977, 0.05378198116579025, -1.340791862201843, 0.02356022445625472]


stand_by = [0, 0.4, 0, 0, -1.5, 0]
ready_to_pick = [0.0166, -0.80, 0.75, 0.0031, -1.30, 0.0235]
about_to_pick = [0.0166, -0.95, 0.75, 0.0031, -1.30, 0.0235]
ready_to_drop_1 = [1.4, 0, 0, 0, -1.5, 0]
ready_to_drop_2 = [-1.4, 0, 0, 0, -1.5, 0]


CONFIDENCE_THRESHOLD = 0.1
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open("/home/hari/darknet/Robot/obj.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]


def pick_black_socks():
    # ned.move_joints(ready_to_pick)
    ned.move_joints(about_to_pick)
    ned.close_gripper()
    # ned.move_joints(about_to_pick)
    ned.move_joints(ready_to_drop_1)
    ned.open_gripper()
    ned.move_joints(stand_by)
    return None

def pick_white_socks():
    # ned.move_joints(ready_to_pick)
    ned.move_joints(about_to_pick)
    ned.close_gripper()
    # ned.move_joints(about_to_pick)
    ned.move_joints(ready_to_drop_2)
    ned.open_gripper()
    ned.move_joints(stand_by)
    return None    

def inference():
    net = cv2.dnn.readNet("/home/hari/darknet/Robot/backup/yolov4_last.weights", "/home/hari/darknet/Robot/yolov4.cfg")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
    
    cap = cv2.VideoCapture(-1)
    while cv2.waitKey(1) < 1:
        (grabbed, frame) = cap.read()
        if not grabbed:
            exit()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        # end = time.time()

        # for (classid, score, box) in zip(classes, scores, boxes):
        #     color = COLORS[int(classid) % len(COLORS)]
        #     label='{}'.format(class_names[int(classid)])
        #     cv2.rectangle(frame, box, color, 2)
        #     cv2.putText(frame, label, (box[0], box[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # fps = "FPS: %.2f " % (1 / (end - start))
        # cv2.putText(frame, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        # cv2.imshow("output", frame)
        print('Prediction:', classes)
        
        # Controlling the ROBOT
        if len(classes) != 0:
            if classes[0].astype(int)==0:
                pick_black_socks()
                # time.sleep(3)
            elif classes[0].astype(int) == 1:
                pick_white_socks()
                # time.sleep(3)
            else:
                pass
            
            

if __name__ == '__main__':
    
    ned = NiryoRobot("192.168.0.107")
    # ned.calibrate_auto()
    inference()
