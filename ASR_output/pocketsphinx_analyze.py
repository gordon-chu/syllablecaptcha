from common import *
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "pocketsphinx-master\\model"
DATADIR = "audio_pcm"

arpaphone_to_IPA = {
    "AA" :	IPA.a,
    "AE" : IPA.ae,
    "AH" : IPA.uh,
    "AO" : IPA.reversec,
    "AW" : IPA.horseshoe,
    "AY" : IPA.aI,
    "B" : IPA.b,
    "CH" : IPA.ts,
    "D" : IPA.d,
    "DH" : IPA.delta,
    "EH" : IPA.epsilon,
    "ER" : IPA.reverseepsilon,
    "EY" : IPA.eI,
    "F" : IPA.f,
    "G" : IPA.g,
    "HH" : IPA.h,
    "IH" : IPA.I,
    "IY" : IPA.i,
    "JH" : IPA.d3,
    "K" : IPA.k,
    "L" : IPA.l,
    "M" : IPA.m,
    "N" : IPA.n,
    "NG" : IPA.engma,
    "OW" : IPA.horseshoe,
    "OY" : IPA.reversec,
    "P" : IPA.p,
    "R" : IPA.r,
    "S" : IPA.s,
    "SH" : IPA.esh,
    "T" : IPA.t,
    "TH" : IPA.theta,
    "UH" : IPA.horseshoe,
    "UW" : IPA.u,
    "V" : IPA.v,
    "W" : IPA.w,
    "Y" : IPA.j,
    "Z" : IPA.z,
    "ZH" : IPA.three
}

def get_transcript(question_num, decoder):
    decoder.start_utt()
    with open(path.join(DATADIR, "%d.raw" % question_num)) as stream:
        while True:
            buf = stream.read(1024)
            if buf:
                decoder.process_raw(buf, False, False)
            else:
                break
        decoder.end_utt()
    hypothesis = decoder.hyp()
    transcript = [seg.word for seg in decoder.seg() if seg.word != "SIL"]
    return [arpaphone_to_IPA[phone] for phone in transcript]

if __name__ == '__main__':
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    config.set_string('-allphone', path.join(MODELDIR, 'en-us/en-us-phone.lm.bin'))
    config.set_string('-backtrace', 'yes')
    config.set_float('-lw', 2.0)
    config.set_float('-beam', 1e-10)
    config.set_float('-pbeam', 1e-10)

    # Decode streaming data.
    decoder = Decoder(config)

    transcripts = {}
    for i in range(1, 31):
        transcripts[i] = get_transcript(i, decoder)

    correct = 0
    incorrect = 0
    for k in range (500 / 30):
        for j in range(1, 31):
            q = questions[j]
            prediction = make_prediction_phones_level(transcripts[j], q['i'], q['options'])
            if prediction == q['answer']:
                correct += 1
            else:
                incorrect += 1

    print("Correct: %d" % correct)
    print("Incorrect: %d" % incorrect)
    print("Ratio %f" % (float(correct) / (correct + incorrect)))
