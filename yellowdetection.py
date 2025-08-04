import cv2
import numpy as np

def get_limits(color):
    # Convert BGR color to HSV
    color_hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)[0][0]

    # Define lower and upper HSV range with some tolerance
    lower_limit = np.array([max(color_hsv[0] - 10, 0), 100, 100])
    upper_limit = np.array([min(color_hsv[0] + 10, 179), 255, 255])

    return lower_limit, upper_limit

yellow = [0, 255, 255]  # Yellow in BGR

cap = cv2.VideoCapture(0)  # Change index if needed

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        # Draw rectangle on the original frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
