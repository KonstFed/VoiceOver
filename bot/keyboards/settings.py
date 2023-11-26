
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def build_settings():
    settings_builder = InlineKeyboardBuilder()
    settings_builder.add(InlineKeyboardButton(text="Change voice speaker", callback_data="settings_voice"))
    settings_builder.add(InlineKeyboardButton(text="Change super tts", callback_data="settings_tts"))
    return settings_builder.as_markup()

def build_choose_voice(voices: list[str]):
    voice_choose_kb_builder = InlineKeyboardBuilder()
    for id, voice_name in enumerate(voices):
        voice_choose_kb_builder.add(InlineKeyboardButton(text=voice_name, callback_data=f"voice_choose_{id}"))
    voice_choose_kb_builder.adjust(2, repeat=True)
    return voice_choose_kb_builder.as_markup()

def build_settings_super_tts():
    settings_builder = InlineKeyboardBuilder()
    settings_builder.add(InlineKeyboardButton(text="Change voice speaker", callback_data="tts_voice_settings"))
    settings_builder.add(InlineKeyboardButton(text="Change voice language", callback_data="tts_lang_settings"))
    return settings_builder.as_markup()

def build_settings_super_tts_voice(supported_voices: list[str]):
    settings_builder = InlineKeyboardBuilder()
    for i, voice_str in enumerate(supported_voices):
        settings_builder.add(InlineKeyboardButton(text=voice_str, callback_data=f"super_tts_set_voice_{i}"))
    settings_builder.adjust(2, repeat=True)
    return settings_builder.as_markup()



def build_choose_lang(languages: list[str]):
    settings_builder = InlineKeyboardBuilder()
    for i, voice_str in enumerate(languages):
        settings_builder.add(InlineKeyboardButton(text=voice_str, callback_data=f"super_tts_set_lang_{i}"))
    settings_builder.adjust(4, repeat=True)
    return settings_builder.as_markup()