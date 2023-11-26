from TTS.api import TTS
from pathlib import Path


apis = {
    
}
def tts(text, tts_model, speaker, speaker_wav, language, device, out_path, speed=1.0):
    global apis
    
    if isinstance(speaker_wav, Path):
        speaker_wav = str(speaker_wav)

    api = TTS(tts_model).to(device)
    
    wav = api.tts(text=text, language=language, speaker=speaker, speaker_wav=speaker_wav, speed=speed)

    if out_path is not None:
        api.synthesizer.save_wav(wav=wav, path=out_path)

    return wav, api.synthesizer.output_sample_rate

