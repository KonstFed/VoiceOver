
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def build_settings():
    settings_builder = InlineKeyboardBuilder()
    settings_builder.add(InlineKeyboardButton(text="Change voice speaker", callback_data="settings_voice"))
    return settings_builder.as_markup()

def build_choose_voice(voices_dict: dict):
    voice_choose_kb_builder = InlineKeyboardBuilder()
    for voice_name, id in voices_dict.items():
        voice_choose_kb_builder.add(InlineKeyboardButton(text=voice_name, callback_data=f"voice_choose_{id}"))
    voice_choose_kb_builder.adjust(2, repeat=True)
    return voice_choose_kb_builder.as_markup()