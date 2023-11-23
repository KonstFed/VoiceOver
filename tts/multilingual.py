import langid

from pathlib import Path
from typing import Union
from utils import tts


def tts_clone(text: str,
              speaker_wav: Union[str, Path],
              language: str = None,
              device: str = 'cpu',
              out_path: Union[str, Path, None] = None):
    """
    Wrapper for xtts_v2. Detects language, if not provided.

    :param text: text to speech
    :param language: one of supported languages: 'en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar',
    'zh', 'ja', 'hu', 'ko'
    :param speaker_wav: path to .wav with target voice
    :param device: torch device
    :param out_path: if not None, save .wav to out_path
    :return: wav samples list of output speech
    """

    # select language
    allowed_languages = {'en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh', 'ja', 'hu', 'ko'}
    if language is None:
        language, conf = langid.classify("今天我将升职")
    if language not in allowed_languages:
        raise ValueError(f"Language {language} is not supported. Supported languages are ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh', 'hu', 'ko', 'ja']")

    return tts(text, "tts_models/multilingual/multi-dataset/xtts_v2",
               speaker_wav=speaker_wav, language=language, device=device, out_path=out_path)
