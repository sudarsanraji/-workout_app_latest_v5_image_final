from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Exercise data with image paths
EXERCISES = {
    "kettlebell": [
        {"name": "Kettlebell Swing", "image": "kettlebell_swing.jpg"},
        {"name": "Kettlebell Goblet Squat", "image": "kettlebell_goblet_squat.jpg"},
        {"name": "Kettlebell Deadlift", "image": "kettlebell_deadlift.jpg"},
        {"name": "Kettlebell Clean", "image": "kettlebell_clean.jpg"},
        {"name": "Kettlebell Snatch", "image": "kettlebell_snatch.jpg"},
        {"name": "Kettlebell Press", "image": "kettlebell_press.jpg"},
        {"name": "Kettlebell Push Press", "image": "kettlebell_push_press.jpg"},
        {"name": "Kettlebell Turkish Get-Up", "image": "kettlebell_turkish_getup.jpg"},
        {"name": "Kettlebell Windmill", "image": "kettlebell_windmill.jpg"},
        {"name": "Kettlebell High Pull", "image": "kettlebell_high_pull.jpg"},
        {"name": "Kettlebell Thruster", "image": "kettlebell_thruster.jpg"},
        {"name": "Kettlebell Row", "image": "kettlebell_row.jpg"},
        {"name": "Kettlebell Floor Press", "image": "kettlebell_floor_press.jpg"},
        {"name": "Kettlebell Halo", "image": "kettlebell_halo.jpg"},
        {"name": "Kettlebell Figure Eight", "image": "kettlebell_figure_eight.jpg"},
        {"name": "Kettlebell Lunge", "image": "kettlebell_lunge.jpg"},
        {"name": "Kettlebell Step-Up", "image": "kettlebell_stepup.jpg"},
        {"name": "Kettlebell Russian Twist", "image": "kettlebell_russian_twist.jpg"},
        {"name": "Kettlebell Side Bend", "image": "kettlebell_side_bend.jpg"},
        {"name": "Kettlebell Overhead Squat", "image": "kettlebell_overhead_squat.jpg"},
        {"name": "Kettlebell Single-Leg Deadlift", "image": "kettlebell_single_leg_deadlift.jpg"},
        {"name": "Kettlebell Clean and Press", "image": "kettlebell_clean_and_press.jpg"},
        {"name": "Kettlebell Clean and Jerk", "image": "kettlebell_clean_and_jerk.jpg"},
        {"name": "Kettlebell Bottoms-Up Press", "image": "kettlebell_bottoms_up_press.jpg"},
        {"name": "Kettlebell Farmer's Walk", "image": "kettlebell_farmers_walk.jpg"},
        {"name": "Kettlebell Suitcase Carry", "image": "kettlebell_suitcase_carry.jpg"},
        {"name": "Kettlebell Rack Carry", "image": "kettlebell_rack_carry.jpg"},
        {"name": "Kettlebell Overhead Carry", "image": "kettlebell_overhead_carry.jpg"},
        {"name": "Kettlebell Swing to Squat", "image": "kettlebell_swing_to_squat.jpg"},
        {"name": "Kettlebell Swing to High Pull", "image": "kettlebell_swing_to_high_pull.jpg"},
        {"name": "Kettlebell Swing to Clean", "image": "kettlebell_swing_to_clean.jpg"},
        {"name": "Kettlebell Swing to Snatch", "image": "kettlebell_swing_to_snatch.jpg"},
        {"name": "Kettlebell Swing to Press", "image": "kettlebell_swing_to_press.jpg"},
        {"name": "Kettlebell Swing to Thruster", "image": "kettlebell_swing_to_thruster.jpg"},
        {"name": "Kettlebell Swing to Row", "image": "kettlebell_swing_to_row.jpg"},
        {"name": "Kettlebell Swing to Floor Press", "image": "kettlebell_swing_to_floor_press.jpg"},
        {"name": "Kettlebell Swing to Halo", "image": "kettlebell_swing_to_halo.jpg"},
        {"name": "Kettlebell Swing to Figure Eight", "image": "kettlebell_swing_to_figure_eight.jpg"},
        {"name": "Kettlebell Swing to Lunge", "image": "kettlebell_swing_to_lunge.jpg"},
        {"name": "Kettlebell Swing to Step-Up", "image": "kettlebell_swing_to_stepup.jpg"}
    ],
    "bodyweight": [
        {"name": "Push Ups", "image": "pushups.jpg"},
        {"name": "Squats", "image": "squats.jpg"},
        {"name": "Lunges", "image": "lunges.jpg"},
        {"name": "Plank", "image": "plank.jpg"},
        {"name": "Burpees", "image": "burpees.jpg"},
        {"name": "Mountain Climbers", "image": "mountain_climbers.jpg"},
        {"name": "Jumping Jacks", "image": "jumping_jacks.jpg"},
        {"name": "Tricep Dips", "image": "tricep_dips.jpg"},
        {"name": "Bicycle Crunches", "image": "bicycle_crunches.jpg"},
        {"name": "Leg Raises", "image": "leg_raises.jpg"},
        {"name": "Side Plank", "image": "side_plank.jpg"},
        {"name": "Glute Bridges", "image": "glute_bridges.jpg"},
        {"name": "High Knees", "image": "high_knees.jpg"},
        {"name": "Inchworms", "image": "inchworms.jpg"},
        {"name": "Superman", "image": "superman.jpg"},
        {"name": "Russian Twists", "image": "russian_twists.jpg"},
        {"name": "Wall Sit", "image": "wall_sit.jpg"},
        {"name": "Donkey Kicks", "image": "donkey_kicks.jpg"},
        {"name": "Flutter Kicks", "image": "flutter_kicks.jpg"},
        {"name": "Bear Crawls", "image": "bear_crawls.jpg"}
    ],
    "stretch": [
        {"name": "Neck Stretch", "image": "neck_stretch.jpg"},
        {"name": "Shoulder Stretch", "image": "shoulder_stretch.jpg"},
        {"name": "Hamstring Stretch", "image": "hamstring_stretch.jpg"},
        {"name": "Quad Stretch", "image": "quad_stretch.jpg"},
        {"name": "Chest Stretch", "image": "chest_stretch.jpg"},
        {"name": "Back Stretch", "image": "back_stretch.jpg"},
        {"name": "Hip Flexor Stretch", "image": "hip_flexor_stretch.jpg"},
        {"name": "Calf Stretch", "image": "calf_stretch.jpg"},
        {"name": "Groin Stretch", "image": "groin_stretch.jpg"},
        {"name": "Tricep Stretch", "image": "tricep_stretch.jpg"}
    ],
    "daily_routines": [
        {"name": "Wake Up Early", "image": "alarm.jpg"},
        {"name": "Hydrate", "image": "water.jpg"},
        {"name": "Stretch or Exercise", "image": "morning_stretch.jpg"},
        {"name": "Meditate or Practice Mindfulness", "image": "meditation.jpg"},
        {"name": "Healthy Breakfast", "image": "healthy_breakfast.jpg"},
        {"name": "Plan Your Day", "image": "planning.jpg"},
        {"name": "Personal Hygiene", "image": "hygiene.jpg"},
        {"name": "Read or Listen to Something Inspirational", "image": "reading.jpg"}
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