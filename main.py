import cv2
import os
from tkinter.filedialog import askopenfilename
import pygame as pg
import time
import moviepy
import sys
import cProfile
import tqdm

video_path = askopenfilename(filetypes=[("Video Files", ["*.mp4", "*.avi"])])

video = moviepy.VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile("./temp.mp3")
video.close()
audio.close()

video = cv2.VideoCapture(video_path)
video_width, video_height = os.get_terminal_size()
delta = 1/video.get(cv2.CAP_PROP_FPS)

chars = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def pixel2ascii(pixel):
    return chars[int((pixel/255)*(len(chars)-1))]

def frame2ascii(frame):
    frame = cv2.resize(frame, (video_width, video_height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_str = "".join("".join(pixel2ascii(pixel) for pixel in row) for row in frame)
    return frame_str

ascii_frames = []

total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

pbar = tqdm.tqdm(total=int(total_frames), desc="Converting video to ASCII frames")

while True:
    start = time.time()
    ret, frame = video.read()
    if not ret:
        break
    ascii_frames.append(frame2ascii(frame))
    pbar.update(1)
video.release()

pg.mixer.init()
pg.mixer.music.load("./temp.mp3")
pg.mixer.music.play()

while True:
    if not pg.mixer.music.get_busy():
        break
    sys.stdout.write("\033[H")
    sys.stdout.write(ascii_frames[int((pg.mixer.music.get_pos()/1000)//delta)])
    sys.stdout.flush()

os.remove("./temp.mp3")