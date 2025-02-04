import streamlit as st
import os
import cv2
from PIL import Image
import time
from datetime import datetime
import json

def predict(video_file_name, query, log_placeholder):
    # Initialize an empty list to keep log entries
    logs = []

    # Function to update the log placeholder with accumulated logs
    def update_logs(message, message_type='info'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if message_type == 'info':
            formatted_message = f"<p style='color: blue;'>[{timestamp}] <b>INFO:</b> {message}</p>"
        elif message_type == 'success':
            formatted_message = f"<p style='color: green;'>[{timestamp}] <b>SUCCESS:</b> {message}</p>"
        elif message_type == 'warning':
            formatted_message = f"<p style='color: orange;'>[{timestamp}] <b>WARNING:</b> {message}</p>"
        elif message_type == 'error':
            formatted_message = f"<p style='color: red;'>[{timestamp}] <b>ERROR:</b> {message}</p>"
        else:
            formatted_message = f"<p>[{timestamp}] <b>{message_type.upper()}:</b> {message}</p>"
        
        # Append the new log message
        logs.append(formatted_message)
        
        
        # Apply border style and black background to the log placeholder
        log_placeholder.markdown(
            f"""
            <div style="border: 2px solid #ddd; border-radius: 5px; padding: 10px; background-color: gray; height: 300px; overflow-y: auto;">
                <div>{'<br>'.join(logs)}</div>
            </div>
            """, unsafe_allow_html=True
        )
    
    # Simulate loading an AI model
    update_logs("Loading AI model...")
    time.sleep(3)  # Simulating model loading time
    update_logs("AI model loaded.")

    # Simulate model prediction process
    update_logs(f"Running prediction on video: {video_file_name} with query: '{query}'")
    time.sleep(3)  # Simulating prediction time
    update_logs("Step 1 running.")
    time.sleep(2)
    update_logs("Step 2 running.")
    time.sleep(2)
    update_logs("Step 3 running.")
    time.sleep(2)
    update_logs("Prediction completed.", message_type='success')
    result = {
        'How to use gun shooting': {
            '4Gx9W0XFAkA.mp4': {
                'relevant': True,
                'clip': True,
                'v_duration': 299.73,
                'bounds': [5, 10],
                'steps': [
                    {'index': 0, 'heading': 'mix it', 'absolute_bounds': [5, 7]},
                    {'index': 1, 'heading': 'bake it in oven', 'absolute_bounds': [7, 8]},
                    {'index': 2, 'heading': 'mix it', 'absolute_bounds': [8, 10]}
                ]
            }
        }
    }

    return result

def capture_frames_at_times(video_path, time_entries):
    frames = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Error: Could not open video.")
        return frames

    for entry in time_entries:
        lower_bound, upper_bound = entry['absolute_bounds']
        cap.set(cv2.CAP_PROP_POS_MSEC, lower_bound * 1000)
        ret, frame = cap.read()
        if ret:
            frames.append((frame, entry['heading'], lower_bound, upper_bound))
        else:
            st.error(f"Error: Could not read frame at {lower_bound} seconds.")
    
    cap.release()
    return frames

# Define the path to the video folder
MEDIA_FOLDER = 'media'

# List all video files in the specified directory
video_files = [f for f in os.listdir(MEDIA_FOLDER) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]

# Set the number of videos to display at a time
videos_per_page = min(4, len(video_files))

# Set the layout of the Streamlit app
st.set_page_config(layout="wide")

# Initialize session state variables if not already set
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = None
if 'submitted' not in st.session_state:
    st.session_state.submitted = None

# Create a container for the video panel
video_panel = st.container()

with video_panel:
    st.write("### Chọn Video")

    # Calculate the number of pages
    total_videos = len(video_files)
    total_pages = (total_videos - 1) // videos_per_page + 1

    # Create a slider to navigate through pages
    page = st.select_slider("Select Page", options=list(range(1, total_pages + 1)), format_func=lambda x: f'Page {x}', label_visibility="collapsed")

    # Calculate the range of videos to display
    start_index = (page - 1) * videos_per_page
    end_index = min(start_index + videos_per_page, total_videos)

    # Create columns for the current page videos
    cols = st.columns(videos_per_page)
    cols2 = st.columns(videos_per_page)

    # Display the videos and buttons for the current page
    for index, (col, video_file) in enumerate(zip(cols, video_files[start_index:end_index])):
        with col:
            st.video(os.path.join(MEDIA_FOLDER, video_file))

    for index, (col2, video_file) in enumerate(zip(cols2, video_files[start_index:end_index])):
        with col2:
            if st.button(f"Select Video {index + start_index + 1}", key=f"select_{index}"):
                st.session_state.selected_video = video_file
# Display the selected video message if one is selected
if st.session_state.selected_video:
    st.write(f"Đã chọn Video: {st.session_state.selected_video}")

# Create a container for the input box and buttons
st.write("### Nhập câu truy vấn")

# Create a form for the input box and submit button
with st.form(key='input_form'):
    col1, col2 ,col3= st.columns([10, 1, 1])

    # Input box
    with col1:
        user_input = st.text_input("Nhập câu truy vấn", placeholder="Nhập câu truy vấn.", label_visibility="collapsed")

    # Submit button
    with col2:
        submit_button = st.form_submit_button("Submit")
    with col3:
        micro_button = st.form_submit_button("🎙")

    if micro_button:
        st.write("Micro button clicked")

    # Handle form submission
    if submit_button:
        if not user_input:
            st.warning("Hãy nhập câu truy vấn.")
        else:
            if st.session_state.selected_video is None:
                st.warning("Hãy chọn một video để phân tích")
            else:
                st.session_state.submitted = True

if st.session_state.submitted:
    st.write("### Kết quả")
    log_placeholder = st.empty()
    video_file_path = os.path.join(MEDIA_FOLDER, st.session_state.selected_video)
    
    # Run prediction and update logs in real-time
    result_json = predict(st.session_state.selected_video, user_input, log_placeholder)
    
    st.write("Kết quả dự đoán:")
    st.code(result_json)
    
    video_bound = next(iter(next(iter(result_json.values())).values()))['bounds']
    times_input = next(iter(next(iter(result_json.values())).values()))['steps']
    
    if times_input and video_bound:
        try:
            frames = capture_frames_at_times(video_file_path, times_input)
            if frames:
                st.write("Thông tin trích xuất:")
                images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame, _, _, _ in frames]
                captions = [f"{heading} từ giây {lower_bound} đến giây {upper_bound}" for _, heading, lower_bound, upper_bound in frames]
                st.image(images, caption=captions, width=300)
                st.write("Video trích xuất:")
                st.video(video_file_path, start_time=video_bound[0], end_time=video_bound[1]) 
        except json.JSONDecodeError:
            st.error("Lỗi giải mã JSON")
        except ValueError:
            st.error("Lỗi giá trị không hợp lệ")
    else:
        st.write("Không có dữ liệu trả về.")
