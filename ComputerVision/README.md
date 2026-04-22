# ComputerVision - README general

Ce dossier regroupe deux mini-projets de vision par ordinateur:

- Face Landmarker (MediaPipe)
- YOLO-World Webcam (Ultralytics)

## Structure du dossier

- `Face-landmark-detection/`
  - `webcam_simple.py`
  - `face_landmarker.task`
  - `blaze_face_short_range.tflite`
  - `README.md`
- `YOLO-World/`
  - `yoloworld_webcam.py`
  - `yolov8s-worldv2.pt` (telecharge automatiquement au premier lancement si absent)
  - `README.md`
- `.venv/` (environnement virtuel Python)

## Prerequis

- Windows
- Python (de preference via `.venv`)
- Webcam

Activation de l'environnement virtuel (PowerShell):

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& C:/Users/PixUser/Desktop/ComputerVision/.venv/Scripts/Activate.ps1)
```

## Installation des dependances

Depuis la racine du projet:

```powershell
cd C:/Users/PixUser/Desktop/ComputerVision
.\.venv\Scripts\python.exe -m pip install mediapipe opencv-python ultralytics
```

## Demarrer Face Landmarker

```powershell
cd C:/Users/PixUser/Desktop/ComputerVision/Face-landmark-detection
py webcam_simple.py
```

Reference detaillee:
- voir `Face-landmark-detection/README.md`

## Demarrer YOLO-World

Lancement simple:

```powershell
cd C:/Users/PixUser/Desktop/ComputerVision/YOLO-World
py yoloworld_webcam.py --model yolov8s-worldv2.pt
```

Lancement plus rapide (GPU + reglages perf):

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt --device 0 --half --imgsz 416 --frame-width 960 --frame-height 540
```

Reference detaillee:
- voir `YOLO-World/README.md`

## Depannage rapide

- La commande `-- model` est invalide (espace en trop)
  - Correct: `--model`
- Si YOLO tourne a ~3 FPS, c'est souvent du CPU
  - verifier CUDA avec:

```powershell
C:/Users/PixUser/Desktop/ComputerVision/.venv/Scripts/python.exe -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

- Quitter les applications webcam:
  - appuyer sur `q`

## Conseils

- Ferme les applis qui utilisent deja la webcam (Teams, Discord, navigateur).
- Pour plus de FPS: baisse `--imgsz` (416 ou 320) et la resolution webcam.
- Pour un rendu plus stable en detection, limite les classes avec `--classes`.
