# Air Writing Recognition ✍️

A computer vision project that lets you write letters and shapes in the air using just your index finger — no pen, no touch, just hand gestures tracked through your webcam in real time.

## How it works

- Uses your webcam to track your hand in real time
- When only your **index finger** is up (all other fingers down), it enters **writing mode** and starts drawing based on your finger's movement
- When more than one finger is up, it stays in **tracking mode** and just follows your hand without drawing
- This gesture-based switching lets you write and pause naturally, without needing a keyboard or mouse

## Tech Stack

- **Python**
- **OpenCV** — for video capture and rendering the drawing
- **MediaPipe** — for real-time hand and finger landmark detection

## Demo

<!-- 
\
<img width="1447" height="806" alt="image" src="https://github.com/user-attachments/assets/a73419fc-2307-40a9-8693-79f0a9624743" />





Add a screenshot or GIF here, e.g.: -->
<!-- ![Demo](screenshots/demo.gif) -->

## How to Run

```bash
pip install opencv-python mediapipe
python main.py
```

Make sure your webcam is connected, then hold up just your index finger to start writing in the air.

## What I Learned

Working on this project helped me understand real-time hand-tracking using MediaPipe's landmark detection, and how to translate finger position data into an interactive drawing system using OpenCV.

## Future Improvements

- Recognize written letters/text using a character recognition model
- Add multiple colors/brush sizes selectable via gestures
- Save drawings as image files
