from flask import Blueprint, request, jsonify
import json
import os
from src.ai_model import get_response, save_appointment

ai_chat_bp = Blueprint("ai_chat_bp", __name__)

@ai_chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    response = get_response(user_message)
    
    # Check if the AI response indicates an appointment booking
    if "حجز موعد" in response and "يرجى تزويدي بهذه المعلومات لإتمام الحجز" in response:
        # This is a placeholder. In a real scenario, you'd extract entities
        # from the user_message and try to save the appointment.
        # For now, we'll just return the AI's request for more info.
        pass

    return jsonify({"response": response})

@ai_chat_bp.route("/book_appointment", methods=["POST"])
def book_appointment():
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")
    service = data.get("service")
    branch = data.get("branch")
    date = data.get("date")
    time = data.get("time")

    if not all([name, phone, service, branch, date, time]):
        return jsonify({"status": "error", "message": "يرجى توفير جميع معلومات الحجز."}), 400

    try:
        save_appointment(name, phone, service, branch, date, time)
        return jsonify({"status": "success", "message": "تم حجز موعدك بنجاح!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


