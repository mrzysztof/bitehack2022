from flask import request, jsonify, Flask
from http import HTTPStatus
import requests
from flask_cors import CORS
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
from ..model.swears_detector import SwearsDetector, ActionList


def offensivity_threshold2number(offensivity_threshold):
    if offensivity_threshold == "negative":
        return 0
    elif offensivity_threshold == "fairly negative":
        return 1
    elif offensivity_threshold == "neutral":
        return 2
    elif offensivity_threshold == "fairly positive":
        return 3
    elif offensivity_threshold == "positive":
        return 4
    else:
        raise ValueError("incorrect offensivity threshold")

@app.route('/foo', methods=['GET', 'POST'])
def foo():
    data = request.json
    return jsonify(data)

@app.route('/just_detect', methods=['GET', 'POST'])
def just_detect():
    if not request.is_json:
        return "json format is required", HTTPStatus.BAD_REQUEST
    data = request.json
    try:
        max_offensivity = offensivity_threshold2number(data['options']['max_offensivity'])
    except ValueError:
        return "incorrect max offensivity parameter", HTTPStatus.BAD_REQUEST
    got_messages = data['comments']
    messages2send = {
        "messages": [{"message_id": i, "content": mess} for i, mess in enumerate(got_messages)],
        "model": "flair"
    }
    detected_request = requests.post('http://127.0.0.1:8444/predict', json=messages2send)
    detected_data = detected_request.json()
    messages_detected = detected_data['messages']
    to_show = [offensivity_threshold2number(message['offensivity']) >= max_offensivity for message in messages_detected]
    return jsonify({"to_show": to_show})


@app.route('/detect_and_filter', methods=['GET', 'POST'])
def detect_and_filter():
    if not request.is_json:
        return "json format is required", HTTPStatus.BAD_REQUEST
    data = request.json
    swear_filter = SwearsDetector('src/data/excluded_words.json')
    filtred_comments = [swear_filter.detect(comment) for comment in data['comments']]
    try:
        max_offensivity = offensivity_threshold2number(data['options']['max_offensivity'])
    except ValueError:
        return "incorrect max offensivity parameter", HTTPStatus.BAD_REQUEST
    got_messages = data['comments']
    messages2send = {
        "messages": [{"message_id": i, "content": mess} for i, mess in enumerate(got_messages)],
        "model": "flair"
    }
    detected_request = requests.post('http://127.0.0.1:8444/predict', json=messages2send)
    detected_data = detected_request.json()
    messages_detected = detected_data['messages']
    to_show = [offensivity_threshold2number(message['offensivity']) >= max_offensivity for message in messages_detected]
    return jsonify({"to_show": to_show, "filteres_comments": filtred_comments})

# print('xxxxxx')
@app.route('/detect_and_replace', methods=['GET', 'POST'])
def detect_and_replace():
    if not request.is_json:
        return "json format is required", HTTPStatus.BAD_REQUEST
    data = request.json
    swear_filter = SwearsDetector('src/data/excluded_words.json')
    filtered_comments = [list(swear_filter.detect(comment, action=ActionList.Mask)) for comment in data['comments']]
    
    try:
       max_offensivity = offensivity_threshold2number(data['options']['max_offensivity'])
    except ValueError:
       return "incorrect max offensivity parameter", HTTPStatus.BAD_REQUEST
    
    # text classification
    messages2send = {"messages": [{"message_id": i, "content": mess} for i, mess in enumerate(data['comments'])], "model": "flair"}
    detected_request = requests.post('http://127.0.0.1:8444/predict', json=messages2send)

    print('here1')
    if not detected_request.status_code == HTTPStatus.OK:
        return "communication error", HTTPStatus.INTERNAL_SERVER_ERROR

    print('here2')
    detected_data = detected_request.json()
    messages_detected = detected_data['messages']


    # language model
    messages_filtered = []

    for i, (filtered_comment_parts, comment) in enumerate(zip(filtered_comments, data['comments'])):
        print('here')
        messages2send_lm = {
            "messages": [{
                "message_id": i, "content": comment, 'spans': [
                    {'start': start, 'end': end} for start, end in filtered_comment_parts
                ]
            }]
        }
        print(messages2send_lm)
        detected_request_filter = requests.post('http://127.0.0.1:8444/lm', json=messages2send_lm)

        if not detected_request_filter.status_code == HTTPStatus.OK:
            return "communication error", HTTPStatus.INTERNAL_SERVER_ERROR
    
        messages_filtered.append(detected_request_filter.json()['messages'][0]['content'])

    to_show = [offensivity_threshold2number(message['offensivity']) >= max_offensivity for message in messages_detected]
    return jsonify({"to_show": to_show, "filteres_comments": messages_filtered})

