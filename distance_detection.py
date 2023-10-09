import cv2
import numpy as np
import app


def calculate_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


# Function to check if a point is too close to any of the existing points
def is_too_close(point, existing_points, min_distance):
    for existing_point in existing_points:
        if calculate_distance(point, existing_point) < min_distance:
            return True
    return False

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Color ranges for detection
        color_ranges = {
            "center": ([20, 100, 100], [30, 255, 255]), #yellow
            "red": ([0, 100, 100], [10, 255, 255]),
            "white": ([36, 100, 100], [86, 255, 255]), #green
            "ficole": ([94, 100, 100], [124, 255, 255]) #blue
        }

        for color, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsvFrame, np.array(lower), np.array(upper))
            mask = cv2.dilate(mask, np.ones((5, 5), "uint8"))

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 300:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                    cv2.putText(frame, color.capitalize(), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
        
        center = (0,0)
        # Find the center of the center block
        if "center" in color_ranges:
            center_mask = cv2.inRange(hsvFrame, np.array(color_ranges["center"][0]), np.array(color_ranges["center"][1]))
            contours, _ = cv2.findContours(center_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                    center = (cX, cY)


        # Calculate distances from center center to the closest edges of other colors
        if "center" in color_ranges:
            for color, (lower, upper) in color_ranges.items():
                if color != "center":
                    mask = cv2.inRange(hsvFrame, np.array(lower), np.array(upper))
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if len(contours) == 0:
                        break
                    shortest_distance = float("inf")  # Initialize with positive infinity
                    for contour in contours:
                        rect = cv2.boundingRect(contour)
                        cx = rect[0] + rect[2] // 2
                        cy = rect[1] + rect[3] // 2
                        distance = calculate_distance(center, rect)
                        shortest_distance = min(shortest_distance, distance)
                    if shortest_distance != float("inf"):
                        cv2.putText(frame, f"{shortest_distance:.2f}", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
                        app.positions[color] = shortest_distance

        
        # Process the frame if needed

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')