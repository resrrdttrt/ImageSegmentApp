import cv2
import streamlit as st
from PIL import Image
import numpy as np
import os

# Path to the media folder
MEDIA_FOLDER = 'media/'

import cv2
import streamlit as st
import os
from PIL import Image

def capture_frames_at_times(video_path, time_entries):
    frames = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Error: Could not open video.")
        return frames

    for entry in time_entries:
        lower_bound, upper_bound = entry['absolute_bounds']
        cap.set(cv2.CAP_PROP_POS_MSEC, lower_bound * 1000)  # Set time in milliseconds
        ret, frame = cap.read()
        if ret:
            frames.append((frame, entry['heading'], lower_bound, upper_bound))
        else:
            st.error(f"Error: Could not read frame at {lower_bound} seconds.")
    
    cap.release()
    return frames

import cv2
import streamlit as st
import os
from PIL import Image

st.title("Video Frame Extraction at Specific Times")

# Define the video file path (use relative path for the media folder)
video_file_path = os.path.join(MEDIA_FOLDER, 'vid2.mp4')

# Check if the video file exists
if not os.path.isfile(video_file_path):
    st.error("Error: Video file does not exist.")
else:
    # Display video
    st.video(video_file_path)

    # Input JSON data
    times_input = st.text_area("Enter JSON data with time entries (e.g., [{\"index\": 1, \"heading\": \"Hold them both\", \"absolute_bounds\": [60, 70]}])")
    
    if times_input:
        try:
            # Parse JSON input into a list of dictionaries
            import json
            time_entries = json.loads(times_input)
            
            # Capture frames at specified times
            frames = capture_frames_at_times(video_file_path, time_entries)
            
            if frames:
                st.write("Captured Frames:")

                # Convert OpenCV images to PIL and display them horizontally
                images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame, _, _, _ in frames]
                captions = [f"{heading} at {lower_bound} to {upper_bound} seconds" for _, heading, lower_bound, upper_bound in frames]
                st.image(images, caption=captions, width=200)

        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please ensure the JSON data is correctly formatted.")
        except ValueError:
            st.error("Please ensure the JSON data is correctly formatted and includes 'index', 'heading', and 'absolute_bounds'.")
