import csv

FILENAME = "Batch_3494929_batch_results.csv"
FIRST_DATA_COL = 28
LAST_DATA_COL = 1535
AGE_RANGES = ["18_27", "28_37", "38_47", "48_57", "58_67", ">68"]
GENDERS = ["female", "male", "other"]
FLUENCIES = ["basic", "conversational", "native"]
EDUCATIONS = ["grad", "undergrad", "high_school", "no_high_school"]

QUESTION_NO_TO_INDEX = {
    1 : 2,
    2 : 2,
    3 : 1,
    4 : 1,
    5 : 1,
    6 : 1,
    7 : 1,
    8 : 1,
    9 : 2,
    10 : 3,
    11 : 4,
    12 : 3,
    13 : 1,
    14 : 1,
    15 : 2,
    16 : 4,
    17 : 3,
    18 : 2,
    19 : 4,
    20 : 2,
    21 : 4,
    22 : 1,
    23 : 5,
    24 : 4,
    25 : 4,
    26 : 1,
    27 : 2,
    28 : 2,
    29 : 1,
    30 : 3
}

CORRECT_ANSWERS = {
    1 : 'fnai',
    2 : 'mro',
    3 : 'kma',
    4 : 'glee',
    5 : 'pwai',
    6 : 'vlo',
    7 : 'gwaiw',
    8 : 'in',
    9 : 'vma',
    10 : 'gral',
    11 : 'gleeg',
    12 : 'froo',
    13 : 'twai',
    14 : 'flo',
    15 : 'bloo',
    16 : 'rof',
    17 : 'too',
    18 : 'glee',
    19 : 'mwok',
    20 : 'bnoo',
    21 : 'dnee',
    22 : 'tnee',
    23 : 'gnair',
    24 : 'klur',
    25 : 'dee',
    26 : 'pre',
    27 : 'a',
    28 : 'kwa',
    29 : 'fla',
    30 : 'ee'
}

def parse_header_row(row):
    col_no_to_meaning = {}
    for i in range(FIRST_DATA_COL, LAST_DATA_COL + 1):
        text = row[i]
        fields = text.split('.')
        if fields[1] in set(AGE_RANGES) | set(GENDERS) | set(FLUENCIES) | set(EDUCATIONS):
            col_no_to_meaning[i] = fields[1]
        else: # it's a question
            col_no_to_meaning[i] = (int(fields[2]), fields[-1].split(' ')[-1])
    return col_no_to_meaning

def parse_row(row, col_no_to_meaning):
    person = {}
    person["answers"] = set()
    person["nonanswers"] = set()
    for i in range(FIRST_DATA_COL, LAST_DATA_COL + 1):
        meaning = col_no_to_meaning[i]
        if meaning in AGE_RANGES:
            if row[i].lower() == "true":
                person["age"] = meaning
        elif meaning in GENDERS:
            if row[i].lower() == "true":
                person["gender"] = meaning
        elif meaning in EDUCATIONS:
            if row[i].lower() == "true":
                person["education"] = meaning
        elif meaning in FLUENCIES:
            if row[i].lower() == "true":
                person["fluency"] = meaning
        else: # must be a question
            if row[i].strip().lower() == "true":
                person["answers"].add(meaning)
            elif row[i].strip().lower() == "false":
                person["nonanswers"].add(meaning)
    return person

def print_results_by_spanning_attribute(attribute, attribute_classes, qualified_persons):
    results_by_attribute = {}
    for attribute_class in attribute_classes:
        results_by_attribute[attribute_class] = {}
        results_by_attribute[attribute_class]["correct"] = 0
        results_by_attribute[attribute_class]["incorrect"] = 0

    for person in qualified_persons:
        for mp3_no, answer in person["answers"]:
            correct_answer = CORRECT_ANSWERS[mp3_no]
            results_by_attribute[person[attribute]]["correct"] += 1 if answer == correct_answer else 0
            results_by_attribute[person[attribute]]["incorrect"] += 0 if answer == correct_answer else 1

    print("==BY %s==" % attribute)
    for attribute_class in attribute_classes:
        no_corr = results_by_attribute[attribute_class]["correct"]
        no_incorr = results_by_attribute[attribute_class]["incorrect"]
        if no_corr + no_incorr == 0:
            continue
        print("Correct (%s): %d" % (attribute_class, no_corr))
        print("Incorrect (%s): %d" % (attribute_class, no_incorr))
        print("Ratio (%s): %f" % (attribute_class, float(no_corr) / (no_corr + no_incorr)))
        print("")

def main():
    answers = {}

    persons = []

    with open(FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                col_no_to_meaning = parse_header_row(row)
            else:
                persons.append(parse_row(row, col_no_to_meaning))
            line_count += 1

    qualified_persons = [person for person in persons if len(person["answers"]) == 5]
    print("Participants who answered 5 questions: %d" % len(qualified_persons))
    print("")

    for person in qualified_persons:
        for answer in person["answers"]:
            mp3_no = answer[0]
            syllable = answer[1]
            if mp3_no not in answers:
                answers[mp3_no] = []
            answers[mp3_no].append(syllable)


    # calculate total correct percentage
    correct = 0
    incorrect = 0
    for mp3_no in answers:
        correct_answer = CORRECT_ANSWERS[mp3_no]
        for response in answers[mp3_no]:
            if response == correct_answer:
                correct += 1
            else:
                incorrect += 1

    print("==TOTAL==")
    print("Correct: %d" % correct)
    print("Incorrect: %d" % incorrect)
    print("Ratio %f" % (float(correct) / (correct + incorrect)))
    print("")

    # calculate correct percentages based off syllable lengths
    correct_3syllable = 0
    correct_4syllable = 0
    correct_5syllable = 0
    incorrect_3syllable = 0
    incorrect_4syllable = 0
    incorrect_5syllable = 0

    for mp3_no in answers:
        correct_answer = CORRECT_ANSWERS[mp3_no]
        for response in answers[mp3_no]:
            if mp3_no in range(11):
                correct_3syllable += 1 if response == correct_answer else 0
                incorrect_3syllable += 0 if response == correct_answer else 1
            elif mp3_no in range(11, 21):
                correct_4syllable += 1 if response == correct_answer else 0
                incorrect_4syllable += 0 if response == correct_answer else 1
            elif mp3_no in range(21, 31):
                correct_5syllable += 1 if response == correct_answer else 0
                incorrect_5syllable += 0 if response == correct_answer else 1

    print("==BY SYLLABLE LENGTH==")
    print("Correct (3-syl): %d" % correct_3syllable)
    print("Incorrect (3-syl): %d" % incorrect_3syllable)
    print("Ratio (3-syl): %f" % (float(correct_3syllable) / (correct_3syllable + incorrect_3syllable)))
    print("")

    print("Correct (4-syl): %d" % correct_4syllable)
    print("Incorrect (4-syl): %d" % incorrect_4syllable)
    print("Ratio (4-syl): %f" % (float(correct_4syllable) / (correct_4syllable + incorrect_4syllable)))
    print("")

    print("Correct (5-syl): %d" % correct_5syllable)
    print("Incorrect (5-syl): %d" % incorrect_5syllable)
    print("Ratio (5-syl): %f" % (float(correct_5syllable) / (correct_5syllable + incorrect_5syllable)))
    print("")

    # TODO: look at index of syllable
    results_by_syllable_index = {}
    for mp3_no in answers:
        index = QUESTION_NO_TO_INDEX[mp3_no]
        correct_answer = CORRECT_ANSWERS[mp3_no]
        if index not in results_by_syllable_index:
            results_by_syllable_index[index] = {}
            results_by_syllable_index[index]["correct"] = 0
            results_by_syllable_index[index]["incorrect"] = 0
        for response in answers[mp3_no]:
            results_by_syllable_index[index]["correct"] += 1 if response == correct_answer else 0
            results_by_syllable_index[index]["incorrect"] += 0 if response == correct_answer else 1

    print("==BY INDEX OF SYLLABLE==")
    for i in range(1, 6):
        if i in results_by_syllable_index:
            print("Correct (index %d): %d" % (i, results_by_syllable_index[i]["correct"]))
            print("Incorrect (index %d): %d" % (i, results_by_syllable_index[i]["incorrect"]))
            print("Ratio (index %d): %f" % (i, float(results_by_syllable_index[i]["correct"]) / (results_by_syllable_index[i]["correct"] + results_by_syllable_index[i]["incorrect"])))
            print("")
    print("")

    # by GENDERS
    print_results_by_spanning_attribute("gender", GENDERS, qualified_persons)
    print("")

    # by AGE_RANGES
    print_results_by_spanning_attribute("age", AGE_RANGES, qualified_persons)
    print("")

    # by FLUENCIES
    print_results_by_spanning_attribute("fluency", FLUENCIES, qualified_persons)
    print("")

    # by EDUCATIONS
    print_results_by_spanning_attribute("education", EDUCATIONS, qualified_persons)
    print("")

if __name__ == '__main__':
    main()
