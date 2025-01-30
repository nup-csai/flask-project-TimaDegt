import unittest
import requests

BASE_URL = "http://localhost:8080"

class TestWorkoutTracker(unittest.TestCase):
    def setUp(self):
        self.workout_id = None
        self.exercise_id = None

    def tearDown(self):
        if self.exercise_id:
            requests.delete(f"{BASE_URL}/api/exercises/{self.exercise_id}")
        if self.workout_id:
            requests.delete(f"{BASE_URL}/api/workouts/{self.workout_id}")

    def test_1_create_workout(self):
        response = requests.post(
            f"{BASE_URL}/api/workouts",
            json={"name": "Morning Routine"}
        )
        self.assertEqual(response.status_code, 201)
        self.workout_id = response.json()["id"]
        self.assertIsNotNone(self.workout_id)

    def test_2_create_exercise(self):
        self.test_1_create_workout()  # Ensure a workout exists
        response = requests.post(
            f"{BASE_URL}/api/workouts/{self.workout_id}/exercises",
            json={"name": "Push-ups", "sets": 3, "reps": 10, "duration": 60}
        )
        self.assertEqual(response.status_code, 201)
        self.exercise_id = response.json()["id"]
        self.assertIsNotNone(self.exercise_id)

    def test_3_get_exercises(self):
        self.test_2_create_exercise()  # Ensure a workout and exercise exist
        response = requests.get(
            f"{BASE_URL}/api/workouts/{self.workout_id}/exercises"
        )
        self.assertEqual(response.status_code, 200)
        exercises = response.json()
        self.assertGreater(len(exercises), 0)

    def test_4_toggle_exercise_completion(self):
        self.test_2_create_exercise()  # Ensure a workout and exercise exist
        response = requests.put(
            f"{BASE_URL}/api/exercises/{self.exercise_id}/complete",
            json={"completed": True}
        )
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            f"{BASE_URL}/api/workouts/{self.workout_id}/exercises"
        )
        exercises = response.json()
        exercise = next(e for e in exercises if e["id"] == self.exercise_id)
        self.assertTrue(exercise["completed"])

    def test_5_delete_exercise(self):
        self.test_2_create_exercise()  # Ensure a workout and exercise exist
        response = requests.delete(
            f"{BASE_URL}/api/exercises/{self.exercise_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.exercise_id = None  # Mark as deleted to avoid cleanup

    def test_6_delete_workout(self):
        self.test_1_create_workout()  # Ensure a workout exists
        response = requests.delete(
            f"{BASE_URL}/api/workouts/{self.workout_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.workout_id = None  # Mark as deleted to avoid cleanup

if __name__ == "__main__":
    unittest.main()

def check_root_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 400:
            print("Запрос успешен, код 200.")
        else:
            exit(-1)
    except requests.RequestException as e:
        exit(-1)


check_root_url(BASE_URL)