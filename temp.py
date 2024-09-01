if st.button(f"Select Video {index + start_index + 1}", key=f"select_{index}"):
    st.session_state.selected_video = video_file