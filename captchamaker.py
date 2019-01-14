from syllablecaptcha import *
import random

def gen_captcha(num_syllables, num_options):
    word = gen_word(num_syllables)
    print(IPA.to_str(word))
    print(' | '.join(map(englishize, segment_syllables(word))))
    print(englishize(word))

    i = random.randint(1, num_syllables)
    print("What is the %d-th syllable?" % i)
    print("Alternative options: ")
    for j in range(num_options-1):
        print("\t %s" % englishize(gen_syllable()))

    print("Answer: %s" % englishize(segment_syllables(word)[i-1]))
    pass

if __name__ == '__main__':
    # 10 captchas of 3 syllables
    for i in range(10):
        gen_captcha(3 + (i / 3), 5)
    # 10 captchas of 4 syllables
    # 10 captchas of 5 syllables
