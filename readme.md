## Small video object tracking project

Will accept video files using the the --video flag

Without a specified video file, webcam will be used.

Will accept the following OpenCV trackers using the --tracker flag:
- "csrt"
- "kcf"
- "boosting"
- "mil"
- "tld"
- "medianflow"
- "mosse"

Default is set to csrt.

After selecting the bounding box around an object you would like to track, the box will follow the selected object in real time.
