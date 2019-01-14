import os

if __name__ == '__main__':
    for i in range(1, 31):
        cmd = "ffmpeg.exe -i ..\\..\\audio\\%d.mp3 %d.wav"
        os.system(cmd % (i, i))
