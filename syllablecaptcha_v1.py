import random
from functools import reduce

class IPA():
    p = 1
    t = 2
    k = 3
    b = 4
    d = 5
    g = 6
    f = 7
    theta = 8
    s = 9
    v = 10
    duh = 11
    z = 12
    m = 13
    n = 14
    engma = 15
    l = 16
    r = 17
    j = 18
    w = 19
    i = 20
    u = 21
    a = 22
    aa = 23

voiceless = set([IPA.p, IPA.t, IPA.k, IPA.f, IPA.theta, IPA.s])
voiced = set([IPA.b, IPA.d, IPA.g, IPA.v, IPA.duh, IPA.z])
oral_stops = set([IPA.p, IPA.t, IPA.k, IPA.b, IPA.d, IPA.g])
fricatives = set([IPA.f, IPA.theta, IPA.s, IPA.v, IPA.duh, IPA.z])
nasals = set([IPA.m, IPA.n, IPA.engma])
liquids = set([IPA.l, IPA.r])
semivowels = set([IPA.j, IPA.w])
high_vowels = set([IPA.i, IPA.u])
low_vowels = set([IPA.a, IPA.aa])
vowels = high_vowels | low_vowels

sonority_scale = [
    voiceless & oral_stops,
    voiced & oral_stops,
    voiceless & fricatives,
    voiced & fricatives,
    nasals,
    liquids,
    semivowels,
    vowels
]

def consonants_with_lesser_sonority(phoneme):
    for i in range(len(sonority_scale)):
        if phoneme in sonority_scale[i]:
            return reduce(lambda x, y : x | y, sonority_scale[:i], set()) - vowels
    return set()

def consonants_with_greater_sonority(phoneme):
    for i in range(len(sonority_scale)):
        if phoneme in sonority_scale[i]:
            return reduce(lambda x, y : x | y, sonority_scale[i+1:], set()) - vowels
    return set()

def random_sample(s):
    return random.sample(s, 1)[0]

# v1: a syllable is defined as a peak in sonority,
# with optional rise before and optional decline after
def gen_syllable():
    syllable = []
    peak = random_sample(vowels)
    length = random.randint(2, 5+1)
    # len = 2 => peak can be anywhere [1, len]
    # len = 3 => peak can be anywhere [1, len]
    # len = 4 => peak can be anywhere [2, 3]
    # len = 5 => peak must be 3
    if length == 2:
        c = random_sample(consonants_with_lesser_sonority(peak))
        syllable.append(c)
        syllable.append(peak)
        random.shuffle(syllable)
    elif length == 3:
        peak_index = random.randint(0, length)
        curr = peak
        for i in range(peak_index):
            c = random_sample(consonants_with_lesser_sonority(curr))
            syllable.append(c)
            curr = c
        syllable.reverse()
        syllable.append(peak)
        curr = peak
        for i in range(peak_index, length):
            c = random_sample(consonants_with_lesser_sonority(curr))
            syllable.append(c)
            curr = c
    elif length == 4:
        peak_index = random.randint(1, length)
        curr = peak
        for i in range(peak_index):
            c = random_sample(consonants_with_lesser_sonority(curr))
            syllable.append(c)
            curr = c
        syllable.reverse()
        syllable.append(peak)
        curr = peak
        for i in range(peak_index, length):
            c = random_sample(consonants_with_lesser_sonority(curr))
            syllable.append(c)
            curr = c
    elif length == 5:
        peak_index = 2
        curr = peak
        for i in range(peak_index):
            c = random_sample(consonants_with_lesser_sonority(curr))
            syllable.append(c)
            curr = c
        syllable.reverse()
        syllable.append(peak)
        curr = peak
        for i in range(peak_index, length):
            c = random_sample(consonants_with_lesser_sonority(curr))
            syllable.append(c)
            curr = c

    return syllable

if __name__ == '__main__':
    print(gen_syllable())
