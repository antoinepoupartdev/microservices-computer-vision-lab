# Face Landmarker Webcam

Projet minimal pour ouvrir la webcam et afficher le maillage du visage en temps reel avec MediaPipe.

## Fichiers utiles

- [webcam_simple.py](webcam_simple.py)
- [face_landmarker.task](face_landmarker.task)
- [.venv](.venv)

## Ce que fait le script actuel

- ouvre la webcam en 1280x720
- met l'image en miroir pour l'effet selfie
- detecte les visages avec MediaPipe
- affiche le maillage facial en vert
- affiche des points du visage en jaune
- affiche le nombre de visages detectes
- quitte avec la touche `Q`

## Lancer le script

```powershell
cd C:\Users\PixUser\Desktop\ComputerVision
.\.venv\Scripts\python.exe webcam_simple.py
```

## Si le modele manque

Le script attend le fichier `face_landmarker.task` dans le dossier du projet.

Pour le retel charger:

```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task" -OutFile "face_landmarker.task"
```

## Dependances

Si tu veux reinstaller les packages de base:

```powershell
cd C:\Users\PixUser\Desktop\ComputerVision
.\.venv\Scripts\python.exe -m pip install mediapipe opencv-python
```

## Notes

Le script utilise le mode `VIDEO` de MediaPipe parce qu'il est adapte au flux en direct de la webcam. Ce n'est pas une video fichier.

Si tu veux garder un projet propre avec juste la webcam, tu peux supprimer les anciens fichiers d'exemple image ou video s'ils ne te servent plus.

