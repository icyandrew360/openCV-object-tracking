import cv2

def draw_object_tracker_info(frame, success, fps, tracker):
    info = [
        ("Selected tracker", tracker),
        ("Success", str(success)),
        ("FPS", "{:.2f}".format(fps.fps())),
        ("To quit", "Press 'q'")
    ]

    for (index, (key, value)) in enumerate(info):
        text = f"{key}: {value}"
        cv2.putText(
            frame, 
            text, 
            (10, frame.shape[0] - ((index * 20) + 20)), #This is the position of the text on the frame
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.6, #font size/scale
            (200, 100, 200), 
            2 #thickness of the text
        )

def draw_instruction_info(frame, erase=False):
    if erase:
        info = [None, None]
    else: info = [
        "Press 's' to select the object to track",
        "Press 'q' to quit the program"
    ]
    for i in range(2):
        cv2.putText(
            frame,
            info[i],
            (10, frame.shape[0] - ((i * 20) + 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.6, #font size/scale
            (0, 0, 255), 
            2 #thickness of the text
        )
