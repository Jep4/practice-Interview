import random
import cv2


def record():
    video_filename = "answer_video.mp4"

    video_capture = cv2.VideoCapture(0)
    video_format = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    out = cv2.VideoWriter(video_filename, video_format, 20.0, (frame_width, frame_height))

    print("Recording video...")
    print("Press 'q' to stop recording.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        out.write(frame)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved as {video_filename}")


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


if __name__ == "__main__":
    file_path = "q.txt"
    questions_list = read_questions_from_file(file_path)

    if questions_list:
        print("Press Enter to see next question, type record to record a video answer, type exit to end")
        while 1:
            random_question = random.choice(questions_list)
            print("Q:", random_question.strip())
            command = input("Enter to see next question...\n")

            if command == "exit":
                exit(1)

            elif command == 'record':
                record()
    else:
        print("No questions found in the file.")
