from common import *
import os

RESULTS_FILE = "google_transcribe.txt"

def get_transcripts():
    transcripts = {}
    with open(RESULTS_FILE, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if "===" in lines[i] and i+1 < len(lines) and "===" not in lines[i+1]:
            question_num = int(lines[i].split('.')[0].split(' ')[-1])
            transcripts[question_num] = lines[i+1].replace("Transcript: ", "").strip()
    return transcripts

if __name__ == '__main__':
    # read in processed text file to get transcripts
    transcripts = get_transcripts()

    correct = 0
    incorrect = 0
    for k in range(500 / 30):
        for j in range(1, 31):
            q = questions[j]
            prediction = make_prediction_word_level_v2(transcripts.get(j, ""), q['i'], q['options'])
            if prediction == q['answer']:
                correct += 1
            else:
                incorrect += 1

    print("Correct: %d" % correct)
    print("Incorrect: %d" % incorrect)
    print("Ratio %f" % (float(correct) / (correct + incorrect)))
