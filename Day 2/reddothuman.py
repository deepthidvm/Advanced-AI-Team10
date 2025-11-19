import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            lm = face.landmark

            # Eyebrow landmark IDs
            left = lm[105]
            right = lm[334]

            # Convert to pixel coordinates
            x1 = int(left.x * frame.shape[1])
            y1 = int(left.y * frame.shape[0])
            x2 = int(right.x * frame.shape[1])
            y2 = int(right.y * frame.shape[0])

            # Midpoint between eyebrows
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2

            # Draw red dot only
            cv2.circle(frame, (mid_x, mid_y), 6, (0, 0, 255), -1)

    cv2.imshow("Eyebrow Dot", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()