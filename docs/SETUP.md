# Windows 개발 환경과 설치 보고

기준일: 2026-10-04. 이 문서는 현재 PC에서 검증한 환경의 기록입니다.

## 프로그램

| 구성 | 버전 | 상태 |
| --- | --- | --- |
| VS Code | 1.140.0 | 설치 완료 |
| Git for Windows | 2.55.0.windows.5 | 설치 완료, 새 터미널의 PATH에서 검색 확인 |
| Python | 3.12.15 | uv 관리 버전으로 프로젝트 `.venv` 생성 |
| uv | 0.12.22 | 설치 완료, 사용자 PATH에 실행 폴더 추가 |
| FFmpeg shared | 8.1.2 | 설치 완료, TorchCodec 영상 읽기 확인 |
| NVIDIA RTX 3060 | VRAM 12GB | 기존 하드웨어, PyTorch CUDA 계산·역전파 확인 |

기존 Miniconda 환경은 유지했습니다. 프로젝트에는 별도 `.venv`를 사용합니다. ROS 2와 Linux/WSL 운영체제 구성, AWS, RAG와 LangGraph 패키지는 이번 설치 범위에 포함하지 않았습니다. 현재 PyTorch CUDA 런타임으로 실행 검사를 통과했으므로 별도 CUDA Toolkit은 설치하지 않았습니다.

## VS Code 확장

새로 설치한 확장:

- Korean Language Pack (`ms-ceintl.vscode-language-pack-ko`)
- IntelliJ IDEA Keybindings (`k--kato.intellij-idea-keybindings`): 주요 PyCharm 단축키
- Ruff (`charliermarsh.ruff`): 코드 검사와 서식
- GitHub Pull Requests (`github.vscode-pull-request-github`)

이미 설치되어 있어 확인한 확장:

- Python, Pylance, Python Debugger, Python Environments
- Jupyter 및 Jupyter Keymap, Renderers, Cell Tags, Slideshow
- WSL

한국어 언어 설정 `locale=ko`를 저장했습니다. 열려 있는 VS Code를 완전히 닫고 다시 열면 적용됩니다. 저장 시 Ruff 서식, import 정리와 수정 기능을 프로젝트 설정에 추가했습니다. 확장 설치는 Python 라이브러리 설치와 별개입니다.

## 주요 Python 패키지

직접 의존성은 [pyproject.toml](../pyproject.toml), 해결된 버전은 [uv.lock](../uv.lock)에 있습니다. 현재 Windows 가상환경에 설치된 전체 178개 배포 패키지는 [전체 목록](installed-packages-windows.txt)에서 확인할 수 있습니다.

| 분야 | 주요 버전 |
| --- | --- |
| GPU 학습 | torch 2.11.0+cu128, torchvision 0.26.0+cu128 |
| 로봇 학습·환경 | lerobot 0.6.1, gym-hil 0.1.14, mujoco 3.8.1, gymnasium 1.3.0 |
| 데이터 분석 | numpy 2.2.6, pandas 2.3.3, scipy 1.18.1, scikit-learn 1.9.1 |
| 시각화·영상 | matplotlib 3.11.2, imageio 2.38.0, torchcodec 0.11.1 |
| 추론 API | fastapi 0.142.2, uvicorn 0.54.0 |
| 개발 | ipykernel 7.4.0, jupyterlab 4.6.4, ruff 0.16.10, pytest 9.1.1 |

LeRobot이 사용하는 datasets, safetensors, Hugging Face Hub, Accelerate, W&B, 영상 도구 등은 의존성으로 함께 설치되었습니다. W&B 계정 연결이나 클라우드 배포는 아직 구성하지 않았습니다.

## 현재 PC에서 실행하기

MuJoCo가 한글이 포함된 XML 경로를 읽지 못하는 문제가 있어, 같은 폴더를 가리키는 영문 junction 경로를 만들었습니다. 파일을 복사하거나 옮기지 않았습니다.

```powershell
cd "$env:USERPROFILE/Projects/I_Want_RoboRobo"
./.venv/Scripts/python.exe --version
uv sync --locked --python .venv/Scripts/python.exe --no-python-downloads
./.venv/Scripts/python.exe scripts/check_environment.py
```

`uv sync --locked --no-python-downloads`도 현재 만들어 둔 환경에서 통과했습니다. 새 터미널에서 `uv`, `git`, `ffmpeg` 명령을 사용할 수 있습니다. 이전 터미널은 PATH를 새로 읽도록 다시 열어야 합니다.

VS Code에서 이 영문 경로를 열고 `.venv/Scripts/python.exe` 인터프리터를 선택합니다. 노트북 커널은 `Python (Robot Learning Lab)`으로 등록했습니다. 디버깅 설정은 `.vscode/launch.json`에 있습니다.

검사 보고서는 Git에서 제외되는 `outputs/environment-check.json`에 생성됩니다. 18개 항목이 모두 통과했습니다.

- 작은 Linear 모델의 CUDA 계산, 역전파, Adam 업데이트
- 주요 모듈 14개 import (ACT 모델 및 LeRobot 데이터셋 모듈 포함)
- MuJoCo 물리 계산 및 64 x 64 RGB 렌더링
- `gym_hil/PandaPickCubeBase-v0` 초기화와 한 단계 실행
- FFmpeg 영상 생성과 TorchCodec 첫 프레임 디코딩

위 검사는 실행 환경 확인입니다. 시연 데이터 수집, ACT 학습 완료나 로봇 집기 성공을 검증한 결과는 아닙니다. 집기 환경의 현재 관측 키는 `agent_pos`, `environment_state`였으며 학습용 카메라 관측은 추후 구성합니다.

## 새 Windows PC에서 준비하기

1. VS Code, Git, uv, NVIDIA 드라이버, FFmpeg shared 8 계열을 준비합니다.
2. 저장소를 한글이 없는 경로에 clone합니다.
3. `uv python install 3.12.15`, `uv venv --python 3.12.15`, `uv sync --locked` 순서로 환경을 만듭니다.
4. 환경 선택과 영상 DLL 검색을 확인한 뒤 검사 스크립트를 실행합니다.

현재 PC에서 uv의 Python 버전 별칭 경로 오류가 한 번 발생해, 실제 설치된 Python 실행 파일을 명시하여 `.venv`를 만들었습니다. 새 PC에서 같은 오류가 나면 `uv python dir` 아래 실제 `python.exe`를 `uv venv --python`에 전달합니다. GPU와 운영체제가 다르면 추가 조정이 필요합니다. 새 PC 전체 설치 과정은 이번 작업에서 별도로 검증하지 않았습니다.

## 공부와 아이패드

- [개발 환경 학습 PDF](../output/pdf/robot_learning_environment_guide_ko.pdf)
- [학습 가이드 텍스트](ENVIRONMENT_GUIDE.md)
- [VS Code 웹에서 열기](https://vscode.dev/github/I-Wani-RoboRobo/I_Want_RoboRobo)

아이패드 웹 편집기는 데스크톱 설정과 별도입니다. 문서·코드 읽기와 가벼운 수정에 사용하고 GPU 학습은 현재 데스크톱에서 실행합니다.
