# YOLO-World Webcam (Ultralytics)

Script Python simple pour faire de la detection d'objets en direct avec la webcam.

Fichier principal:
- `yoloworld_webcam.py`

## Prerequis

- Windows + Python (venv recommande)
- Webcam fonctionnelle
- Packages Python:

```powershell
c:/Users/PixUser/Desktop/ComputerVision/.venv/Scripts/python.exe -m pip install ultralytics opencv-python
```

## Lancer le script

Place-toi dans le dossier du projet:

```powershell
cd C:/Users/PixUser/Desktop/ComputerVision/YOLO-World
```

Lancement standard (le modele est telecharge automatiquement si absent):

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt
```

Quitter l'application:
- appuie sur `q`

## Exemples utiles

Detection de classes personnalisees:

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt --classes person bus car
```

Utiliser le GPU (si CUDA est disponible):

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt --device 0 --half
```

Mode plus rapide (resolution plus faible):

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt --imgsz 416 --frame-width 960 --frame-height 540
```

Sauvegarder la video annotee:

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt --save sortie.mp4
```

## Options principales

- `--model` nom/fichier du modele YOLO-World (`yolov8s-worldv2.pt` par defaut)
- `--camera-id` index webcam (0 par defaut)
- `--classes` liste de classes ciblees
- `--add-background-class` ajoute `""` a la liste des classes
- `--conf` seuil de confiance (defaut `0.25`)
- `--imgsz` taille d'inference (defaut `640`)
- `--device` `auto`, `cpu`, `0`, `1`, etc.
- `--half` active FP16 (utile surtout sur GPU)
- `--frame-width` largeur capture webcam
- `--frame-height` hauteur capture webcam
- `--save` fichier video de sortie

## Depannage rapide

Erreur de syntaxe d'argument:

```text
error: unrecognized arguments: -- model yolov8s-worldv2.pt
```

Cause: espace en trop entre `--` et `model`.

Correct:

```powershell
py yoloworld_webcam.py --model yolov8s-worldv2.pt
```

FPS faible (ex: 2 a 5 FPS):
- souvent normal en CPU
- essaye `--imgsz 416` ou `--imgsz 320`
- reduis la resolution webcam (`--frame-width 640 --frame-height 480`)
- utilise GPU CUDA (`--device 0 --half`) si disponible

Verifier CUDA dans le venv:

```powershell
c:/Users/PixUser/Desktop/ComputerVision/.venv/Scripts/python.exe -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

Si `False`, PyTorch CUDA n'est pas actif dans l'environnement.
