# import the necessary packages
import argparse
import imutils
import time
import cv2
import numpy as np
import requests
import datetime
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-p", "--prototxt", required=True,
        help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)
 
# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])
 
# initialize the Fr frame in the video stream
firstFrame = None
count = 0


# cap = cv2.VideoCapture(0) # Capture video from camera
# time.sleep(0.25)
ret, frame_record = camera.read()
FPS= 20.0
FrameSize=(frame_record.shape[1], frame_record.shape[0]) # MUST set or not thing happen !!!! vtest is 768,576.
isColor=1# flag for color(true or 1) or gray (0)
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('Video_output.avi', fourcc, FPS, FrameSize)

def load_model():
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    return net

def predict():
    # loop over the frames of the video
    global firstFrame
    global count
    net = load_model()
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break
     
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        if count%60 == 0:
            firstFrame = gray

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
     
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        # (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        #   cv2.CHAIN_APPROX_SIMPLE)
        image, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue
            
            # out.write(frame)

            # # write the flipped frame
            # out.write(frame)
            # cv2.imshow('frame',frame)

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
        count += 1
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843,
         (300, 300), 127.5)
        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]
     
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
     
                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                    # post request
                print(label)
                tstamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                try:
                    requests.post("http://172.31.78.10:8000/surveillance/alert/", data={
                        'timeStamp': str(tstamp),
                        'label': str(label).split()[0],
                        'confidence': str(label).split()[1]})
                except Exception as e:
                    print(e)
                    pass
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
     
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
     
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
     
        
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
predict()
out.save()
out.release()
cap.release()
camera.release()
            