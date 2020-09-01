import cv2,dlib
font=cv2.FONT_HERSHEY_SIMPLEX
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

class Detection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"Resources\shape_predictor_68_face_landmarks.dat")
        self.yourEyes = 2300
        self.frames = 7
        self.movement_range=(600,1050)
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


    def get_gaze_ratio(self, eye_region,frame,gray):

        height, width, _ = frame.shape

        mask = np.zeros((height, width), np.uint8)

        cv2.polylines(mask, [eye_region], True, 255, 2)
        cv2.fillPoly(mask, [eye_region], 255)

        eye = cv2.bitwise_and(gray, gray, mask=mask)
        min_x = np.min(eye_region[:, 0])
        max_x = np.max(eye_region[:, 0])
        min_y = np.min(eye_region[:, 1])
        max_y = np.max(eye_region[:, 1])

        gray_eye = eye[min_y: max_y, min_x: max_x]
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
        height, width = threshold_eye.shape
        left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
        x = cv2.resize(left_side_threshold, None, fx=10, fy=10)
        # cv2.imshow('left',x)
        left_side_white = cv2.countNonZero(left_side_threshold)

        right_side_threshold = threshold_eye[0:height, int(width / 2): width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        y=cv2.resize(right_side_threshold, None, fx=10, fy=10)
        # cv2.imshow('right',y)

        if right_side_white == 0:
            return 10
        else:
            return left_side_white / right_side_white

    def getEyeMovement(self, left_eye,right_eye,frame,gray):
        gaze_ratio_right_eye = self.get_gaze_ratio(right_eye,frame,gray)
        gaze_ratio_left_eye = self.get_gaze_ratio(left_eye,frame,gray)
        gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye) / 2
        return int(gaze_ratio*1000)

    def maxIn10Frames(self):

        findBlanking = {
            'blank': 0,
            'right_blank': 0,
            'left_blank': 0,
            'open': 0
        }
        findMovement={
            'right':0,
            'left':0,
            'open':0
        }

        for i in range(self.frames):
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, None, fx=0.60, fy=0.60)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray,0)

            try :
                face = faces[0]

                shape = self.predictor(gray, face)
                shape = face_utils.shape_to_np(shape)

                leftEye = shape[self.lStart:self.lEnd]
                leftEAR = int(eye_aspect_ratio(leftEye)*10000)

                rightEye = shape[self.rStart:self.rEnd]
                rightEAR = int(eye_aspect_ratio(rightEye)*10000)

                leftEAR,rightEAR=rightEAR,leftEAR                   #My Camera Flib video

                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                # cv2.putText(frame, str(leftEAR), (50, 150), font, 1, (0, 0, 255))
                # cv2.putText(frame, str(rightEAR), (300, 150), font, 1, (0, 0, 255))

                if leftEAR < self.yourEyes and rightEAR < self.yourEyes:
                    findBlanking['blank'] += 1
                elif leftEAR < self.yourEyes:
                    findBlanking['left_blank'] += 1
                elif rightEAR < self.yourEyes:
                    findBlanking['right_blank'] += 1
                else:
                    findBlanking['open'] += 1

                eye_movement=self.getEyeMovement(leftEye,rightEye,frame,gray)
                cv2.putText(frame, str(eye_movement), (150, 300), font, 2, (0, 255, 0))

                if eye_movement<=self.movement_range[0]:
                    findMovement['left']+=1
                elif eye_movement>=self.movement_range[1]:
                    findMovement['right'] += 1
                else:
                    findMovement['open'] += 1

                cv2.imshow('frame', frame)
            except:pass
            if cv2.waitKey(1)>27:
                break

        mx = ('', 0)
        for key in findBlanking:
            if findBlanking[key] >= mx[1]:
                mx = (key, findBlanking[key])

        if mx[0]=='open':
            if findMovement['right']>findMovement['left'] and findMovement['right']>=findMovement['open']:
                return 'right'
            elif findMovement['left']>findMovement['right'] and findMovement['left']>=findMovement['open']:
                return 'left'
        return mx[0]


    def showMessege(self,messege1,messege2):
        _,frame=self.cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, None, fx=0.76, fy=0.76)
        # cv2.putText(frame, str(messege1), (30, 100), font, 1, (0, 0, 255))
        # cv2.putText(frame, str(messege2), (30, 150), font, 1, (0, 0, 255))
        cv2.imshow('frame', frame)
        key= cv2.waitKey(1)
        return key






if __name__=='__main__':
    d=Detection()
    pre = 'open'
    while True:
        cur = d.maxIn10Frames()
        if cur != pre and cur == 'open':
            print(pre)
        pre = cur

