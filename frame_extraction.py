import os
import cv2
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Script to extract frames from a video file')
parser.add_argument('source_video_path', type=str, help='Path to the Source Video File')
args = parser.parse_args()

# Get the absolute path of the source video file and its directory
source_video_path = os.path.abspath(args.source_video_path)
source_video_dir = os.path.dirname(source_video_path)

# Create the frames folder in the source video directory if it doesn't exist
frames_folder_path = os.path.join(source_video_dir, 'extracted_frames')
if not os.path.exists(frames_folder_path):
    os.makedirs(frames_folder_path)

# Open the video file
video_capture = cv2.VideoCapture(source_video_path)

# Loop through all frames in the video file
for frame_number in range(int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))):
    # Read the next frame
    success, frame = video_capture.read()
    if not success:
        break
    # Save the frame as a JPEG image in the frames folder
    frame_filename = os.path.join(frames_folder_path, f'frame{frame_number+1}.jpg')
    cv2.imwrite(frame_filename, frame)

# Release the video file
video_capture.release()
print("Finished extracting frames.")
