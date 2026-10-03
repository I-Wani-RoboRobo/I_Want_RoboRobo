"""Check installed learning libraries, CUDA, rendering, and video decoding."""

import importlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    report = {"python": platform.python_version(), "checks": {}, "packages": {}}
    dll_handles = []
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg and os.name == "nt":
        dll_handles.append(os.add_dll_directory(str(Path(ffmpeg).resolve().parent)))

    def check(name, operation):
        try:
            report["checks"][name] = {"ok": True, "detail": operation()}
            print(f"PASS {name}")
        except Exception as error:
            report["checks"][name] = {"ok": False, "error": str(error)}
            print(f"FAIL {name}: {error}")

    def cuda_training():
        import torch

        if not torch.cuda.is_available():
            raise RuntimeError("PyTorch cannot access CUDA.")
        model = torch.nn.Linear(4, 2).to("cuda")
        optimizer = torch.optim.Adam(model.parameters())
        loss = model(torch.randn(8, 4, device="cuda")).square().mean()
        loss.backward()
        optimizer.step()
        torch.cuda.synchronize()
        return {
            "device": torch.cuda.get_device_name(0),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "loss": loss.item(),
        }

    def mujoco_rendering():
        import mujoco

        model = mujoco.MjModel.from_xml_string(
            '<mujoco><worldbody><light pos="0 0 3"/>'
            '<geom type="plane" size="2 2 0.1"/>'
            '<body pos="0 0 1"><freejoint/>'
            '<geom type="sphere" size="0.1" mass="1"/>'
            "</body></worldbody></mujoco>"
        )
        data = mujoco.MjData(model)
        for _ in range(20):
            mujoco.mj_step(model, data)
        with mujoco.Renderer(model, height=64, width=64) as renderer:
            renderer.update_scene(data)
            frame = renderer.render()
        return {"simulated_seconds": data.time, "rgb_shape": list(frame.shape)}

    def video_decoding():
        from torchcodec.decoders import VideoDecoder

        if not ffmpeg:
            raise RuntimeError("FFmpeg is not on PATH. Restart the terminal after installing it.")
        with tempfile.TemporaryDirectory(prefix="robot-lab-video-") as temporary:
            video = Path(temporary) / "sample.mp4"
            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-loglevel",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=c=blue:s=64x64:r=5:d=1",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    str(video),
                ],
                check=True,
                capture_output=True,
            )
            decoder = VideoDecoder(str(video))
            frame = decoder[0]
            result = {"frames": len(decoder), "frame_shape": list(frame.shape)}
            del decoder
            del frame
            return result

    def pick_cube_environment():
        import gymnasium as gym
        import numpy as np

        with gym.make("gym_hil/PandaPickCubeBase-v0") as environment:
            observation, _ = environment.reset(seed=0)
            action = np.zeros(environment.action_space.shape, dtype=environment.action_space.dtype)
            _, reward, terminated, truncated, _ = environment.step(action)
            return {
                "observation_keys": sorted(observation),
                "reward": float(reward),
                "terminated": bool(terminated),
                "truncated": bool(truncated),
            }

    check("CUDA forward/backward", cuda_training)
    for module in (
        "torchvision",
        "numpy",
        "pandas",
        "scipy",
        "sklearn",
        "matplotlib",
        "gymnasium",
        "gym_hil",
        "fastapi",
        "uvicorn",
        "ipykernel",
        "jupyterlab",
        "lerobot.policies.act.modeling_act",
        "lerobot.datasets.lerobot_dataset",
    ):
        check(module, lambda name=module: importlib.import_module(name).__name__)
    check("MuJoCo physics and RGB rendering", mujoco_rendering)
    check("Panda pick-cube environment reset and step", pick_cube_environment)
    check("FFmpeg and TorchCodec video decoding", video_decoding)
    report["packages"] = {
        distribution.metadata["Name"]: distribution.version
        for distribution in importlib.metadata.distributions()
    }
    output = Path(__file__).resolve().parents[1] / "outputs" / "environment-check.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Installed distributions: {len(report['packages'])}")
    print(f"Report: {output}")
    return 0 if all(item["ok"] for item in report["checks"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
