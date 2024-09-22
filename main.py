import streamlit as st
import subprocess

def replace_audio_in_video(video_template, audio_file, output_file):
    # ffmpeg command to replace the audio in the video template
    command = [
        'ffmpeg', '-i', video_template, '-i', audio_file,
        '-c:v', 'copy',  # Copy the video stream without re-encoding
        '-c:a', 'aac',   # Encode the audio stream to AAC (YouTube-friendly)
        '-b:a', '128k',  # Set the audio bitrate
        '-shortest',     # End the video when the audio ends
        output_file
    ]

    # Run the command using subprocess
    subprocess.run(command, check=True)
    return output_file

# Streamlit app
def main():
    st.title("Simple Audio to Video Converter App")

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=["mp3", "mp4", "m4a"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        video_template = "video_template_3h.mp4"  # Get the uploaded video file
        # Get the current datetime
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"video_{current_time}.mp4"
        # Replace the audio in the video template
        processed_file = replace_audio_in_video(video_template, uploaded_file, output_file)

        # Allow the user to download the processed file
        st.download_button(
            label="Download processed file",
            data=processed_file,
            file_name=file_name, 
            mime="text/plain"  # Adjust the MIME type based on your file type
        )

if __name__ == "__main__":
    main()
