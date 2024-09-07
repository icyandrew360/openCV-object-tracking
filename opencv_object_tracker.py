import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import time
import cv2

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--video", type=str, help="path to input video file")
arg_parser.add_argument("-t", "--tracker", type=str, default="kcf", help="OpenCV object tracker type")

args = vars(arg_parser.parse_args())

print(f"You are currently running openCV {cv2.__version__}")
# Because we are using OpenCV > 3.2, we must explicitly call the tracker with the correct name
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}
# Grab the appropriate object tracker using the tracker name from dict
selected_tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# Now we must set a bounding box for the object we want to track
bounding_box = None

# If a video file was not supplied, we will use the webcam
webcam = False
if args.get("video") == None:
    print("[INFO] starting video stream...")
    video_stream = VideoStream(src=0).start()
    time.sleep(1.0)
    webcam = True

else:
    video_stream = cv2.VideoCapture(args["video"])

fps = None

while True:
    frame = video_stream.read()
    frame = frame[1] if not webcam else frame
    # Note: frame[1] is used because the VideoStream object returns a tuple with two values when reading from cv2.VideoCapture.
    # The first value is a boolean indicating if the frame was successfully read and the second value is the frame itself.
    if frame is None:
        break

    #the following lines are used to reduce size of processed data
    frame = imutils.resize(frame, width=500)
    (FRAME_HEIGHT, FRAME_WIDTH) = frame.shape[:2] #this saves the height and width of the frame
    # frame.shape returns a tuple representing the dimensions of the image.
    # frame.shape[0]: The height of the image.
    # frame.shape[1]: The width of the image.
    # frame.shape[2]: The number of color channels in the image.
    if bounding_box is not None:
        (success, box) = selected_tracker.update(frame)

        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(
                frame, 
                (x, y), 
                (x + w, y + h), 
                (0, 255, 0), 
                2
            )

        fps.update()
        fps.stop()

        # We will display this info on the frame
        info = [
            ("Selected tracker", args["tracker"]),
            ("Success", str(success)),
            ("FPS", "{:.2f}".format(fps.fps()))
        ]

        for (index, (key, value)) in enumerate(info):
            text = f"{key}: {value}"
            cv2.putText(
                frame, 
                text, 
                (10, FRAME_HEIGHT - ((i * 20) + 20)), #This is the position of the text on the frame
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, #font size/scale
                (0, 0, 255), 
                2 #thickness of the text
            )
            






# When we are reading from

