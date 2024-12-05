import requests
import json

def emotion_detector(text_to_analyse):
    # Definir Falta de texto a analizar
    if not text_to_analyse:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Define the URL for the emotion analysis API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Create the payload with the text to be analyzed
    # myobj = { "raw_document": { "text": text_to_analyse } }
    Input_json = { "raw_document": { "text": text_to_analyse } }
    
    # Set the headers with the required model ID for the API
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    # Despliego el texto pasao para analizarlo
    #print ("El texto a analizar es :",Input_json)
    
    try:
         # Make a POST request to the API with the payload and headers
        response = requests.post(url, json=Input_json, headers=headers)
            # Parse the response from the API
        formatted_response = json.loads(response.text)
        # Print Respuesta
        # print("La respuesta a la invocacion fue :", formatted_response)
        # Analizo si la devolucion es OK
        if response.status_code == 200:
            response_data = response.json()

            emotions = response_data['emotionPredictions'][0]['emotion']

            anger_score = emotions.get('anger', 0)
            disgust_score = emotions.get('disgust', 0)
            fear_score = emotions.get('fear', 0)
            joy_score = emotions.get('joy', 0)
            sadness_score = emotions.get('sadness', 0)

            emotion_output = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score
            }

            dominant_emotion = max(emotion_output, key=emotion_output.get, default=None)

            emotion_output['dominant_emotion'] = dominant_emotion

            if dominant_emotion is None:
                return {"error": "Invalid text! Please try again!"}

            return emotion_output
        else:
            return {"error": f"Error: Received status code {response.status_code}, Message: {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error: Failed to connect to the API. {e}"}