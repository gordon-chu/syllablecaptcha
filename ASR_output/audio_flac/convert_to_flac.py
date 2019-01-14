import os

if __name__ == '__main__':
    for i in range(1, 31):
        cmd = "ffmpeg.exe -y -i ..\\..\\audio\\%d.mp3 -acodec -vn -acodec flac -ar 16000 -ac 1 %d.flac"
        os.system(cmd % (i, i))
