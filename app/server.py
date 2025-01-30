from flask import Flask, jsonify, request, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3

app = Flask(__name__)

# Swagger setup
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # URL for the Swagger JSON file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Workout Tracker API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Database setup
DATABASE = 'data/workout.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER,
                name TEXT NOT NULL,
                sets INTEGER,
                reps INTEGER,
                duration INTEGER,
                completed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (workout_id) REFERENCES workouts (id)
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    """
    Get all workouts.
    ---
    responses:
      200:
        description: A list of workouts.
    """
    conn = get_db_connection()
    workouts = conn.execute('SELECT * FROM workouts').fetchall()
    conn.close()
    return jsonify([dict(workout) for workout in workouts])

@app.route('/api/workouts', methods=['POST'])
def create_workout():
    """
    Create a new workout.
    ---
    parameters:
      - name: name
        in: body
        type: string
        required: true
    responses:
      201:
        description: Workout created successfully.
    """
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    conn = get_db_connection()
    conn.execute('INSERT INTO workouts (name) VALUES (?)', (name,))
    conn.commit()
    workout_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': workout_id, 'name': name}), 201

@app.route('/api/workouts/<int:workout_id>/exercises', methods=['GET'])
def get_exercises(workout_id):
    """
    Get all exercises for a workout.
    ---
    parameters:
      - name: workout_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A list of exercises.
    """
    conn = get_db_connection()
    exercises = conn.execute('SELECT * FROM exercises WHERE workout_id = ?', (workout_id,)).fetchall()
    conn.close()
    return jsonify([dict(exercise) for exercise in exercises])

@app.route('/api/workouts/<int:workout_id>/exercises', methods=['POST'])
def create_exercise(workout_id):
    """
    Create a new exercise for a workout.
    ---
    parameters:
      - name: workout_id
        in: path
        type: integer
        required: true
      - name: name
        in: body
        type: string
        required: true
      - name: sets
        in: body
        type: integer
        required: true
      - name: reps
        in: body
        type: integer
        required: true
      - name: duration
        in: body
        type: integer
        required: true
    responses:
      201:
        description: Exercise created successfully.
    """
    data = request.get_json()
    name = data.get('name')
    sets = data.get('sets')
    reps = data.get('reps')
    duration = data.get('duration')
    if not name or not sets or not reps or not duration:
        return jsonify({'error': 'Name, sets, reps, and duration are required'}), 400
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO exercises (workout_id, name, sets, reps, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (workout_id, name, sets, reps, duration))
    conn.commit()
    exercise_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': exercise_id, 'workout_id': workout_id, 'name': name, 'sets': sets, 'reps': reps, 'duration': duration}), 201

@app.route('/api/exercises/<int:exercise_id>/complete', methods=['PUT'])
def toggle_complete_exercise(exercise_id):
    """
    Toggle the completion status of an exercise.
    ---
    parameters:
      - name: exercise_id
        in: path
        type: integer
        required: true
      - name: completed
        in: body
        type: boolean
        required: true
    responses:
      200:
        description: Exercise completion status updated.
    """
    data = request.get_json()
    completed = data.get('completed')
    if completed is None:
        return jsonify({'error': 'Completed status is required'}), 400
    conn = get_db_connection()
    conn.execute('UPDATE exercises SET completed = ? WHERE id = ?', (completed, exercise_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Exercise completion status updated'}), 200

@app.route('/api/timer', methods=['POST'])
def start_timer():
    """
    Start a timer.
    ---
    parameters:
      - name: duration
        in: body
        type: integer
        required: true
    responses:
      200:
        description: Timer started successfully.
    """
    data = request.get_json()
    duration = data.get('duration')
    if not duration:
        return jsonify({'error': 'Duration is required'}), 400
    from datetime import datetime
    end_time = datetime.now().timestamp() + duration
    return jsonify({'end_time': end_time}), 200

@app.route('/api/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """
    Delete a workout.
    ---
    parameters:
      - name: workout_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Workout deleted successfully.
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Workout deleted successfully'}), 200

@app.route('/api/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """
    Delete an exercise.
    ---
    parameters:
      - name: exercise_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Exercise deleted successfully.
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM exercises WHERE id = ?', (exercise_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Exercise deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
