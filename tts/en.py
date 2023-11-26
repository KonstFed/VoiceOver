from pathlib import Path
from typing import Union
from .utils import tts


def tts_male(text: str,
             device: str = 'cpu',
             out_path: Union[str, Path, None] = None,
             speed = 1.0):
    """
    Wrapper for vctk/vits, speaker p330

    :param text: text to speech
    :param device: torch device
    :param out_path: if not None, save .wav to out_path
    :return: wav samples list of output speech
    """

    return tts(text, "tts_models/en/vctk/vits",
               speaker='p330', speaker_wav=None, language=None, device=device, out_path=out_path, speed=speed)


def tts_female(text: str,
               device: str = 'cpu',
               out_path: Union[str, Path, None] = None,
               speed = 1.0):
    """
    Wrapper for vctk/vits, speaker p225

    :param text: text to speech
    :param device: torch device
    :param out_path: if not None, save .wav to out_path
    :return: wav samples list of output speech
    """

    return tts(text, "tts_models/en/vctk/vits",
               speaker='p225', speaker_wav=None, language=None, device=device, out_path=out_path, speed=speed)
