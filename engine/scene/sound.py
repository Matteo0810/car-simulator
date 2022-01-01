import time
import wave
from enum import Enum
from threading import Thread
from pyaudio import PyAudio, paContinue


class SoundStatus(Enum):
    PLAY = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3


class Sound:

    def __init__(self, file: str):
        self._file = wave.open(file, 'rb')
        self._audio = PyAudio()
        self._stream = self._audio.open(
            format=self._audio.get_format_from_width(self._file.getsampwidth()),
            channels=self._file.getnchannels(),
            rate=self._file.getframerate(),
            output=True,
            stream_callback=self._stream_callback
        )
        self._stopped = False

    def set_state(self, state: SoundStatus):
        if state == SoundStatus.PLAY:
            Thread(target=self._play).start()
        elif state == SoundStatus.PAUSE:
            self.stopped(True)
            self._pause()
        elif state == SoundStatus.RESUME:
            Thread(target=self._play).start()
        elif state == SoundStatus.STOP:
            self.stopped(True)
            self._stop()

    def _play(self):
        self.stopped(False)
        self._stream.start_stream()
        while self._stream.is_active():
            time.sleep(0.1)

    def _pause(self):
        self._stream.stop_stream()
        self._stream.close()

    def _stop(self):
        self._audio.terminate()

    def stopped(self, stopped: bool):
        self._stopped = stopped

    def _stream_callback(self, in_data, frame_count, time_info, status):
        data = self._file.readframes(frame_count)
        return data, paContinue

    def _get_data(self):
        return self._file.readframes(1024)
