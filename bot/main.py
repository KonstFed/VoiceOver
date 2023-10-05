import sys

sys.path.append(".")

import json
import logging
from io import BytesIO
import asyncio


from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
import librosa
import soundfile
import numpy as np


from voice_conversion.svc import SvcWrapper
from db import get_user, add_user, update_user
from user import User, RedactState, WorkingState
from keyboards.settings import build_settings, build_choose_voice


with open("bot/bot_config.json", "r") as f:
    secret = json.load(f)

TOKEN = secret["token"]
bot = Bot(token=TOKEN)
dp = Dispatcher()

# SVC = SvcWrapper("voices/Nikita/model/G_10000.pth", "voices/Nikita/config/config.json")
SVC = SvcWrapper("voices/batch/G_107.pth", "voices/batch/config.json")


spk2id = SVC.get_speakers()
id2spk = {value: key for key, value in spk2id.items()}


@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    user = get_user(message.from_user.id)
    if user is None:
        user = User(message.from_user.id, message.from_user.username, WorkingState())
        add_user(user)

    await bot.send_message(
        user.telegram_id,
        f"Welcome to VoiceOver bot. Your voice choice is {id2spk[user.voice]}. If you want to change it press /settings",
    )


@dp.message(Command("settings"))
async def send_settings(message: types.Message):
    user = get_user(message.from_user.id)
    msg = await bot.send_message(
        user.telegram_id,
        f"Your current settings\nVoice speaker: {id2spk[user.voice]}",
        reply_markup=build_settings(),
    )
    user.state = RedactState("remove_settings_state", msg.message_id)
    update_user(user)


@dp.callback_query(F.data.regexp("voice_choose_[\d]+"))
async def handle_voice_choose(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    voice = int(callback.data.split("_")[-1])
    user.voice = voice
    update_user(user)
    await callback.answer()
    await bot.delete_message(user.telegram_id, user.state.msg_id)
    await bot.send_message(user.telegram_id, f"You current voice is changed to `{id2spk[voice]}`\nIf you want to change it use /settings")
    # await send_settings(cal)


@dp.callback_query(F.data == "settings_voice")
async def handle_change_voice_setting(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    if user.state != "remove_settings_state":
        return
    await bot.delete_message(callback.from_user.id, user.state.msg_id)
    msg = await bot.send_message(
        user.telegram_id,
        "You can choose from following voices",
        reply_markup=build_choose_voice(spk2id),
    )
    user.state = RedactState("remove_settings_state", msg.message_id)
    update_user(user)
    await callback.answer()


async def _load_voice(file_id) -> np.ndarray:
    file = await bot.get_file(file_id)
    result = await bot.download_file(file.file_path)
    inp_audio, _ = librosa.load(result, sr=SVC.target_sample)
    inp_audio = inp_audio.astype("float32")
    return inp_audio


def _to_inputfile(sound: np.ndarray) -> BufferedInputFile:
    audio_buffer = BytesIO()
    soundfile.write(audio_buffer, sound, samplerate=SVC.target_sample, format="ogg")
    return BufferedInputFile(audio_buffer.getvalue(), "output.ogg")


@dp.message(F.voice)
async def handle_voice(msg: types.Message):
    user = get_user(msg.from_user.id)
    file_id = msg.voice.file_id
    inp_audio = await _load_voice(file_id)
    output_audio = SVC(inp_audio, speaker=user.voice)

    await bot.send_voice(msg.from_user.id, _to_inputfile(output_audio))



async def start_bot() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
