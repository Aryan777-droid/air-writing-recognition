import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ── MediaPipe setup (same as your current code) ───────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

# ── Webcam (same as your current code, CAP_AVFOUNDATION for Mac) ──────────────
camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

ret, frame = camera.read()
h, w = frame.shape[:2]

# ── Drawing canvas (transparent layer on top of webcam) ───────────────────────
canvas = np.zeros((h, w, 3), dtype=np.uint8)

prev_x, prev_y = None, None
draw_color = (0, 255, 0)   # default green
brush_size = 5

os.makedirs("screenshots", exist_ok=True)

# ── Helper: which fingers are up? ─────────────────────────────────────────────
def fingers_up(lm):
    tips = [8, 12, 16, 20]
    raised = [lm[tip].y < lm[tip - 2].y for tip in tips]
    return raised  # [index, middle, ring, pinky]

# ── Main loop ─────────────────────────────────────────────────────────────────
print("Running! Show your hand.")
print("Index finger only = draw | Open hand = pause | C = clear | S = save | Q = quit")

while True:
    success, frame = camera.read()
    if not success:
        break

    frame    = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results  = hands.process(rgb_frame)

    print("Hand detected:", results.multi_hand_landmarks is not None)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw skeleton (same as your current code)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            # Index fingertip position in pixels
            fx = int(lm[8].x * w)
            fy = int(lm[8].y * h)

            raised = fingers_up(lm)
            only_index = raised[0] and not raised[1] and not raised[2] and not raised[3]
            open_hand  = all(raised)

            if only_index:
                # DRAW MODE
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (fx, fy), draw_color, brush_size)
                prev_x, prev_y = fx, fy
                cv2.circle(frame, (fx, fy), 8, draw_color, -1)  # cursor dot
                cv2.putText(frame, "DRAWING", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # PEN LIFTED
                prev_x, prev_y = None, None
                cv2.putText(frame, "PAUSED", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
    else:
        prev_x, prev_y = None, None

    # Blend canvas strokes onto the camera frame
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    frame[mask > 0] = canvas[mask > 0]

    # Instructions at bottom
    cv2.putText(frame, "C=Clear | S=Save | Q=Quit",
                (10, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    cv2.imshow("My Camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        print("Canvas cleared.")
    elif key == ord('s'):
        ts   = time.strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/airwrite_{ts}.png"
        cv2.imwrite(path, frame)
        print(f"Saved → {path}")

camera.release()
cv2.destroyAllWindows()