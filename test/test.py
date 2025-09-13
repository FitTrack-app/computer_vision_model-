import cv2

cap = cv2.VideoCapture(0)
print("Opened:", cap.isOpened())

while True:
    ok, frame = cap.read()
    if not ok:
        print("Failed to grab frame.")
        break
    cv2.imshow("Webcam test - press q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
