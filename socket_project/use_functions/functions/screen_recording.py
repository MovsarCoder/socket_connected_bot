from datetime import datetime

import cv2
import pyautogui
import numpy as np
import datetime
import threading
import time



class ScreenRecorder:
    def __init__(self, output_file="screen_recorder", format_movie='mov'):
        filename = datetime.datetime.now().strftime('%Y_%m_%d___%H_%M_%S')
        self.output_file = ''.join(f'video/{output_file}_{filename}.{format_movie}')
        self.is_recording = False
        self.frames = []

    def record_screen(self):
        while self.is_recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.frames.append(frame)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            print(11111)
            recording_thread = threading.Thread(target=self.record_screen)
            recording_thread.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            print(222222222)
            time.sleep(1)
            self.save_video()

    def save_video(self):
        if self.frames:
            height, width, layers = self.frames[0].shape
            size = (width, height)
            out = cv2.VideoWriter(
                self.output_file, cv2.VideoWriter_fourcc(*"mp4v"), 10, size
            )

            for frame in self.frames:
                out.write(frame)

            out.release()
            print(f"Video saved as {self.output_file}")

# if __name__ == "__main__":
#     recording = ScreenRecorder()
#     input('start')
#     recording.start_recording()
#
#     input('stop')
#     recording.stop_recording()
