import whisper
import pyaudio
import wave
import tempfile

class ASR:
    def __init__(self):
        # Load the Whisper model if not loaded
        self.model = whisper.load_model("base.en")
        self.result = "none"

        #TODO: Be sure that this line is unnecessary
        #self.temp_file = tempfile.mkstemp(suffix='.wav', prefix='tempWav', dir='./')
        self.temp_file = r"C:\Users\mavlu\GitHub\Offline-MT-Assistant\src\temporaryWav.wav"

    def start(self):
        #Start listening mic and recording it to temporaryWav.wav file

        sample_rate = 16000
        bits_per_sample = 16
        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1

        def callback(in_data, frame_count, time_info, status):
            self.wav_file.writeframes(in_data)
            return None, pyaudio.paContinue

        # Open the wave file for writing
        self.wav_file = wave.open(self.temp_file, 'wb')
        self.wav_file.setnchannels(channels)
        self.wav_file.setsampwidth(bits_per_sample // 8)
        self.wav_file.setframerate(sample_rate)

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

        # Start recording audio
        self.stream = self.audio.open(format=audio_format,
                            channels = channels,
                            rate = sample_rate,
                            input = True,
                            frames_per_buffer = chunk_size,
                            stream_callback = callback)

    def stop(self):

        # Stop and close the audio stream
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.wav_file.close()

        transcribed = self.model.transcribe(self.temp_file, fp16=False)
        
        #TODO: Delete teporaryWav file after speech is transcribed!
        
        #Text
        return transcribed["text"].strip()