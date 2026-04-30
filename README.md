#Highway Vehicle Tracker

## Project Overview

Highway Vehicle Tracker is a computer vision application that detects, tracks, and counts moving vehicles on highway footage in real-time. The system uses background subtraction techniques combined with Euclidean distance-based tracking to identify and follow vehicles as they move through the camera's field of view.

The project solves the problem of automated traffic monitoring and vehicle counting, which is essential for traffic management, flow analysis, and transportation planning. By processing video footage frame-by-frame, the system can distinguish individual vehicles, assign unique IDs, and maintain accurate counts of both currently visible and total vehicles that have passed through the monitored area.

Key features include real-time vehicle detection using MOG2 background subtraction, persistent object tracking with unique ID assignment, live on-screen statistics display showing current and cumulative vehicle counts, and configurable region-of-interest (ROI) monitoring for focused highway lane analysis.

## Tools & Technologies Used

- **Python 3.x** - Primary programming language
- **OpenCV (cv2)** - Computer vision library for video processing and object detection
- **NumPy** - Array operations and mathematical computations (implicit dependency of OpenCV)
- **MOG2 Background Subtractor** - Gaussian mixture-based background/foreground segmentation
- **Euclidean Distance Tracking** - Custom implementation for object tracking across frames

## Installation & Setup

### Prerequisites
- Python 3.7 or higher installed on your system
- pip package manager
- A video file of highway traffic (e.g., `highway.mp4`)

### Step-by-Step Installation

1. **Clone or download the project repository**
   ```bash
   cd path/to/project
   ```

2. **Install required dependencies**
   ```bash
   pip install opencv-python numpy
   ```
   Expected outcome: Successfully installed opencv-python and numpy packages

3. **Verify OpenCV installation**
   ```bash
   python -c "import cv2; print(cv2.__version__)"
   ```
   Expected outcome: Displays OpenCV version (e.g., 4.8.0)

4. **Place your video file**
   - Ensure `highway.mp4` is in the project root directory
   - Or update the video path in the main script:
     ```python
     cap = cv2.VideoCapture("path/to/your/video.mp4")
     ```

5. **Run the application**
   ```bash
   python main_fullframe_counter.py
   ```
   Expected outcome: Opens multiple windows showing vehicle tracking visualization

## Usage & Sample Outputs

### Example 1: Full Frame Vehicle Tracking
**Input/Action:** Run `python main_fullframe_counter.py`

**Output:** 
- Opens "Vehicle Tracking & Counting" window displaying the full highway view
- Green bounding boxes around detected vehicles
- Blue ID numbers above each tracked vehicle
- Black info panel showing:
  - Current Count: 8 (vehicles currently visible)
  - Total Counted: 45 (unique vehicles seen so far)
  - Frame: 1234

### Example 2: Region of Interest (ROI) Tracking
**Input/Action:** Run `python main_with_counter.py`

**Output:**
- Opens three windows: "ROI - Vehicle Detection", "Full Frame", "Mask"
- Focuses on specific highway lanes (rows 340-720, columns 500-800)
- Displays tracking within the defined region
- Info panel shows current and total counts specific to ROI

### Example 3: Background Subtraction Mask
**Input/Action:** View the "Background Mask" or "Mask" window during execution

**Output:**
- Binary (black and white) visualization
- White pixels represent moving objects (vehicles)
- Black pixels represent static background (road, barriers)
- Helps visualize detection quality

### Example 4: Console Statistics Output
**Input/Action:** Monitor terminal while program runs

**Output:**
```
Frame 30: Active=5, Total=12
Frame 60: Active=7, Total=18
Frame 90: Active=6, Total=24
...
==================================================
FINAL STATISTICS
==================================================
Total frames processed: 3240
Total unique vehicles counted: 127
Vehicle IDs: [0, 1, 2, 3, 4, ..., 126]
==================================================
```

### Example 5: Exit and View Final Report
**Input/Action:** Press ESC or Q key to stop tracking

**Output:**
- All windows close
- Terminal displays final statistics summary
- Shows total frames processed and complete list of tracked vehicle IDs

### Example 6: Real-time Detection Progress
**Input/Action:** Observe frame counter and detections during playback

**Output:**
- Frame counter increments (top-left of video)
- Current Count fluctuates as vehicles enter/exit view (3→7→5→9)
- Total Counted only increases when new vehicles appear (never decreases)

## Project Structure

```
highway-vehicle-tracker/
│
├── main.py                          # Original main script (with bug fix needed)
├── main_with_counter.py             # ROI-based tracking with counters
├── main_fullframe_counter.py        # Full frame tracking with counters (recommended)
├── tracker.py                       # EuclideanDistTracker class implementation
├── highway.mp4                      # Sample highway video footage
│
├── README.md                        # Project documentation (this file)
├── requirements.txt                 # Python dependencies
│
└── outputs/                         # (Optional) Screenshots and sample results
    ├── tracking_screenshot.png
    └── final_statistics.txt
```

### Key Files Description
- **tracker.py** - Contains `EuclideanDistTracker` class that maintains vehicle IDs and tracks center points using Euclidean distance calculations
- **main_fullframe_counter.py** - Main application file with full frame processing and visual counter display
- **main_with_counter.py** - Alternative version using ROI for focused lane monitoring
- **highway.mp4** - Input video file showing highway traffic (replace with your own footage)

## Testing

### Manual Testing
Run the application and verify:
```bash
python main_fullframe_counter.py
```

**Expected Results:**
1. Windows open without errors
2. Vehicles are detected and bounded by green rectangles
3. Each vehicle receives a unique numeric ID
4. Counter increments when new vehicles appear
5. Tracking persists across frames (same vehicle keeps same ID)
6. Program exits cleanly with ESC/Q key

### Verification Checklist
- [ ] Video loads successfully
- [ ] Background subtraction mask shows moving objects in white
- [ ] Bounding boxes appear around vehicles
- [ ] ID numbers are visible and stable
- [ ] Current count matches visible vehicles (±1-2 tolerance)
- [ ] Total count only increases (never decreases)
- [ ] Final statistics print correctly on exit

**Note:** Automated unit tests are not currently implemented. Future versions may include pytest-based tests for the tracker module.

## Notes & Troubleshooting

### Common Issues

**Issue 1: "Can't open video file" error**
- **Solution:** Verify `highway.mp4` exists in the same directory as the script
- **Alternative:** Use absolute path: `cap = cv2.VideoCapture("/full/path/to/highway.mp4")`

**Issue 2: Windows don't appear**
- **Solution:** Ensure you're not running in a headless environment (no display)
- **For WSL/Linux:** Install X server or use VNC
- **Check:** `echo $DISPLAY` should output `:0` or similar

**Issue 3: Video ends immediately / black screen**
- **Solution:** Check video codec compatibility
- **Fix:** Convert video using: `ffmpeg -i input.mp4 -vcodec libx264 output.mp4`

**Issue 4: Poor detection / too many false positives**
- **Solution:** Adjust detection threshold in code:
  ```python
  if area > 500:  # Increase this value to reduce false positives
  ```
- **Alternative:** Tune MOG2 parameters:
  ```python
  object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=50)
  ```

**Issue 5: Tracking IDs jump/switch between vehicles**
- **Solution:** Increase distance threshold in `tracker.py`:
  ```python
  if dist < 35:  # Increase from 25 to 35 for more stable tracking
  ```

**Issue 6: ImportError for cv2 or numpy**
- **Solution:** Reinstall dependencies:
  ```bash
  pip install --upgrade opencv-python numpy
  ```

### Performance Tips
- Use ROI version (`main_with_counter.py`) for faster processing on slower machines
- Reduce video resolution if lagging: `frame = cv2.resize(frame, (640, 360))`
- Adjust `cv2.waitKey(30)` to `cv2.waitKey(1)` for faster playback

### Contact & Support
For questions or issues, contact: **<STUDENT_EMAIL>** or create an issue in the repository.

## License

This project is available under the **MIT License** - feel free to use, modify, and distribute.

To change the license: Replace or edit the `LICENSE` file in the repository root.

## Contribution

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/improvement-name`
3. Commit your changes: `git commit -m "Add improvement description"`
4. Push to branch: `git push origin feature/improvement-name`
5. Submit a Pull Request with detailed description

**Suggested Improvements:**
- Add video output recording functionality
- Implement vehicle speed estimation
- Add support for multiple ROI zones
- Create web-based dashboard for statistics
- Integrate deep learning models (YOLO, SSD) for better detection

---

## Author

**<STUDENT_NAME>**  
**<STUDENT_EMAIL>**  
**<COURSE_NAME>** - <SEMESTER/YEAR>
