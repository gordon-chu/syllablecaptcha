import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'REPLACE WITH YOUR GCP SERVICE ACCOUNT KEY'

    client = speech.SpeechClient()

    for i in range(1, 31):
        filename = os.path.join("audio_flac", "%d.flac" % i)

        with io.open(filename, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code='en-US'
        )

        print("===Results for %d.flac===" % i)
        response = client.recognize(config, audio)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
