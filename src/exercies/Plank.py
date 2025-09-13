import cv2
import numpy as np
import mediapipe as mp
import time
import threading, queue
import pyttsx3

from src.ThreadedCamera import ThreadedCamera
from src.exercies.Exercise import Exercise
from src.utils import *  # needs: get_idx_to_coordinates, ang, rescale_frame

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

# MediaPipe Pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Drawing specs
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5


class VoiceCoach:
    """Non-blocking French TTS in a background thread."""
    def __init__(self, phrase="Ta position est fausse. Corrige-la.", rate=175, volume=1.0):
        self.phrase = phrase
        self.q = queue.Queue(maxsize=8)
        self.thread = threading.Thread(target=self._loop, args=(rate, volume), daemon=True)
        self.thread.start()

    def _loop(self, rate, volume):
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        # Try to pick a French voice if available
        try:
            for v in engine.getProperty('voices'):
                name = (getattr(v, 'name', '') or '').lower()
                langs = ','.join(getattr(v, 'languages', []) or []).lower()
                if 'fr' in name or 'french' in name or 'fr' in langs:
                    engine.setProperty('voice', v.id)
                    break
        except Exception:
            pass

        while True:
            text = self.q.get()
            if text is None:
                break
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

    def warn(self, text=None):
        try:
            self.q.put_nowait(text or self.phrase)
        except queue.Full:
            pass

    def stop(self):
        try:
            self.q.put_nowait(None)
        except Exception:
            pass


class Plank(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        eang1 = 0.0
        plankTimer = None
        plankDuration = 0.0

        # Voice coach setup
        coach = VoiceCoach(phrase="Ta position est fausse. Corrige-la.")

        # Immediate speak when bad starts, then one follow-up at +7s
        bad_state = False
        next_warning_time = None
        WARNING_DELAY = 7.0
        REPEAT_EVERY_7S = False   # set True if you want reminders every 7s continuously

        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue

            # Flip once for mirror view
            image = cv2.flip(image, 1)

            # Run MediaPipe Pose
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)
            image.flags.writeable = True

            # Draw pose landmarks
            if results.pose_landmarks is not None:
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=pose_landmark_drawing_spec,
                    connection_drawing_spec=pose_connection_drawing_spec
                )

            idx_to_coordinates = get_idx_to_coordinates(image, results)

            # Compute angle shoulder(11)-hip(23)-knee(27) on the left side
            try:
                if 11 in idx_to_coordinates and 23 in idx_to_coordinates and 27 in idx_to_coordinates:
                    cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[23]), thickness=6, color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[27]), thickness=6, color=(255, 0, 0))
                    eang1 = ang((idx_to_coordinates[11], idx_to_coordinates[23]),
                                (idx_to_coordinates[23], idx_to_coordinates[27]))
                    cv2.putText(image, str(round(eang1, 2)),
                                (idx_to_coordinates[23][0] - 40, idx_to_coordinates[23][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 0), thickness=3)
                    for k in (11, 23, 27):
                        cv2.circle(image, (idx_to_coordinates[k]), 10, (0, 0, 255), cv2.FILLED)
                        cv2.circle(image, (idx_to_coordinates[k]), 15, (0, 0, 255), 2)
            except Exception:
                pass

            # Form check + voice scheduling
            try:
                correct_form = eang1 > 170  # adjust threshold if too strict

                if correct_form:
                    # Proper plank timer
                    if plankTimer is None:
                        plankTimer = time.time()
                    plankDuration += time.time() - plankTimer
                    plankTimer = time.time()

                    # Reset bad-state scheduling
                    bad_state = False
                    next_warning_time = None
                else:
                    # Bad form: speak now on transition, then again at +7s
                    plankTimer = None
                    now = time.time()
                    if not bad_state:
                        bad_state = True
                        coach.warn()                      # immediate warning (FR)
                        next_warning_time = now + WARNING_DELAY
                    else:
                        if next_warning_time is not None and now >= next_warning_time:
                            coach.warn()                  # follow-up at +7s
                            if REPEAT_EVERY_7S:
                                # reschedule every 7s if you want continuous reminders
                                next_warning_time += WARNING_DELAY
                                while now >= next_warning_time and REPEAT_EVERY_7S:
                                    next_warning_time += WARNING_DELAY
                            else:
                                # only one follow-up
                                next_warning_time = None

                # Progress bar (based on angle)
                bar = np.interp(eang1, (120, 170), (850, 300))
                per = np.interp(eang1, (120, 170), (0, 100))
                cv2.rectangle(image, (200, 300), (260, 850), (0, 255, 0))
                cv2.rectangle(image, (200, int(bar)), (260, 850), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, f'{int(per)} %', (200, 255),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.1, color=(0, 255, 0), thickness=4)

            except Exception:
                pass

            # Plank timer overlay
            if 0 in idx_to_coordinates:
                cv2.putText(image, "Plank Timer : " + str(round(plankDuration)) + " sec",
                            (idx_to_coordinates[0][0] - 60, idx_to_coordinates[0][1] - 240),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.9, color=(0, 255, 0), thickness=4)

            # Show window
            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:  # ESC
                break

        # Cleanup
        coach.stop()
        pose.close()
        cv2.destroyAllWindows()
