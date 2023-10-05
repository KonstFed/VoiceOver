import sys
sys.path.append('.')

import asyncio
import logging
import sys
from io import BytesIO
import json


from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile


from voice_conversion.svc import SvcWrapper

import librosa
import soundfile


with open("bot/bot_config.json", "r") as f:
    secret = json.load(f)

SVC = SvcWrapper("voices/Nikita/model/G_10000.pth", "voices/Nikita/config/config.json")

TOKEN = secret["token"]
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start", "help"))
async def process_start_command(message: types.Message):
    await message.reply(
        "ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ. TODO"
    )


@dp.message(F.voice)
async def handle_photo(msg: types.Message):
    file_id = msg.voice.file_id
    file = await bot.get_file(file_id)
    result: BytesIO = await bot.download_file(file.file_path)
    inp_audio, _ = librosa.load(result, sr=SVC.target_sample)
    inp_audio = inp_audio.astype("float32")
    output_audio = SVC(inp_audio, speaker=0)
    audio_buffer = BytesIO()
    soundfile.write(audio_buffer, output_audio, samplerate=SVC.target_sample, format="WAV")
    with open("bot/debug.wav", "wb") as f:
        f.write(audio_buffer.getvalue())
    outputfile = BufferedInputFile(audio_buffer.getvalue(), "output.wav")
    await bot.send_voice(msg.from_user.id, outputfile)

@dp.message()
async def handle_photo(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Default answer")

async def start_bot() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
