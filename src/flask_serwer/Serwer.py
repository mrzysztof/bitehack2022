from flask import request, jsonify
from http import HTTPStatus
import requests
from flask_serwer import mood_detector_blueprint
from ..model.swears_detector import SwearsDetector


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


@mood_detector_blueprint.route('/mood_detector/just_detect', methods=['GET'])
def mood_detect():
    if not request.is_json:
        return "json format is required", HTTPStatus.BAD_REQUEST
    data = request.json
    try:
        max_offensivity = offensivity_threshold2number(data['options']['max_offensivity'])
    except ValueError:
        return "incorrect max offensivity parameter", HTTPStatus.BAD_REQUEST
    got_messages = data['comments']
    messages2send = {"messages": [{"message_id": i, "content": mess} for i, mess in enumerate(got_messages)]}
    detected_request = requests.post('http://127.0.0.1:8444/', params=jsonify(messages2send))
    detected_data = detected_request.json()
    messages_detected = detected_data['messages']
    to_show = [offensivity_threshold2number(message['offensivity']) < max_offensivity for message in messages_detected]
    return jsonify({"to_show": to_show})


@mood_detector_blueprint.route('/mood_detector/detect_and_filter', methods=['GET'])
def detect_and_filter():
    if not request.is_json:
        return "json format is required", HTTPStatus.BAD_REQUEST
    data = request.json
    swear_filter = SwearsDetector('data/excluded_words.json')
    filtred_comments = [swear_filter.detect(comment) for comment in data['comments']]
    try:
        max_offensivity = offensivity_threshold2number(data['options']['max_offensivity'])
    except ValueError:
        return "incorrect max offensivity parameter", HTTPStatus.BAD_REQUEST
    got_messages = data['comments']
    messages2send = {"messages": [{"message_id": i, "content": mess} for i, mess in enumerate(got_messages)]}
    detected_request = requests.post('http://127.0.0.1:8444/', params=jsonify(messages2send))
    detected_data = detected_request.json()
    messages_detected = detected_data['messages']
    to_show = [offensivity_threshold2number(message['offensivity']) < max_offensivity for message in messages_detected]
    return jsonify({"to_show": to_show, "filteres_comments": filtred_comments})
