import numpy as np
import torch

from so_vits_svc_fork.inference.core import Svc


class SvcWrapper:
    def __init__(self, g_path: str, config_path: str, device: str = "cpu") -> None:
        self.device = device
        self.svc = Svc(
            net_g_path=g_path,
            config_path=config_path,
            cluster_model_path=None,
            device=device,
        )
        self.target_sample = self.svc.target_sample

    def get_speakers(self) -> list[str]:
        return self.svc.spk2id

    def forward(self, audio: np.ndarray, speaker: int|str=0) -> np.ndarray:
        output_audio, _ = self.svc.infer(speaker=speaker, transpose=0, audio=audio)
        return output_audio

    def __call__(self, audio: np.ndarray, speaker: int|str=0) -> np.ndarray:
        return self.forward(audio, speaker)

    def to_gpu(self) -> None:
        self.device = "gpu"
        _device = torch.device(self.device)
        self.svc.device = _device

    def to_cpu(self) -> None:
        self.device = "gpu"
        _device = torch.device(self.device)
        self.svc.device = _device


if __name__ == "__main__":
    import librosa
    import soundfile
    svc = SvcWrapper("voices/Nikita/model/G_10000.pth", "voices/Nikita/config/config.json")

    input_audio, _ = librosa.load(
        "test_samples/input/kisel_kostya.ogg", sr=svc.target_sample
    )

    output_audio = svc(input_audio, 0)
    soundfile.write("test_samples/output/new.ogg", output_audio, svc.target_sample)
