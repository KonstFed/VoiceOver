import sys

sys.path.append(".")

import json
import logging
logger = logging.getLogger("so_vits_svc_fork")
logger.setLevel(level=logging.DEBUG)
from io import BytesIO
import asyncio


from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import BufferedInputFile, Message
import librosa
import soundfile
import numpy as np


from voice_conversion.svc import SvcWrapper
from db import get_user, add_user, update_user
from user import User, RedactState, WorkingState
from keyboards.settings import build_settings, build_choose_voice


class AudioFileFilter(BaseFilter):

    def __init__(self, audio: bool) -> None:
        self.audio = audio
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        if self.audio:
            return not message.audio is None
        else:
            return not message.document is None

with open("bot/bot_config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
bot = Bot(token=TOKEN)
dp = Dispatcher()

svc_queue = asyncio.Queue(maxsize=6)


models = []
models_names = []
target_samples = []


async def request_queue_consumer(queue, bot):
    global models
    while True:
        user, inp_audio = await queue.get()
        if user is None:
            break
        output_audio = models[user.voice](inp_audio)
        await bot.send_voice(user.telegram_id, _to_inputfile(output_audio, target_samples[user.voice]))
        queue.task_done()

# SVC = SvcWrapper("voices/gura/G_3400.pth", "voices/gura/config.json")
# SVC = SvcWrapper("voices/nikita/nikita.pth", "voices/nikita/config.json")
# SVC = SvcWrapper("voices/ivanov/G_10000.pth", "voices/ivanov/config.json")

# SVC = SvcWrapper("voices/burmyakov/G_500.pth", "voices/burmyakov/config.json")
# SVC = SvcWrapper("voices/gura/G_5900.pth", "voices/gura/config.json")
# SVC = SvcWrapper("voices/neco/G_999.pth", "voices/neco/config.json")
# SVC = SvcWrapper("voices/sidor/G_1000.pth", "voices/sidor/sidor.json")


@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    user = get_user(message.from_user.id)
    if user is None:
        user = User(message.from_user.id, message.from_user.username, WorkingState())
        add_user(user)

    await bot.send_message(
        user.telegram_id,
        f"Welcome to VoiceOver bot. Your voice choice is {models_names[user.voice]}. If you want to change it press /settings",
    )


@dp.message(Command("settings"))
async def send_settings(message: types.Message):
    user = get_user(message.from_user.id)
    msg = await bot.send_message(
        user.telegram_id,
        f"Your current voice speaker:\n{models_names[user.voice]}",
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
    await bot.send_message(user.telegram_id, f"You current voice is changed to:\n`{models_names[voice]}`\nIf you want to change it use /settings")
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
        reply_markup=build_choose_voice(models_names),
    )
    user.state = RedactState("remove_settings_state", msg.message_id)
    update_user(user)
    await callback.answer()


async def _load_voice(file_id, target_sample) -> np.ndarray:
    file = await bot.get_file(file_id)
    result = await bot.download_file(file.file_path)
    
    inp_audio, _ = librosa.load(result, sr=target_sample)
    inp_audio = inp_audio.astype("float32")
    return inp_audio


def _to_inputfile(sound: np.ndarray, target_sample) -> BufferedInputFile:
    audio_buffer = BytesIO()
    soundfile.write(audio_buffer, sound, samplerate=target_sample, format="ogg")
    return BufferedInputFile(audio_buffer.getvalue(), "output")


@dp.message(F.voice)
async def handle_voice(msg: types.Message):
    user = get_user(msg.from_user.id)
    file_id = msg.voice.file_id
    inp_audio = await _load_voice(file_id, target_sample=target_samples[user.voice])
    task = svc_queue.put((user, inp_audio))
    q_size = svc_queue.qsize()
    await bot.send_message(user.telegram_id, f"You are {q_size} in queue...")
    await task



@dp.message(AudioFileFilter(audio=True))
async def handle_audio_file(msg: types.Message):
    user = get_user(msg.from_user.id)
    file_id = msg.audio.file_id
    inp_audio = await _load_voice(file_id, target_sample=target_samples[user.voice])
    task = svc_queue.put((user, inp_audio))
    q_size = svc_queue.qsize()
    await bot.send_message(user.telegram_id, f"You are {q_size} in queue...")
    await task


@dp.message(AudioFileFilter(audio=False))
async def handle_file(msg: types.Message):
    user = get_user(msg.from_user.id)
    file_id = msg.document.file_id
    inp_audio = await _load_voice(file_id, target_sample=target_samples[user.voice])
    task = svc_queue.put((user, inp_audio))
    q_size = svc_queue.qsize()
    await bot.send_message(user.telegram_id, f"You are {q_size} in queue...")
    await task

async def start_bot() -> None:

    svc_task = asyncio.create_task(request_queue_consumer(svc_queue, bot))
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    for model_cfg in config["models"]:
        model = SvcWrapper(model_cfg["weight_path"], model_cfg["config_path"])
        target_samples.append(model.target_sample)
        models.append(model)
        models_names.append(model_cfg["name"])
    await dp.start_polling(bot)
    await svc_task


if __name__ == "__main__":
    asyncio.run(start_bot())
