from flask import Flask, render_template, request, jsonify
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock data for water usage
def generate_water_data():
    data = []
    base_date = datetime.now()
    for i in range(30):
        date = base_date - timedelta(days=29-i)
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'usage': random.randint(80, 200),
            'leak_detected': random.random() > 0.85
        })
    return data

# Mock AI prediction function
def predict_water_usage(historical_data, weather_data):
    # Simple prediction algorithm (in real app, would use ML model)
    last_week_avg = sum([d['usage'] for d in historical_data[-7:]]) / 7
    # Simulate some AI processing
    prediction = last_week_avg * (0.8 + 0.4 * random.random())
    return max(80, min(200, prediction))

# Sustainable plumbing tips
plumbing_tips = [
    "Install low-flow showerheads to reduce water usage by 40-50%",
    "Fix leaks promptly - a dripping faucet can waste 20 gallons of water a day",
    "Use water-efficient appliances (look for WaterSense labeled products)",
    "Install dual-flush toilets to save water with every flush",
    "Insulate hot water pipes to reduce heat loss and save water while waiting for hot water",
    "Collect rainwater for outdoor irrigation",
    "Use a broom instead of a hose to clean outdoor areas",
    "Water plants early in the morning or late in the evening to reduce evaporation"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/water-usage')
def water_usage():
    data = generate_water_data()
    return jsonify(data)

@app.route('/api/predict-usage', methods=['POST'])
def predict_usage():
    historical_data = request.json.get('historical_data', [])
    weather_data = request.json.get('weather_data', {})
    prediction = predict_water_usage(historical_data, weather_data)
    return jsonify({'prediction': round(prediction, 2)})

@app.route('/api/leak-alerts')
def leak_alerts():
    data = generate_water_data()
    leaks = [d for d in data if d['leak_detected']]
    return jsonify(leaks[-3:])  # Return last 3 leaks

@app.route('/api/plumbing-tips')
def get_plumbing_tips():
    return jsonify(plumbing_tips)

@app.route('/api/water-savings')
def water_savings():
    # Calculate potential savings
    data = generate_water_data()
    avg_usage = sum(d['usage'] for d in data) / len(data)
    potential_savings = avg_usage * 0.25  # Assume 25% savings with efficient practices
    return jsonify({
        'current_usage': round(avg_usage, 2),
        'potential_savings': round(potential_savings, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
