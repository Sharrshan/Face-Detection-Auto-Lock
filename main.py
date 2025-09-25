# main.py
import cv2
import os
import time
import platform

# --- SETTINGS ---
# How long (in seconds) to wait after no face is detected before locking.
# You can change this value. 10 seconds is a good starting point.
LOCK_DELAY = 10

# --- DO NOT EDIT BELOW THIS LINE (unless you know what you're doing) ---

# Load the pre-trained model for face detection (the "Face Rulebook")
# Make sure the XML file is in the same folder as this script.
try:
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise IOError("Could not load haarcascade_frontalface_default.xml. Make sure the file is in the same directory as the script.")
except Exception as e:
    print(f"Error loading cascade file: {e}")
    exit()

# Start capturing video from the default webcam (usually camera 0)
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

# This variable will store the time when a face was last seen.
last_face_seen_time = time.time()

print("Program started. Looking for a face...")
print("A window will pop up showing your webcam feed.")
print("Press 'q' in that window to quit the program.")

# This is the main loop where everything happens.
while True:
    # Read a single frame from the webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break

    # Convert the color frame to grayscale (face detection is more accurate on grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    # detectMultiScale finds faces of different sizes in the input image.
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # How much the image size is reduced at each image scale.
        minNeighbors=5,   # How many neighbors each candidate rectangle should have to retain it.
        minSize=(30, 30)  # Minimum possible object size. Faces smaller than this are ignored.
    )

    # Check if any faces were found
    if len(faces) > 0:
        # If we found a face, update the time we last saw one.
        last_face_seen_time = time.time()
        # Draw a green rectangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    else:
        # If no face was found, check how long it's been.
        time_since_last_face = time.time() - last_face_seen_time
        
        # Display a warning on the screen
        warning_text = f"No face detected. Locking in {int(LOCK_DELAY - time_since_last_face)}s"
        cv2.putText(frame, warning_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        if time_since_last_face > LOCK_DELAY:
            print(f"No face detected for {LOCK_DELAY} seconds. Locking computer.")
            
            # --- SCREEN LOCK COMMANDS ---
            system_platform = platform.system()
            
            if system_platform == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif system_platform == "Darwin": # Darwin is the system name for macOS
                os.system("/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession -suspend")
            elif system_platform == "Linux":
                # This command works for many Linux distributions (like Ubuntu with GNOME)
                os.system("gnome-screensaver-command -l")
            else:
                print(f"Unsupported operating system: {system_platform}")

            # We break the loop to stop the program after locking.
            break

    # Display the resulting frame in a window called 'Video'
    cv2.imshow('Video', frame)

    # Wait for the 'q' key to be pressed to quit the program.
    # The `& 0xFF` is a standard bitwise operation in this context.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("'q' pressed. Exiting program.")
        break

# When everything is done, release the webcam and close all windows.
video_capture.release()
cv2.destroyAllWindows()
print("Program has been shut down.")

