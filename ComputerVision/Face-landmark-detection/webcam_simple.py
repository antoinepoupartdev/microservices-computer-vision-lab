import os

import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_styles, drawing_utils


MODEL_PATH = "face_landmarker.task"
CAMERA_ID = 0

if not os.path.exists(MODEL_PATH):
    print("Le modele face_landmarker.task manque.")
    print("Telecharge-le puis mets-le dans ce dossier:")
    print(
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    )
    raise SystemExit(1)

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=4,
    min_face_detection_confidence=0.35,
    min_face_presence_confidence=0.35,
    min_tracking_confidence=0.35,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
)

cap = cv2.VideoCapture(CAMERA_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Impossible d'ouvrir la webcam.")
    raise SystemExit(1)

print("Webcam ouverte. Appuie sur Q pour quitter.")

start_time_ms = cv2.getTickCount() / cv2.getTickFrequency() * 1000


def draw_landmarks_on_image(bgr_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(bgr_image)

    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style(),
        )
        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style(),
        )
        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_LEFT_IRIS,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style(),
        )
        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_RIGHT_IRIS,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style(),
        )

    return annotated_image


def plot_face_blendshapes_bar_graph(face_blendshapes):
    face_blendshapes_names = [
        face_blendshapes_category.category_name
        for face_blendshapes_category in face_blendshapes
    ]
    face_blendshapes_scores = [
        face_blendshapes_category.score
        for face_blendshapes_category in face_blendshapes
    ]
    face_blendshapes_ranks = range(len(face_blendshapes_names))

    fig, ax = plt.subplots(figsize=(12, 12))
    bar = ax.barh(
        face_blendshapes_ranks,
        face_blendshapes_scores,
        label=[str(x) for x in face_blendshapes_ranks],
    )
    ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
    ax.invert_yaxis()

    for score, patch in zip(face_blendshapes_scores, bar.patches):
        plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

    ax.set_xlabel("Score")
    ax.set_title("Face Blendshapes")
    plt.tight_layout()
    plt.show()


with FaceLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int((cv2.getTickCount() / cv2.getTickFrequency() * 1000) - start_time_ms)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.face_landmarks:
            frame = draw_landmarks_on_image(frame, result)

        cv2.putText(
            frame,
            f"Visages: {len(result.face_landmarks) if result.face_landmarks else 0}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        cv2.imshow("Face Landmarker - Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
print("Webcam fermee.")
