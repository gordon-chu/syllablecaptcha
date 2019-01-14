from common import *
import os

RESULTS_FILE = "microsoft_transcribe.processed.txt"

def get_transcripts():
    transcripts = {}
    with open(RESULTS_FILE, 'r') as f:
        linecount = 1
        questioncount = 1
        for line in f:
            if (linecount - 2) % 3 == 0:
                transcripts[questioncount] = line.strip()
                questioncount += 1
            linecount += 1
    return transcripts

if __name__ == '__main__':
    # read in processed text file to get transcripts
    transcripts = get_transcripts()

    for i in range(1, 31):
        print(transcripts[i])

    correct = 0
    incorrect = 0
    for k in range(500 / 30):
        for j in range(1, len(questions) + 1):
            q = questions[j]
            prediction = make_prediction_word_level_v2(transcripts[j], q['i'], q['options'])
            if prediction == q['answer']:
                correct += 1
            else:
                incorrect += 1

    print("Correct: %d" % correct)
    print("Incorrect: %d" % incorrect)
    print("Ratio %f" % (float(correct) / (correct + incorrect)))
