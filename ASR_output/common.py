from syllabipy.sonoripy import SonoriPy
import random

ipa_map = {
    'p' : 1,
    'b' : 2,
    'f' : 3,
    'v' : 4,
    'm' : 5,
    'n' : 6,
    'engma' : 7,
    'l' : 8,
    'r' : 9,
    'j' : 10,
    'w' : 11,
    'i' : 12,
    'u' : 13,
    'e' : 14,
    'o' : 15,
    'a' : 16,
    'I' : 17,
    'NULL' : 18,
    'd' : 19,
    'g' : 20,
    't': 21,
    'k' : 22,
    'epsilon' : 23,
    'uh' : 24,
    'ae' : 25,
    'horseshoe' : 26,
    'schwa' : 27,
    'd3' : 28,
    'esh' : 29,
    'theta' : 30,
    'delta' : 31,
    's' : 32,
    'three' : 33,
    'h' : 34,
    'x' : 35,
    'ts' : 36,
    'aI' : 37,
    'reversec' : 38,
    'eI' : 39,
    'reverseepsilon' : 40,
    'z' : 41
}

ipa_map_inv = {v : k for k, v in ipa_map.iteritems()}

class IPA():
    p = 1
    b = 2
    f = 3
    v = 4
    m = 5
    n = 6
    engma = 7
    l = 8
    r = 9
    j = 10
    w = 11
    i = 12
    u = 13
    e = 14
    o = 15
    a = 16
    I = 17
    NULL = 18
    d = 19
    g = 20
    t = 21
    k = 22
    epsilon = 23
    uh = 24
    ae = 25
    horseshoe = 26
    schwa = 27
    d3 = 28
    esh = 29
    theta = 30
    delta = 31
    s = 32
    three = 33
    h = 34
    x = 35
    ts = 36
    aI = 37
    reversec = 38
    eI = 39
    reverseepsilon = 40
    z = 41

    @staticmethod
    def to_char(ipa_num):
        return ipa_map_inv[ipa_num]

    @staticmethod
    def to_str(ipa_nums):
        return list(map(lambda n : ipa_map_inv[n], ipa_nums))

tense_vowels = set([IPA.i, IPA.e, IPA.u, IPA.o, IPA.a])
lax_vowels = set([IPA.I, IPA.epsilon, IPA.uh]) #IPA.ae, IPA.])
vowels = tense_vowels | lax_vowels
consonants = set([IPA.p, IPA.b, IPA.f, IPA.v, IPA.m, IPA.n, IPA.l, IPA.r, IPA.j, IPA.w, IPA.d, IPA.g, IPA.t, IPA.k, IPA.z]) #IPA.engma,
sonorants = set([IPA.a, IPA.e, IPA.epsilon, IPA.i, IPA.o, IPA.u, IPA.w, IPA.l, IPA.r, IPA.m, IPA.n]) # IPA.engma
coronals = set([IPA.n, IPA.l, IPA.r]) #IPA.engma
degree1 = set([IPA.p, IPA.b, IPA.f, IPA.v, IPA.d, IPA.g, IPA.t, IPA.k, IPA.z, IPA.theta, IPA.delta, IPA.s, IPA.h, IPA.three])
degree2 = set([IPA.m, IPA.n, IPA.engma])
degree3 = set([IPA.l])
degree4 = set([IPA.r])
degree5 = set([IPA.j, IPA.w, IPA.i, IPA.u, IPA.I, IPA.schwa])
degree6 = set([IPA.e, IPA.o, IPA.a, IPA.epsilon, IPA.uh, IPA.ae, IPA.aI, IPA.reversec, IPA.eI, IPA.reverseepsilon, IPA.horseshoe])

sonority_scale = [degree1, degree2, degree3, degree4, degree5, degree6]

def get_sonority_degree(phoneme):
    for i in range(len(sonority_scale)):
        if phoneme in sonority_scale[i]:
            return i
    print(phoneme)
    assert False
    return -1

def segment_syllables(word):
    # convert each datapoint to its local sonority derivative
    sonorities = [get_sonority_degree(phone) for phone in word]
    sonority_changes = [sonorities[i + 1] - sonorities[i] for i in range(len(sonorities) - 1)]
    # a boundary is present right before a sonority trough
    # AKA wherever the local sonority change goes from negative to >= 0
    boundaries = []
    for i in range(len(sonority_changes) - 1):
        if (sonority_changes[i] <= 0 and sonority_changes[i+1] > 0) or (word[i] in vowels and word[i+1] in vowels) or (sonority_changes[i] == 0 and sonority_changes[i+1] < 0):
            boundaries.append(i)

    segments = []
    prev_bound = 0
    for i in boundaries:
        segments.append(word[prev_bound:i+1])
        prev_bound = i+1

    segments.append(word[prev_bound:])
    if len(segments) == 1 and len(segments[0]) == 0:
        return []
    return segments

blocks_to_ipa = {
    'ee' : IPA.i,
    'ai' : IPA.e,
    'oo' : IPA.u
}

exception_letter_to_ipa = {
    'y' : IPA.j,
    'i' : IPA.I,
    'e' : IPA.epsilon,
    'u' : IPA.uh
}

# inverse of englishize
def IPAize(english):
    ipa = []
    i = 0
    while i < len(english):
        # look ahead for blocks of letters
        if i + 1 < len(english):
            block = english[i:i+2]
            if block in blocks_to_ipa:
                ipa.append(blocks_to_ipa[block])
                i += 2
                continue
        if english[i] in exception_letter_to_ipa:
            ipa.append(exception_letter_to_ipa[english[i]])
        else:
            ipa.append(ipa_map[english[i]])
        i += 1
    return ipa

# takes a syllable and returns the an English spelling approximation
def englishize(syllable):
    english = []
    for ipa in syllable:
        if ipa == IPA.j:
            english.append('y')
        elif ipa == IPA.I:
            english.append('i')
        elif ipa == IPA.i:
            english.append('ee')
        elif ipa == IPA.e:
            english.append('ai')
        elif ipa == IPA.u:
            english.append('oo')
        elif ipa == IPA.epsilon:
            english.append('e')
        elif ipa == IPA.uh:
            english.append('u')
        else:
            english.append(IPA.to_char(ipa))
    return ''.join(english)

def test(english):
    ipa = IPAize(english)
    verify_english = englishize(ipa)

    print("%s : %s : %s" % (english, ipa, verify_english))

def test_edit_distance(ipa1, ipa2):
    print(ipa1)
    print(ipa2)
    print("edit distance: %d" % edit_distance(ipa1, ipa2))

# copied from https://www.python-course.eu/levenshtein_distance.php
def edit_distance(s, t, costs=(1,1,1)):
    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + cost) # substitution
    return dist[row][col]

def segment(asr_output):
    words = asr_output.replace(',', '').replace('.', '').replace(';', '').replace('-', '').split(' ')
    segmentation = []
    for word in words:
        segments = SonoriPy(word.lower())
        # fix any apostrophe hoopla e.g. (1) they, (2) 're => (1) they're
        temp = []
        for segment in segments:
            if segment[0] == "'":
                temp[-1] = temp[-1] + segment
            else:
                temp.append(segment)
        segmentation.extend(temp)
    return [str(segment) for segment in segmentation]

to_phonetics_map = {
    "Plouffe Neff Loon." : [IPA.p, IPA.l, IPA.o, IPA.horseshoe, IPA.f, IPA.n, IPA.epsilon, IPA.f, IPA.l, IPA.u, IPA.n],
    "Remember Layla?" : [IPA.r, IPA.I, IPA.m, IPA.epsilon, IPA.m, IPA.b, IPA.schwa, IPA.r, IPA.l, IPA.ae, IPA.j, IPA.l, IPA.uh],
    "Come on, Luke met." : [IPA.k, IPA.uh, IPA.m, IPA.a, IPA.n, IPA.l, IPA.u, IPA.k, IPA.m, IPA.epsilon, IPA.t],
    "Click right." : [IPA.k, IPA.l, IPA.I, IPA.k, IPA.r, IPA.aI, IPA.t],
    "Point grand Geet." : [IPA.p, IPA.reversec, IPA.I, IPA.n, IPA.t, IPA.g, IPA.ae, IPA.n, IPA.d, IPA.g, IPA.i, IPA.t],
    "Good little knob." : [IPA.g, IPA.horseshoe, IPA.d, IPA.l, IPA.I, IPA.t, IPA.schwa, IPA.l, IPA.n, IPA.a, IPA.b],
    "Quay we make." : [IPA.k, IPA.i, IPA.w, IPA.i, IPA.m, IPA.eI, IPA.k],
    "Ended me." : [IPA.epsilon, IPA.n, IPA.d, IPA.schwa, IPA.d, IPA.m, IPA.i],
    "Ruth Murray." : [IPA.r, IPA.u, IPA.theta, IPA.m, IPA.reverseepsilon, IPA.r, IPA.i],
    "Flynn will girl." : [IPA.f, IPA.l, IPA.I, IPA.n, IPA.w, IPA.I, IPA.l, IPA.g, IPA.reverseepsilon, IPA.r, IPA.l],
    "Ealier food, Blake." : [IPA.i, IPA.l, IPA.schwa, IPA.r, IPA.f, IPA.u, IPA.d, IPA.b, IPA.l, IPA.eI, IPA.k],
    "Nail rare fruit noir." : [IPA.n, IPA.eI, IPA.l, IPA.r, IPA.epsilon, IPA.r, IPA.f, IPA.r, IPA.u, IPA.t, IPA.n, IPA.reversec, IPA.I, IPA.r],
    "Toya lukewarm." : [IPA.t, IPA.reversec, IPA.I, IPA.schwa, IPA.l, IPA.u, IPA.k, IPA.w, IPA.reversec, IPA.r, IPA.m],
    "With Lynn Mary." : [IPA.w, IPA.I, IPA.delta, IPA.l, IPA.I, IPA.n, IPA.m, IPA.epsilon, IPA.r, IPA.i],
    "Drink." : [IPA.d, IPA.r, IPA.I, IPA.engma, IPA.k],
    "Plant Marine War of" : [IPA.p, IPA.l, IPA.ae, IPA.n, IPA.t, IPA.m, IPA.schwa, IPA.r, IPA.i, IPA.n, IPA.w, IPA.reversec, IPA.r, IPA.uh, IPA.v],
    "Twice you tick, Ma'am." : [IPA.t, IPA.w, IPA.aI, IPA.s, IPA.j, IPA.u, IPA.t, IPA.I, IPA.k, IPA.m, IPA.ae, IPA.m],
    "Verbally lair pig." : [IPA.v, IPA.schwa, IPA.r, IPA.b, IPA.ae, IPA.l, IPA.i, IPA.l, IPA.epsilon, IPA.r, IPA.p, IPA.I, IPA.g],
    "Hardware on look." : [IPA.h, IPA.a, IPA.r, IPA.d, IPA.w, IPA.epsilon, IPA.r, IPA.a, IPA.n, IPA.l, IPA.horseshoe, IPA.k],
    "Opening your own meal." : [IPA.o, IPA.horseshoe, IPA.p, IPA.schwa, IPA.n, IPA.I, IPA.engma, IPA.j, IPA.horseshoe, IPA.schwa, IPA.r, IPA.o, IPA.horseshoe, IPA.n, IPA.m, IPA.i, IPA.l],
    "Neck movement mean wass." : [IPA.n, IPA.epsilon, IPA.k, IPA.m, IPA.u, IPA.v, IPA.m, IPA.schwa, IPA.n, IPA.t, IPA.m, IPA.i, IPA.n, IPA.w, IPA.uh, IPA.s],
    "Name, rank and file." : [IPA.n, IPA.eI, IPA.m, IPA.r, IPA.ae, IPA.engma, IPA.k, IPA.ae, IPA.n, IPA.d, IPA.f, IPA.aI, IPA.l],
    "No non worry drug Nair." : [IPA.n, IPA.o, IPA.horseshoe, IPA.n, IPA.a, IPA.n, IPA.w, IPA.reverseepsilon, IPA.r, IPA.i, IPA.d, IPA.r, IPA.uh, IPA.g, IPA.n, IPA.epsilon, IPA.r],
    "Trib. Roy Collateral Ron." : [IPA.t, IPA.r, IPA.I, IPA.b, IPA.r, IPA.reversec, IPA.I, IPA.k, IPA.schwa, IPA.l, IPA.ae, IPA.t, IPA.schwa, IPA.r, IPA.schwa, IPA.l, IPA.r, IPA.a, IPA.n],
    "Maron Multi black." : [IPA.m, IPA.a, IPA.r, IPA.reversec, IPA.n, IPA.m, IPA.uh, IPA.l, IPA.t, IPA.i, IPA.b, IPA.l, IPA.ae, IPA.k],
    "Printer Weld montage." : [IPA.p, IPA.r, IPA.I, IPA.n, IPA.t, IPA.schwa, IPA.r, IPA.w, IPA.epsilon, IPA.l, IPA.d, IPA.m, IPA.a, IPA.n, IPA.t, IPA.a, IPA.three],
    "Free. Ah, guten praise." : [IPA.f, IPA.r, IPA.i, IPA.a, IPA.g, IPA.u, IPA.t, IPA.e, IPA.n, IPA.p, IPA.r, IPA.eI, IPA.z],
    "Can acquire one movement." : [IPA.k, IPA.ae, IPA.n, IPA.schwa, IPA.k, IPA.w, IPA.aI, IPA.schwa, IPA.r, IPA.w, IPA.uh, IPA.n, IPA.m, IPA.u, IPA.v, IPA.m, IPA.schwa, IPA.n, IPA.t],
    "Fly away. Fourth, Doug." : [IPA.f, IPA.l, IPA.aI, IPA.schwa, IPA.w, IPA.eI, IPA.f, IPA.reversec, IPA.r, IPA.theta, IPA.d, IPA.uh, IPA.g],
    "Mere flavors blend." : [IPA.m, IPA.i, IPA.r, IPA.f, IPA.l, IPA.eI, IPA.v, IPA.schwa, IPA.r, IPA.z, IPA.b, IPA.l, IPA.epsilon, IPA.n, IPA.d],
    "Postnet alone." : [IPA.p, IPA.o, IPA.s, IPA.t, IPA.n, IPA.e, IPA.t, IPA.schwa, IPA.l, IPA.o, IPA.horseshoe, IPA.n],
    "Drum roll out." : [IPA.d, IPA.r, IPA.uh, IPA.m, IPA.r, IPA.o, IPA.horseshoe, IPA.l, IPA.a, IPA.horseshoe, IPA.t],
    "Come on Luke met." : [IPA.k, IPA.uh, IPA.m, IPA.o, IPA.n, IPA.l, IPA.u, IPA.k, IPA.m, IPA.epsilon, IPA.t],
    "Click radio." : [IPA.k, IPA.l, IPA.i, IPA.k, IPA.r, IPA.eI, IPA.d, IPA.i, IPA.o, IPA.horseshoe],
    "Quite Granby." : [IPA.k, IPA.w, IPA.aI, IPA.t, IPA.g, IPA.r, IPA.a, IPA.n, IPA.b, IPA.i], # need to take into account y -> IPA.i mapping on top of tophonetics here
    "God little mouth." : [IPA.g, IPA.a, IPA.d, IPA.l, IPA.I, IPA.t, IPA.schwa, IPA.l, IPA.m, IPA.a, IPA.horseshoe, IPA.theta],
    "Way we make." : [IPA.w, IPA.eI, IPA.w, IPA.i, IPA.m, IPA.eI, IPA.k],
    "Indent mean" : [IPA.I, IPA.n, IPA.d, IPA.epsilon, IPA.n, IPA.t, IPA.m, IPA.i, IPA.n],
    "Ruth Marie." : [IPA.r, IPA.u, IPA.theta, IPA.m, IPA.m, IPA.schwa, IPA.r, IPA.i],
    "Glenwood girl." : [IPA.g, IPA.l, IPA.epsilon, IPA.n, IPA.w, IPA.horseshoe, IPA.d, IPA.g, IPA.reverseepsilon, IPA.r, IPA.l],
    "Elier food Lake." : [IPA.epsilon, IPA.l, IPA.I, IPA.schwa, IPA.r, IPA.f, IPA.u, IPA.d, IPA.l, IPA.eI, IPA.k],
    "Now rare fruit noir." : [IPA.n, IPA.a, IPA.horseshoe, IPA.r, IPA.epsilon, IPA.r, IPA.f, IPA.r, IPA.u, IPA.t, IPA.n, IPA.reversec, IPA.I, IPA.r],
    "Toyota Gore," : [IPA.t, IPA.o, IPA.horseshoe, IPA.j, IPA.o, IPA.horseshoe, IPA.t, IPA.schwa, IPA.g, IPA.reversec, IPA.r],
    "What's luminary?" : [IPA.w, IPA.uh, IPA.t, IPA.s, IPA.l, IPA.u, IPA.m, IPA.schwa, IPA.n, IPA.epsilon, IPA.r, IPA.i],
    "Trend Laferrari." : [IPA.t, IPA.r, IPA.epsilon, IPA.n, IPA.d, IPA.l, IPA.a, IPA.f, IPA.e, IPA.r, IPA.r, IPA.a, IPA.r, IPA.i],
    "Plum Rain War of." : [IPA.p, IPA.l, IPA.uh, IPA.m, IPA.r, IPA.eI, IPA.n, IPA.w, IPA.reversec, IPA.r, IPA.uh, IPA.v],
    "Try YouTube moon." : [IPA.t, IPA.r, IPA.aI, IPA.i, IPA.o, IPA.u, IPA.t, IPA.u, IPA.b, IPA.e, IPA.m, IPA.u, IPA.n],
    "Brimley lair poop?" : [IPA.b, IPA.r, IPA.i, IPA.m, IPA.l, IPA.e, IPA.e, IPA.l, IPA.epsilon, IPA.r, IPA.p, IPA.u, IPA.p],
    "Hardware mug." : [IPA.h, IPA.a, IPA.r, IPA.d, IPA.d, IPA.epsilon, IPA.r, IPA.m, IPA.uh, IPA.g],
    "Open Uber on meal." : [IPA.o, IPA.horseshoe, IPA.p, IPA.schwa, IPA.p, IPA.schwa, IPA.n, IPA.j, IPA.u, IPA.b, IPA.schwa, IPA.r, IPA.a, IPA.n, IPA.m, IPA.i, IPA.l],
    "Make note meant mean Wolf." : [IPA.m, IPA.eI, IPA.k, IPA.n, IPA.o, IPA.horseshoe, IPA.t, IPA.m, IPA.epsilon, IPA.n, IPA.t, IPA.m, IPA.i, IPA.n, IPA.w, IPA.horseshoe, IPA.l, IPA.f],
    "Name rock'n' blah blah." : [IPA.n, IPA.eI, IPA.m, IPA.r, IPA.o, IPA.k, IPA.k, IPA.n, IPA.b, IPA.l, IPA.a, IPA.b, IPA.l, IPA.a], # need to take into account c -> IPA.k mapping
    "Milk Nonwords Ragnarr." : [IPA.m, IPA.I, IPA.l, IPA.k, IPA.n, IPA.o, IPA.n, IPA.w, IPA.o, IPA.r, IPA.d, IPA.s, IPA.r, IPA.a, IPA.g, IPA.n, IPA.a, IPA.r, IPA.r],
    "Troll broad Klatt Real Rob." : [IPA.t, IPA.r, IPA.o, IPA.horseshoe, IPA.l, IPA.b, IPA.r, IPA.reversec, IPA.d, IPA.k, IPA.l, IPA.ae, IPA.t, IPA.b, IPA.l, IPA.ae, IPA.k],
    "Maryland multi black." : [IPA.m, IPA.epsilon, IPA.r, IPA.schwa, IPA.l, IPA.schwa, IPA.n, IPA.d, IPA.m, IPA.uh, IPA.l, IPA.t, IPA.i, IPA.b, IPA.l, IPA.ae, IPA.k],
    "Printer Weldment Offen." : [IPA.p, IPA.r, IPA.I, IPA.n, IPA.t, IPA.schwa, IPA.r, IPA.w, IPA.epsilon, IPA.l, IPA.d, IPA.m, IPA.schwa, IPA.n, IPA.t, IPA.reversec, IPA.f, IPA.schwa, IPA.n],
    "Priya goo praise." : [IPA.p, IPA.r, IPA.i, IPA.i, IPA.a, IPA.g, IPA.u, IPA.p, IPA.r, IPA.eI, IPA.z],
    "Connect wire when Rove met." : [IPA.k, IPA.schwa, IPA.n, IPA.epsilon, IPA.k, IPA.t, IPA.w, IPA.aI, IPA.schwa, IPA.r, IPA.w, IPA.epsilon, IPA.n, IPA.r, IPA.o, IPA.horseshoe, IPA.v, IPA.m, IPA.epsilon, IPA.t],
    "Fly Away Fourth Nog." : [IPA.f, IPA.l, IPA.aI, IPA.schwa, IPA.w, IPA.eI, IPA.f, IPA.reversec, IPA.r, IPA.theta, IPA.n, IPA.o, IPA.g],
    "Mere Fleegle Room land." : [IPA.m, IPA.I, IPA.r, IPA.f, IPA.l, IPA.e, IPA.e, IPA.g, IPA.l, IPA.e, IPA.r, IPA.u, IPA.m, IPA.l, IPA.ae, IPA.n, IPA.d],
    "clique" : [IPA.k, IPA.l, IPA.i, IPA.k],
    "Moby black" : [IPA.m, IPA.o, IPA.horseshoe, IPA.b, IPA.i, IPA.b, IPA.l, IPA.ae, IPA.k]
}

def to_phonetics_syllable_to_ipa(text):
    # to_phonetics does not have an API
    # so instead of writing code that scrapes the website,
    # we manually entered the translations we needed
    # but a scraper could be written to automate this step
    # note that sometimes the website does not return a phonetic transcription
    # for cases with proper names like Brimley. In this case we map 1 to 1
    # really crudely, so each letter gets a phone. Since IPA.y does not exist,
    # we choose to put in IPA.i (y is usually either IPA.i, IPA.j, IPA.eI)
    if text == "a":
        return [IPA.a]
    elif text == "they're":
        return [IPA.delta, IPA.epsilon, IPA.r]
    else:
        return to_phonetics_map[text]

# makes a prediction based on word-level output
# syllabify at English spelling level
def make_prediction_word_level(asr_output, index, options):
    # segment asr_output into syllables
    segmentation = segment(asr_output)

    # find the i-th syllable in the segmented output
    if index > len(segmentation): # need to guess randomly if segmentation fails
        return options[random.randint(0, len(options) - 1)]

    indexed_syllable = segmentation[index - 1]

    # convert i-th syllable to ipa (use: https://tophonetics.com/)
    ipa_indexed_syllable = to_phonetics_syllable_to_ipa(indexed_syllable)

    # convert options to IPA
    ipa_options = [IPAize(option) for option in options]
    random.shuffle(ipa_options) # to tie break randomly on same edit distance

    # return min edit distance option
    min_edit_dist = 999999
    min_edit_option = -1
    for ipa_option in ipa_options:
        dist = edit_distance(ipa_indexed_syllable, ipa_option)
        if dist < min_edit_dist:
            min_edit_dist = dist
            min_edit_option = ipa_option

    return englishize(min_edit_option)

# makes a prediction based on word-level output
# syllabify at IPA level
def make_prediction_word_level_v2(asr_output, index, options):
    # segment asr_output into syllables
    ipa_word = to_phonetics_syllable_to_ipa(asr_output) if asr_output else []
    ipa_segmentation = segment_syllables(ipa_word)

    # find the i-th syllable in the segmented output
    if index > len(ipa_segmentation): # need to guess randomly if segmentation fails
        return options[random.randint(0, len(options) - 1)]

    ipa_indexed_syllable = ipa_segmentation[index - 1]

    # convert options to IPA
    ipa_options = [IPAize(option) for option in options]
    random.shuffle(ipa_options) # to tie break randomly on same edit distance

    # return min edit distance option
    min_edit_dist = 999999
    min_edit_option = -1
    for ipa_option in ipa_options:
        dist = edit_distance(ipa_indexed_syllable, ipa_option)
        if dist < min_edit_dist:
            min_edit_dist = dist
            min_edit_option = ipa_option

    return englishize(min_edit_option)

# makes a prediction based on phoneme-level output
def make_prediction_phones_level(asr_output_phones, index, options):
    # segment asr_output into syllables
    ipa_word = asr_output_phones
    ipa_segmentation = segment_syllables(ipa_word)

    # find the i-th syllable in the segmented output
    if index > len(ipa_segmentation): # need to guess randomly if segmentation fails
        return options[random.randint(0, len(options) - 1)]

    ipa_indexed_syllable = ipa_segmentation[index - 1]

    # convert options to IPA
    ipa_options = [IPAize(option) for option in options]
    random.shuffle(ipa_options) # to tie break randomly on same edit distance

    # return min edit distance option
    min_edit_dist = 999999
    min_edit_option = -1
    for ipa_option in ipa_options:
        dist = edit_distance(ipa_indexed_syllable, ipa_option)
        if dist < min_edit_dist:
            min_edit_dist = dist
            min_edit_option = ipa_option

    return englishize(min_edit_option)

q1 = {
    'i' : 2,
    'mp3_url' : '1.mp3',
    'options' : ['gnaib', 'trood', 'bneem', 'ent', 'fnai'],
    'answer' : 'fnai'
};

q2 = {
	'i' : 2,
	'mp3_url' : '2.mp3',
	'options' : ['prad', 'ploom', 'bnirg', 'knuwf', 'mro'],
	'answer' : 'mro'
};
q3 = {
	'i' : 1,
	'mp3_url' : '3.mp3',
	'options' : ['pmumg', 'rol', 'vroo', 'vreld', 'kma'],
	'answer' : 'kma'
};
q4 = {
	'i' : 1,
	'mp3_url' : '4.mp3',
	'options' : ['kmaif', 'aid', 'vroob', 'low', 'glee'],
	'answer' : 'glee'
};
q5 = {
	'i' : 1,
	'mp3_url' : '5.mp3',
	'options' : ['pnult', 'aim', 'bloon', 'og', 'pwai'],
	'answer' : 'pwai'
};
q6 = {
	'i' : 1,
	'mp3_url' : '6.mp3',
	'options' : ['vnool', 'kwerb', 'dmilv', 'pmeek', 'vlo'],
	'answer' : 'vlo'
};
q7 = {
	'i' : 1,
	'mp3_url' : '7.mp3',
	'options' : ['gloor', 'raiy', 'aiw', 'trag', 'gwaiw'],
	'answer' : 'gwaiw'
};
q8 = {
	'i' : 1,
	'mp3_url' : '8.mp3',
	'options' : ['dleel', 'oor', 'mer', 'ook', 'in'],
	'answer' : 'in'
};
q9 = {
	'i' : 2,
	'mp3_url' : '9.mp3',
	'options' : ['oot', 'vrinp', 'vwam', 'knaiy', 'vma'],
	'answer' : 'vma'
};
q10 = {
	'i' : 3,
	'mp3_url' : '10.mp3',
	'options' : ['trinv', 'klot', 'vmaiw', 'ran', 'gral'],
	'answer' : 'gral'
};
q11 = {
	'i' : 4,
	'mp3_url' : '11.mp3',
	'options' : ['naf', 'flemg', 'frag', 'vreem', 'gleeg'],
	'answer' : 'gleeg'
};
q12 = {
	'i' : 3,
	'mp3_url' : '12.mp3',
	'options' : ['gmaig', 'tmemt', 'vwaig', 'vnelm', 'froo'],
	'answer' : 'froo'
};
q13 = {
	'i' : 1,
	'mp3_url' : '13.mp3',
	'options' : ['free', 'vrood', 'pwert', 'krelk', 'twai'],
	'answer' : 'twai'
};
q14 = {
	'i' : 2,
	'mp3_url' : '14.mp3',
	'options' : ['urf', 'blow', 'dmai', 'ool', 'flo'],
	'answer' : 'flo'
};
q15 = {
	'i' : 2,
	'mp3_url' : '15.mp3',
	'options' : ['u', 'gmool', 'brok', 'nuwm', 'bloo'],
	'answer' : 'bloo'
};
q16 = {
	'i' : 4,
	'mp3_url' : '16.mp3',
	'options' : ['oog', 'fnaif', 'bmom', 'gnan', 'rof'],
	'answer' : 'rof'
};
q17 = {
	'i' : 3,
	'mp3_url' : '17.mp3',
	'options' : ['gnail', 'knimd', 'fnof', 'fnaiy', 'too'],
	'answer' : 'too'
};
q18 = {
	'i' : 2,
	'mp3_url' : '18.mp3',
	'options' : ['pmaim', 'vrat', 'twenf', 'pwan', 'glee'],
	'answer' : 'glee'
};
q19 = {
	'i' : 4,
	'mp3_url' : '19.mp3',
	'options' : ['tlew', 'fror', 'dreeb', 'trap', 'mwok'],
	'answer' : 'mwok'
};
q20 = {
	'i' : 2,
	'mp3_url' : '20.mp3',
	'options' : ['ni', 'fwenp', 'vlumb', 'trirt', 'bnoo'],
	'answer' : 'bnoo'
};

q21 = {
	'i' : 4,
	'mp3_url' : '21.mp3',
	'options' : ['pnumd', 'fnop', 'dnool', 'url', 'dnee'],
	'answer' : 'dnee'
};
q22 = {
	'i' : 1,
	'mp3_url' : '22.mp3',
	'options' : ['knemp', 'blan', 'proor', 'pro', 'tnee'],
	'answer' : 'tnee'
};
q23 = {
	'i' : 5,
	'mp3_url' : '23.mp3',
	'options' : ['fwer', 'traid', 'el', 'maw', 'gnair'],
	'answer' : 'gnair'
};
q24 = {
	'i' : 4,
	'mp3_url' : '24.mp3',
	'options' : ['vnood', 'prain', 'frinf', 'pneef', 'klur'],
	'answer' : 'klur'
};
q25 = {
	'i' : 4,
	'mp3_url' : '25.mp3',
	'options' : ['eem', 'enp', 'gwaip', 'aiw', 'dee'],
	'answer' : 'dee'
};
q26 = {
	'i' : 1,
	'mp3_url' : '26.mp3',
	'options' : ['aw', 'trod', 'kwal', 'luwb', 'pre'],
	'answer' : 'pre'
};
q27 = {
	'i' : 2,
	'mp3_url' : '27.mp3',
	'options' : ['frulf', 'fleep', 'vrirp', 'ern', 'a'],
	'answer' : 'a'
};
q28 = {
	'i' : 2,
	'mp3_url' : '28.mp3',
	'options' : ['aim', 'aip', 'glult', 'irn', 'kwa'],
	'answer' : 'kwa'
};
q29 = {
	'i' : 1,
	'mp3_url' : '29.mp3',
	'options' : ['fmeer', 'tmeel', 'fwaid', 'bmeep', 'fla'],
	'answer' : 'fla'
};
q30 = {
	'i' : 3,
	'mp3_url' : '30.mp3',
	'options' : ['klir', 'tmurd', 'tlot', 'gnair', 'ee'],
	'answer' : 'ee'
};

qs = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]
questions = {i+1 : qs[i] for i in range(len(qs))}
