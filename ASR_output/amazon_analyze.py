from common import *
import os
import json

AUDIO_DIR = "amazon_transcribe"

def get_transcript(question_num):
    filepath = os.path.join(AUDIO_DIR, "%d_asrOutput.json" % question_num)
    with open(filepath, 'r') as f:
        stuff = json.load(f)
    return stuff["results"]["transcripts"][0]["transcript"]

if __name__ == '__main__':
    transcripts = {}
    # read in JSON to get the amazon transcribe ASR outputs
    for i in range(1, 31):
        transcripts[i] = get_transcript(i)

    correct_count = 0
    incorrect_count = 0
    for k in range(500 / 30):
        for j in range(1, len(questions) + 1):
            q = questions[j]
            prediction = make_prediction_word_level_v2(transcripts[j], q['i'], q['options'])
            if prediction == q['answer']:
                correct_count += 1
            else:
                incorrect_count += 1

    print("Correct: %d" % correct_count)
    print("Incorrect: %d" % incorrect_count)
    print("Ratio %f" % (float(correct_count) / (correct_count + incorrect_count)))
