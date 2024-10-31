import streamlit as st
import subprocess
import requests
from datetime import datetime
import tempfile
import os

# Function to download file from Google Drive
def download_from_google_drive(drive_url, output_path):
    response = requests.get(drive_url)
    with open(output_path, 'wb') as file:
        file.write(response.content)

# Function to replace audio in the video using ffmpeg
def replace_audio_in_video(video_template_path, audio_file_path, output_file_path):
    # ffmpeg command to replace the audio in the video template
    command = [
        'ffmpeg', '-i', video_template_path, '-i', audio_file_path,
        '-c:v', 'copy',  # Copy the video stream without re-encoding
        '-c:a', 'aac',   # Encode the audio stream to AAC (YouTube-friendly)
        '-b:a', '128k',  # Set the audio bitrate
        '-shortest',     # End the video when the audio ends
        output_file_path
    ]
    
    # Run the command using subprocess
    subprocess.run(command, check=True)

# Streamlit app
def main():
    st.title("Simple Audio to Video Converter App")
    st.write("")  # Adds a blank line (space)
    multi = '''Quickly and easily convert your audio 🎵 files (MP3, M4A, MP4, MPEG4) into a video 🎞️ format, ready for YouTube uploads, with a pre-defined, low-quality background image throughout the video. Perfect for sharing recordings on YouTube without the need for complex video editing.
    It’s fast and secure—since it’s a Streamlit app, none of your data is stored or saved. Just upload, convert, and download with peace of mind.
    '''
    st.markdown(multi)
    # Define Google Drive link (adjusted for direct download)
    google_drive_link = "https://drive.google.com/uc?export=download&id=1R1KemckSVIyFHvI8DxXXCR8CkK0tLHSL"

    # Temporary location to save the downloaded video template
    video_template_path = os.path.join(tempfile.gettempdir(), "video_template.mp4")

    # Download video template from Google Drive
    st.info("Downloading video template...")
    download_from_google_drive(google_drive_link, video_template_path)
    st.success("Video template downloaded successfully!")

    # File upload for audio
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "m4a", "mp4"])

    if uploaded_file is not None:
        st.success("Audio file uploaded successfully!")

        # Save the uploaded audio file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_file.write(uploaded_file.read())
            audio_file_path = temp_audio_file.name

        # Get the current datetime for unique file naming
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_name = f"video_{current_time}.mp4"
        output_file_path = os.path.join(tempfile.gettempdir(), output_file_name)

        # Replace the audio in the video template
        replace_audio_in_video(video_template_path, audio_file_path, output_file_path)

        # Allow the user to download the processed video file
        with open(output_file_path, "rb") as video_file:
            st.download_button(
                label="Download processed video",
                data=video_file,
                file_name=output_file_name, 
                mime="video/mp4"
            )

if __name__ == "__main__":
    main()
