import os
from moviepy.editor import VideoFileClip
import librosa
import soundfile
from slicer2 import Slicer


def video_to_audio(dir_to, dir_from, video_file, output_ext="wav"):
    filename = video_file.split(".")[0]
    clip = VideoFileClip(f'{dir_from}/{video_file}')
    if not os.path.exists(dir_to):
        os.makedirs(dir_to)
    clip.audio.write_audiofile(f"{dir_to}/{filename}.{output_ext}")

def slice_audio(path, video_file, min_interval=300, min_length=10000):
    print(f'Loading {video_file}...')
    audio, sr = librosa.load(path + '/' + video_file, sr=None, mono=False) 
    slicer = Slicer(sr=sr, min_length=min_length, min_interval=min_interval)
    print(f'Slicing {video_file}...')
    chunks = slicer.slice(audio)
    print('Done, saving...')

    path += '/clips'
    if not os.path.exists(path):
        os.makedirs(path)

    for i, chunk in enumerate(chunks):
        if len(chunk.shape) > 1:
            chunk = chunk.T  # Swap axes if the audio is stereo.
        soundfile.write(f'{path}/{video_file.split(".")[0]}_{i}.wav', chunk, sr)  



do_not_process = ["ivanov", "strang"]

dirs = os.listdir('../video')

# Adjust min_intervals according to the temp of the speaker, 
# minimize the value if there is practically no silence, 
# maximize the value if there is a lot of silence.
min_intervals = dict(zip(dirs, [300, 300, 200, 250, 10]))

for dir in dirs:
    if dir in do_not_process or not os.listdir(f'../video/{dir}'):
        print(f'Skipping {dir}')
        continue
    dir_to = f'../audio/{dir}'
    dir_from = f'../video/{dir}'
    for video_file in os.listdir(dir_from):
        filename = video_file.split(".")[0]
        print(f'Processing {video_file}...')
        video_to_audio(dir_to, dir_from, video_file, output_ext="wav")
        slice_audio(path=dir_to, video_file=filename+'.wav', min_interval=min_intervals[dir])
        print('Finished with ' + video_file)

