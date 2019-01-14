import random
from functools import reduce

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
    'ts' : 36
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

    @staticmethod
    def to_char(ipa_num):
        return ipa_map_inv[ipa_num]

    @staticmethod
    def to_str(ipa_nums):
        return list(map(lambda n : ipa_map_inv[n], ipa_nums))

tense_vowels = set([IPA.i, IPA.e, IPA.u, IPA.o, IPA.a])
lax_vowels = set([IPA.I, IPA.epsilon, IPA.uh, IPA.ae, IPA.horseshoe, IPA.schwa])
vowels = tense_vowels | lax_vowels
consonants = set([IPA.p, IPA.b, IPA.f, IPA.v, IPA.m, IPA.n, IPA.l, IPA.r, IPA.j, IPA.w, IPA.d, IPA.g, IPA.t, IPA.k, IPA.d3, IPA.esh, IPA.engma, IPA.theta, IPA.delta, IPA.s, IPA.three, IPA.h, IPA.x, IPA.ts]) #IPA.engma,
sonorants = set([IPA.a, IPA.e, IPA.epsilon, IPA.i, IPA.o, IPA.u, IPA.w, IPA.l, IPA.r, IPA.m, IPA.n, IPA.engma]) # IPA.engma
coronals = set([IPA.n, IPA.l, IPA.r, IPA.engma]) #IPA.engma
degree1 = set([IPA.p, IPA.b, IPA.f, IPA.v, IPA.d, IPA.g, IPA.t, IPA.k, IPA.d3, IPA.esh, IPA.theta, IPA.delta, IPA.s, IPA.three, IPA.ts, IPA.x, IPA.h])
degree2 = set([IPA.m, IPA.n, IPA.engma]) # IPA.engma
degree3 = set([IPA.l])
degree4 = set([IPA.r])
degree5 = set([IPA.j, IPA.w, IPA.i, IPA.u, IPA.I])
degree6 = set([IPA.e, IPA.o, IPA.a, IPA.epsilon, IPA.uh, IPA.ae, IPA.horseshoe, IPA.schwa])

sonority_scale = [degree1, degree2, degree3, degree4, degree5, degree6]

def get_sonority_degree(phoneme):
    for i in range(len(sonority_scale)):
        if phoneme in sonority_scale[i]:
            return i
    return -1

def gen_syllable2(prev=None):
    if prev is None:
        return gen_syllable()
    else:
        syllable = []
        peak = choose_peak2(prev[-1])
        syllable.append(peak)
        coda = choose_coda(peak)
        syllable.extend(coda)
        onset = choose_onset2(peak, prev[-1])
        onset.extend(syllable)
        return onset

def choose_peak2(prev):
    return random_sample([vowel for vowel in vowels if get_sonority_degree(vowel) >= get_sonority_degree(prev)])

def choose_onset2(peak, prev):
    onset = []
    xc_possibilities = (consonants_with_lesser_sonority(peak) & consonants_with_greater_sonority(prev) & sonorants) | set([IPA.NULL])
    xc = random_sample(xc_possibilities)
    if xc == IPA.NULL:
        return onset
    onset.append(xc)
    xb_possibilities = ((consonants_with_lesser_sonority(xc) & consonants_with_greater_sonority(prev)) - sonorants) | set([IPA.NULL])
    xb = random_sample(xb_possibilities)
    if xb == IPA.NULL:
        return onset
    onset.append(xb)
    return onset[::-1]

def gen_syllable():
    syllable = []
    peak = choose_peak()
    syllable.append(peak)
    coda = choose_coda(peak)
    syllable.extend(coda)
    onset = choose_onset(peak)
    onset.extend(syllable)
    return onset

def consonants_with_greater_sonority(phoneme):
    for i in range(len(sonority_scale)):
        if phoneme in sonority_scale[i]:
            return consonants & reduce(lambda x, y : x | y, sonority_scale[i+1:], set())
    return set()

def consonants_with_lesser_sonority(phoneme):
    for i in range(len(sonority_scale)):
        if phoneme in sonority_scale[i]:
            return consonants & reduce(lambda x, y : x | y, sonority_scale[:i], set())
    return set()

def choose_onset(peak):
    onset = []
    xc_possibilities = (consonants_with_lesser_sonority(peak) & sonorants) | set([IPA.NULL])
    xc = random_sample(xc_possibilities)
    if xc == IPA.NULL:
        return onset
    onset.append(xc)
    xb_possibilities = (consonants_with_lesser_sonority(xc) - sonorants) | set([IPA.NULL])
    xb = random_sample(xb_possibilities)
    if xb == IPA.NULL:
        return onset
    onset.append(xb)
    return onset[::-1]

def choose_coda(peak):
    coda = []
    if peak in tense_vowels: # peak = X1, X2
        x3_possibilities = consonants_with_lesser_sonority(peak) | set([IPA.NULL])
        x3 = random_sample(x3_possibilities)
        if x3 == IPA.NULL:
            return coda
        coda.append(x3)
        return coda
    else: # peak = X1
        x2_possibilities = (consonants_with_lesser_sonority(peak) & sonorants) | set([IPA.NULL])
        x2 = random_sample(x2_possibilities)
        if x2 == IPA.NULL:
            return coda
        coda.append(x2)
        x3_possibilities = (consonants_with_lesser_sonority(x2)) | set([IPA.NULL])
        x3 = random_sample(x3_possibilities)
        if x3 == IPA.NULL:
            return coda
        coda.append(x3)
        return coda

def random_sample(s):
    return random.sample(s, 1)[0]

def choose_peak():
    return random_sample(vowels)

def gen_word(k):
    word = []
    syllable = gen_syllable()
    word.extend(syllable)
    for i in range(k-1):
        syllable = gen_syllable2(syllable)
        word.extend(syllable)
    return word

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
    return segments

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

if __name__ == '__main__':
    k = 5
    word = gen_word(k)
    #word = [IPA.t, IPA.w, IPA.a, IPA.j, IPA.u, IPA.t, IPA.u, IPA.g, IPA.m, IPA.u, IPA.m]
    print(IPA.to_str(word))
    print(' | '.join(map(englishize, segment_syllables(word))))
    print(englishize(word))
    #word = [IPA.g, IPA.w, IPA.e, IPA.w, IPA.u, IPA.m, IPA.i, IPA.g]
    #print(' | '.join(map(englishize, segment_syllables(word))))

    # estimate number of possible CCVCC syllables
    count = 0
    for c1 in (consonants - sonorants):
        for c2 in (consonants & sonorants):
            for v in lax_vowels:
                    for c3 in (consonants & sonorants):
                        if get_sonority_degree(c3) < get_sonority_degree(v):
                            for c4 in consonants:
                                if get_sonority_degree(c4) < get_sonority_degree(c3):
                                    count += 1
    print("Estimation of CCVCC syllables: %d" % count)
