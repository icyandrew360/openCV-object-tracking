import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import time
import cv2

from helpers import draw_instruction_info, draw_object_tracker_info
from enums import OPENCV_OBJECT_TRACKERS

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--video", type=str, help="path to input video file")
arg_parser.add_argument("-t", "--tracker", type=str, default="csrt", help="OpenCV object tracker type")

args = vars(arg_parser.parse_args())

print(f"You are currently running openCV {cv2.__version__}")
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
clear_instruction = False
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
    draw_instruction_info(frame, erase=clear_instruction)
    if bounding_box is not None:
        # This update method will locate the object's new position and return
        # a success boolean and the bounding box of the object.
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
        draw_object_tracker_info(frame, success, fps, args["tracker"])
    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        clear_instruction = True
        # manually select the bounding box on the frozen frame
        bounding_box = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        # now initialize the OpenCV object tracker using the selected
        # bounding box coordinates and it will try to follow object that you selected
        selected_tracker.init(frame, bounding_box)
        fps = FPS().start()

    elif key == ord("q"):
        break

# if we are using a webcam, release the pointer:?
if webcam:
    video_stream.stop()

# otherwise release the file pointer.
else:
    video_stream.release()

cv2.destroyAllWindows()