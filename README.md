# I Want RoboRobo

Robot Learning Lab

시뮬레이션 로봇 팔의 블록 집기를 모방학습하고, 평가·추론 서비스·ROS 2 작업 관리까지 단계적으로 연결하는 개인 프로젝트입니다.

## 현재 상태

Windows에서 Python 3.12와 GPU 학습 환경을 준비했습니다. RTX 3060에서 작은 모델의 계산·역전파, MuJoCo 물리 계산·RGB 렌더링, Panda 집기 환경 초기화·한 단계 실행, 영상 디코딩 검사를 통과했습니다.

시연 수집, ACT 모델 학습, 집기 성공률 평가, 추론 서비스와 ROS 2 연동은 아직 구현되지 않았습니다.

## 목표

- 로봇 팔 한 대와 블록 하나를 대상으로 집기 작업을 수행합니다.
- LeRobot의 ACT 모델로 시연 데이터를 학습합니다.
- 학습에 사용하지 않은 초기 위치에서 성공률을 평가합니다.
- 시연 데이터 양에 따른 성능 차이와 실패 원인을 기록합니다.
- 모델 추론을 별도 프로세스로 분리하고 실행 지연을 측정합니다.
- ROS 2를 통해 작업 시작, 진행 상태, 결과와 취소를 연결합니다.

## 진행 계획

주 5–6시간, 총 6–8주를 목표로 진행합니다. 개발 환경 확인 후 일정과 범위를 조정합니다.

자세한 단계와 완료 기준은 [로드맵](docs/ROADMAP.md)을 참고하세요.

## 개발 환경

- Python 3.12.15 / uv / 프로젝트 전용 `.venv`
- PyTorch 2.11.0 + CUDA 12.8 / torchvision 0.26.0
- LeRobot 0.6.1 / ACT
- MuJoCo 3.8.1 / Gymnasium 1.3.0 / gym-hil 0.1.14
- Jupyter / Ruff / pytest / FastAPI / Uvicorn
- ROS 2는 추후 연동 단계에서 설치합니다.

직접 의존성은 `pyproject.toml`, 해결된 버전은 `uv.lock`에 기록했습니다. 자세한 설치 목록과 실행법은 [환경 설정](docs/SETUP.md)을 참고하세요.

## 폴더 구성

```text
docs/                     계획과 개발 기록
experiments/              실험 설정과 비교 결과
scripts/                  데이터·학습·평가 실행 스크립트
src/robot_learning_lab/   프로젝트 코드
```

데이터, 모델 체크포인트, 비밀값 및 개인 환경 파일은 Git에 포함하지 않습니다. 공유가 필요한 데이터와 모델은 출처·사용 조건을 확인하고 별도 저장소 링크로 기록합니다.

## 시작하기

현재 단계에서는 실행 가능한 환경 검사 코드가 있습니다. 첫 시연 에피소드 저장과 실제 학습 코드가 다음 작업입니다.

Windows PowerShell에서 프로젝트 폴더로 이동한 뒤, 만들어 둔 가상환경으로 실행합니다.

```powershell
./.venv/Scripts/python.exe scripts/check_environment.py
```

이 PC에서는 MuJoCo의 한글 경로 문제를 피하기 위해 같은 프로젝트를 가리키는 영문 연결 경로 `~/Projects/I_Want_RoboRobo`를 사용합니다. 새 PC의 설치 절차와 차이는 [환경 설정](docs/SETUP.md)을 확인하세요.

## 공부 자료

- [개발 환경 학습 가이드 PDF](output/pdf/robot_learning_environment_guide_ko.pdf): 도구의 역할, 용어, GPU 실습, 8주 공부 계획, 설치 버전과 전체 패키지 목록
- [개발 환경 학습 가이드 텍스트](docs/ENVIRONMENT_GUIDE.md)
- [아이패드 VS Code 웹에서 저장소 열기](https://vscode.dev/github/I-Wani-RoboRobo/I_Want_RoboRobo)

VS Code 웹은 코드·문서 편집용입니다. 데스크톱의 GPU와 가상환경을 자동으로 사용하지 않습니다.

## 참고 자료

- [LeRobot 시뮬레이션 모방학습](https://huggingface.co/docs/lerobot/main/il_sim)
- [ACT 모델 안내](https://huggingface.co/docs/lerobot/main/act)
- [LeRobot 비동기 추론](https://huggingface.co/docs/lerobot/main/async)

참고 문서의 main 버전과 실제 설치 버전이 일치하는지 확인합니다.
