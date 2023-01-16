import whisper
import soundcard as sc
import threading
import queue
import numpy as np
import argparse

class LoopbackWhisperModule:
    """
    Streaming Speech Recognition with Whisper and Soundcard
    """

    def __init__(self) -> None:
        self.SAMPLE_RATE = 16000
        self.INTERVAL = 3
        self.BUFFER_SIZE = 8192

        parser = argparse.ArgumentParser()
        parser.add_argument('--model', default='medium')
        args = parser.parse_args()

        print('Loading model...')
        self.model = whisper.load_model(args.model)
        print('Done')

        self.q = queue.Queue()
        self.b = np.ones(100) / 100

        self.options = whisper.DecodingOptions(language='Japanese')

        self.th_recognize = threading.Thread(target=self.recognize, daemon=True)
        self.th_recognize.start()

    def recognize(self):
        while True:
            audio = self.q.get()
            if (audio ** 2).max() > 0.001:
                audio = whisper.pad_or_trim(audio)

                # make log-Mel spectrogram and move to the same device as the model
                mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

                # decode the audio
                result = whisper.decode(self.model, mel, self.options)

                print(f'Ja: {result.text}')

    def loop(self):
        # start recording
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.SAMPLE_RATE, channels=1) as mic:
            audio = np.empty(self.SAMPLE_RATE * self.INTERVAL + self.BUFFER_SIZE, dtype=np.float32)
            n = 0
            while True:
                while n < self.SAMPLE_RATE * self.INTERVAL:
                    data = mic.record(self.BUFFER_SIZE)
                    audio[n:n+len(data)] = data.reshape(-1)
                    n += len(data)

                # find silent periods
                m = n * 4 // 5
                vol = np.convolve(audio[m:n] ** 2, self.b, 'same')
                m += vol.argmin()
                self.q.put(audio[:m])

                audio_prev = audio
                audio = np.empty(self.SAMPLE_RATE * self.INTERVAL + self.BUFFER_SIZE, dtype=np.float32)
                audio[:n-m] = audio_prev[m:n]
                n = n-m