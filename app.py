from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Exercise data with image paths
EXERCISES = {
    "kettlebell": [
        {"name": "Kettlebell Swing", "image": "kettlebell_swing.jpg"},
        {"name": "Kettlebell Goblet Squat", "image": "kettlebell_goblet_squat.jpg"},
        {"name": "Kettlebell Deadlift", "image": "kettlebell_deadlift.jpg"},
    ],
    "bodyweight": [
        {"name": "Push-Ups", "image": "pushups.jpg"},
        {"name": "Squats", "image": "squats.jpg"},
        {"name": "Lunges", "image": "lunges.jpg"},
    ],
    "stretch": [
        {"name": "Neck Stretch", "image": "neck_stretch.jpg"},
        {"name": "Shoulder Stretch", "image": "shoulder_stretch.jpg"},
    ],
    "daily_routines": [
        {"name": "Wake Up Early", "image": "alarm.jpg"},
        {"name": "Hydrate", "image": "water.jpg"},
    ]
}

@app.route('/')
def index():
    return render_template('index.html', exercises=EXERCISES)

@app.route('/exercise_image/<filename>')
def exercise_image(filename):
    return send_from_directory('static/images/exercises', filename)

@app.route('/get_exercises', methods=['GET'])
def get_exercises():
    return jsonify(EXERCISES)

if __name__ == '__main__':
    app.run(debug=True)