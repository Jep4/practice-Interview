import random

import random
import PIL
import cv2
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import time
from tkinter import simpledialog
import os



def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def update_time():
    current_time = time.time()
    time_spent = format_time(current_time - start_time)

    time_label.config(text="Time Spent: " + time_spent)
    root.after(1000, update_time)


def record():

    if not os.path.exists("video"):
        os.makedirs("video")

    video_title = datetime.now().strftime("%m%d%Y_%H%M%S")
    video_filename = f"video/{video_title}.mp4"
    video_capture = cv2.VideoCapture(0)
    video_format = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    out = cv2.VideoWriter(video_filename, video_format, 20.0, (frame_width, frame_height))
    start_time = time.time()

    messagebox.showinfo(title="info", message="press q to end the recording")
    canvas.pack()
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        out.write(frame)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            end_time = time.time()
            time_spent = end_time - start_time

            messagebox.showinfo("info", f"Time Spent: {format_time(time_spent)}")

            messagebox.showinfo(title="info", message="file saved")
            break
    video_capture.release()
    cv2.waitKey(500)
    out.release()
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    cv2.waitKey(500)


def read_questions_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            questions = file.readlines()
            return questions
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def update_video_label():
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (600, 480))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo
    canvas.after(10, update_video_label)


def random_question():
    rand_q = random.choice(questions_list)
    question_label.config(text="Q:" + rand_q.strip())


if __name__ == "__main__":
    file_path = "q.txt"
    questions_list = read_questions_from_file(file_path)

    root = tk.Tk()
    root.title("Interview Practice")
    root.geometry("900x700")

    canvas = tk.Canvas(root, width=600, height=480)
    canvas.pack()

    start_time = time.time()

    video_frame = ttk.Frame(root, width=600, height=480)
    video_frame.pack(side=tk.LEFT)

    video_label = tk.Label(video_frame)
    video_label.pack()
    video_capture = cv2.VideoCapture(0)
    update_video_label()

    time_label = tk.Label(root, text="Time Spent: 00:00:00", font=("Arial", 12), fg="white", bg="#333333")
    time_label.pack(pady=5)

    question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=600)
    question_label.pack(padx=20, pady=10)

    show_question_button = tk.Button(root, text="Show Random Question", font=("Arial", 14), command=random_question)
    show_question_button.pack(pady=5)

    record_video_button = tk.Button(root, text="Record Video", command=record)
    record_video_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    random_question()
    update_time()
    root.mainloop()
