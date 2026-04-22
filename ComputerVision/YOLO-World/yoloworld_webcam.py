import argparse
import time

import cv2


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detection d'objets en direct avec YOLO-World (Ultralytics)."
    )
    parser.add_argument(
        "--model",
        default="yolov8s-worldv2.pt",
        help="Poids du modele YOLO-World (.pt).",
    )
    parser.add_argument(
        "--camera-id",
        type=int,
        default=0,
        help="ID de la webcam a utiliser.",
    )
    parser.add_argument(
        "--classes",
        nargs="*",
        default=None,
        help="Classes a detecter, ex: --classes person bus car",
    )
    parser.add_argument(
        "--add-background-class",
        action="store_true",
        help="Ajoute une classe vide en plus (option scenario-dependante).",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Seuil de confiance de detection.",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Taille d'inference.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        help="Device d'inference: auto, cpu, 0, 1...",
    )
    parser.add_argument(
        "--half",
        action="store_true",
        help="Active FP16 (utile surtout sur GPU).",
    )
    parser.add_argument(
        "--frame-width",
        type=int,
        default=1280,
        help="Largeur de capture webcam.",
    )
    parser.add_argument(
        "--frame-height",
        type=int,
        default=720,
        help="Hauteur de capture webcam.",
    )
    parser.add_argument(
        "--save",
        default=None,
        help="Chemin de sortie video (ex: sortie.mp4).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        from ultralytics import YOLOWorld
        import torch
    except Exception:
        print("Ultralytics n'est pas installe ou introuvable dans cet environnement.")
        print("Installe les dependances avec:")
        print("  .\\.venv\\Scripts\\python.exe -m pip install ultralytics opencv-python")
        raise SystemExit(1)

    # Ultralytics peut telecharger automatiquement les poids si on passe un nom de modele.
    model = YOLOWorld(args.model)

    if args.classes:
        class_names = list(args.classes)
        if args.add_background_class:
            class_names.append("")
        model.set_classes(class_names)
        print("Classes personnalisees:", class_names)
    else:
        print("Classes COCO par defaut utilisees (vocabulaire offline).")

    if args.device == "auto":
        device = 0 if torch.cuda.is_available() else "cpu"
    else:
        device = args.device

    use_half = args.half and str(device) != "cpu"
    print(f"Inference device: {device} | FP16: {use_half}")

    cap = cv2.VideoCapture(args.camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.frame_height)

    if not cap.isOpened():
        print("Impossible d'ouvrir la webcam.")
        raise SystemExit(1)

    writer = None
    if args.save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(args.save, fourcc, fps, (width, height))
        if not writer.isOpened():
            print(f"Impossible d'ecrire la video de sortie: {args.save}")
            writer = None

    print("Webcam ouverte. Appuie sur Q pour quitter.")

    prev_time = time.time()
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Lecture webcam interrompue.")
            break

        # Inference directe sur frame OpenCV (BGR).
        results = model.predict(
            source=frame,
            conf=args.conf,
            imgsz=args.imgsz,
            device=device,
            half=use_half,
            verbose=False,
        )

        annotated = results[0].plot()

        current_time = time.time()
        dt = max(current_time - prev_time, 1e-6)
        fps = 1.0 / dt
        prev_time = current_time

        cv2.putText(
            annotated,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.imshow("YOLO-World Webcam", annotated)

        if writer is not None:
            writer.write(annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()
    print("Arret du script.")


if __name__ == "__main__":
    main()
