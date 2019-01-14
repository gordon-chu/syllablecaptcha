if __name__ == '__main__':
    with open('microsoft_transcribe.txt', 'r') as f:
        lines = f.readlines()

    audio_num = 1

    for i in range(len(lines)):
        if "NOMATCH" in lines[i]:
            prev_line = lines[i-1]
            transcription = prev_line.split('=')[-1]
            print("===Results for %d.wav===" % audio_num)
            print(transcription)
            audio_num += 1
