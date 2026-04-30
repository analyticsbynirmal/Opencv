import cv2
import sys
from tracker import EuclideanDistTracker

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("G:\opencv\highway.mp4")

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

frame_count = 0
total_objects_counted = set()  # Track unique IDs

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read frame")
        break
    
    frame_count += 1

    # 1. Object Detection (full frame)
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Larger threshold for full frame
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    
    # Count objects
    current_count = len(boxes_ids)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        total_objects_counted.add(id)
        
        # Draw tracking info
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Create info panel with statistics
    panel_height = 180
    cv2.rectangle(frame, (10, 10), (450, panel_height), (0, 0, 0), -1)
    cv2.rectangle(frame, (10, 10), (450, panel_height), (255, 255, 255), 3)
    
    # Display statistics
    y_offset = 50
    cv2.putText(frame, "VEHICLE COUNTER", (20, y_offset), 
                cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 0), 2)
    
    y_offset += 40
    cv2.putText(frame, f"Current Count: {current_count}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    y_offset += 40
    cv2.putText(frame, f"Total Counted: {len(total_objects_counted)}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    
    y_offset += 40
    cv2.putText(frame, f"Frame: {frame_count}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Resize for display
    frame_display = cv2.resize(frame, (1280, 720))
    mask_display = cv2.resize(mask, (1280, 720))

    cv2.imshow("Vehicle Tracking & Counting", frame_display)
    cv2.imshow("Background Mask", mask_display)

    # Console output
    if frame_count % 30 == 0:
        print(f"Frame {frame_count}: Active={current_count}, Total={len(total_objects_counted)}")

    key = cv2.waitKey(30)
    if key == 27 or key == ord('q'):
        break

print(f"\n{'='*50}")
print(f"FINAL STATISTICS")
print(f"{'='*50}")
print(f"Total frames processed: {frame_count}")
print(f"Total unique vehicles counted: {len(total_objects_counted)}")
print(f"Vehicle IDs: {sorted(total_objects_counted)}")
print(f"{'='*50}")

cap.release()
cv2.destroyAllWindows()