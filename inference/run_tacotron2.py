import os

from TTS.api import TTS

file_path = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(file_path, 'output.wav')
model_dir = os.path.join(file_path, 'tts_models--en--ljspeech--tacotron2-DCA')
vocoder_dir = os.path.join(file_path, 'vocoder_models--en--ljspeech--multiband-melgan')
tacotron2 = TTS(model_path=os.path.join(model_dir, 'model_file.pth'),
                config_path=os.path.join(model_dir, 'config.json'),
                vocoder_path=os.path.join(vocoder_dir, 'model_file.pth'),
                vocoder_config_path=os.path.join(vocoder_dir, 'config.json'),
                gpu=True)

tacotron2.tts_to_file(text="Name's Levi. Levi Ackerman", file_path=output_path)
