import os
import logging
from flask import Flask, render_template, request
from joblib import load
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the regression model
filename = 'first-innings-score-lr-model.joblib'
regressor = load(filename)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    try:
        # Get batting team and validate
        batting_team = request.form.get('batting-team')
        if batting_team == 'Chennai Super Kings':
            temp_array += [1, 0, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Delhi Daredevils':
            temp_array += [0, 1, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Kings XI Punjab':
            temp_array += [0, 0, 1, 0, 0, 0, 0, 0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array += [0, 0, 0, 1, 0, 0, 0, 0]
        elif batting_team == 'Mumbai Indians':
            temp_array += [0, 0, 0, 0, 1, 0, 0, 0]
        elif batting_team == 'Rajasthan Royals':
            temp_array += [0, 0, 0, 0, 0, 1, 0, 0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array += [0, 0, 0, 0, 0, 0, 1, 0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array += [0, 0, 0, 0, 0, 0, 0, 1]
        else:
            raise ValueError("Invalid batting team.")

        # Get bowling team and validate
        bowling_team = request.form.get('bowling-team')
        if bowling_team == 'Chennai Super Kings':
            temp_array += [1, 0, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array += [0, 1, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array += [0, 0, 1, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array += [0, 0, 0, 1, 0, 0, 0, 0]
        elif bowling_team == 'Mumbai Indians':
            temp_array += [0, 0, 0, 0, 1, 0, 0, 0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array += [0, 0, 0, 0, 0, 1, 0, 0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array += [0, 0, 0, 0, 0, 0, 1, 0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array += [0, 0, 0, 0, 0, 0, 0, 1]
        else:
            raise ValueError("Invalid bowling team.")

        # Get match parameters
        overs = float(request.form.get('overs', 0))
        runs = int(request.form.get('runs', 0))
        wickets = int(request.form.get('wickets', 0))
        runs_in_prev_5 = int(request.form.get('runs_in_prev_5', 0))
        wickets_in_prev_5 = int(request.form.get('wickets_in_prev_5', 0))

        # Add match parameters to input array
        temp_array += [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]

        # Make prediction
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])
        
        # Render result
        return render_template('result.html', lower_limit=my_prediction - 10, upper_limit=my_prediction + 5)

    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return render_template('error.html', error_message="There was an error processing your request.")

# Note: The app.run() block is removed for Vercel compatibility
