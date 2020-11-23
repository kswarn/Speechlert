import pyaudio
import wave
import time
import threading
import winsound
import speech_recognition as sr
from datetime import datetime
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

r = sr.Recognizer()


def record():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start recording")

    frames = []
    prev_len = 0
    prev_sec = 0
    try:
        a = datetime.now()
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if (datetime.now() - a).seconds % 5 == 0 and (datetime.now() - a).seconds != prev_sec:
                prev_sec = (datetime.now() - a).seconds
                yield frames[prev_len:], p.get_sample_size(FORMAT)
                prev_len = len(frames)
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))

    sample_width = p.get_sample_size(FORMAT)

    stream.stop_stream()
    stream.close()
    p.terminate()


def get_chunks():
    file_counter = 0
    for frames, sample_width in record():
        wf = wave.open(f"recording/{file_counter}.wav", 'wb')
        wf.setnchannels(CHANNELS)
        # sample_width, frames = record()
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        file_counter += 1


def processing():
    chunk_number = 0
    while True:
        if not os.path.exists(f'recording/{chunk_number}.wav'):
            time.sleep(2)
            continue
        AUDIO_FILE = f"recording/{chunk_number}.wav"
        with sr.AudioFile(AUDIO_FILE) as source:
            audio_listened = r.listen(source)
        try:
            rec = r.recognize_google(audio_listened)

            # If recognized, write into the file.
            matching(rec)

        # If google could not understand the audio
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results.")
        chunk_number += 1


def matching(rec):
    pattern = "attendance"
    if pattern in rec:
        winsound.PlaySound("beep-06.wav", winsound.SND_FILENAME)


if __name__ == '__main__':
    t1 = threading.Thread(target=get_chunks)
    t2 = threading.Thread(target=processing)
    t1.start()
    t2.start()

    t1.join()
    t2.join()
