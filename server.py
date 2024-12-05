'''
Flask application for emotion detection from text.
This application uses an external service to detect emotions from a given text
and returns a response with the detected emotions.
'''

from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def home():
    '''
    Render the home page where the user can input text for emotion analysis.

    Returns: str: HTML content of the home page.
    '''
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    '''
    Route to handle the emotion detection for the provided text.

    Args: text_to_analyze (str): The input text from the user for emotion analysis.

    Returns: str: The result of the emotion detection in a human-readable format.
    '''
    text_to_analyze = request.args.get('textToAnalyze', '')
    if not text_to_analyze.strip():
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    result = emotion_detector(text_to_analyze)
    if result.get('dominant_emotion') is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    # Breaking long lines into shorter ones to avoid line-too-long warning
    response_text = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, 'joy': {result['joy']} "
        f"and 'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
    )
    return response_text

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
