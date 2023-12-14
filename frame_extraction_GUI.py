import os, cv2, tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FrameExtractor:
    def __init__(self, window):
        self.window = window
        self.progress = ttk.Progressbar(self.window, length=200, mode='determinate')
        self.progress.pack_forget()

    def extract_frames(self, source_video_path):
        try:
            self.progress.pack()

            source_video_path = os.path.abspath(source_video_path)
            source_video_dir = os.path.dirname(source_video_path)
            video_file_name = os.path.splitext(
                os.path.basename(source_video_path))[0]

            frames_folder_path = os.path.join(source_video_dir, f'{video_file_name}_extracted_frames')

            if os.path.exists(frames_folder_path):
                raise FileExistsError("Folder already exists")

            os.makedirs(frames_folder_path)
            video_capture = cv2.VideoCapture(source_video_path)
            if not video_capture.isOpened():
                raise ValueError("Unable to open video file")

            total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.progress['maximum'] = total_frames
            update_frequency = max(5, total_frames // 100)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.progress['value'] = 0
            self.progress.pack_forget()

        for frame_number, _ in enumerate(range(total_frames), start=1):
            success, frame = video_capture.read()
            if not success:
                break
            frame_filename = os.path.join(frames_folder_path, f'frame{frame_number}.jpg')
            cv2.imwrite(frame_filename, frame)
            self.progress['value'] = frame_number
            if frame_number % update_frequency == 0:
                self.window.update()

        video_capture.release()
        self.progress['value'] = 0
        self.progress.pack_forget()
        os.startfile(frames_folder_path)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.extract_frames(filename)

class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Frame Extraction")
        self.window.configure(padx=10, pady=10)
        self.window.minsize(260, 60)

        self.frame = tk.Frame(self.window)
        self.frame.pack(padx=10, pady=10)

        self.file_path_label = tk.Label(self.frame, text="Choose a video:")
        self.file_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.extractor = FrameExtractor(self.window)
        self.browse_button = tk.Button(self.frame, text="Browse", command=self.extractor.browse_file)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()