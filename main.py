import streamlit as st
import subprocess
from datetime import datetime
import tempfile

def replace_audio_in_video(video_template, audio_file_path, output_file_path):
    # ffmpeg command to replace the audio in the video template
    command = [
        'ffmpeg', '-i', video_template, '-i', audio_file_path,
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

    # File upload
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "mp4", "m4a"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
            temp_audio_file.write(uploaded_file.read())
            audio_file_path = temp_audio_file.name

        video_template = "video_template_3h.mp4"  # Assuming you already have this video template

        # Get the current datetime
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"video_{current_time}.mp4"

        # Replace the audio in the video template
        replace_audio_in_video(video_template, audio_file_path, output_file)

        # Allow the user to download the processed file
        with open(output_file, "rb") as video_file:
            st.download_button(
                label="Download processed file",
                data=video_file,
                file_name=output_file, 
                mime="video/mp4"  # Correct MIME type for video
            )

if __name__ == "__main__":
    main()
