from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from database import init_db, save_consultation, get_all_consultations
import json
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create database when app starts
init_db()

SYSTEM_PROMPT = """
You are HomeoBot, a homeopathic medicine assistant for a college project.
You specialize ONLY in homeopathic remedies and treatments.
When given symptoms, respond ONLY in this exact JSON format with no extra text:
{
  "condition": "most likely condition",
  "medicines": [
    {"name": "homeopathic remedy name", "dosage": "potency and how often e.g. Arnica 30C twice daily"}
  ],
  "lifestyle": "one homeopathic lifestyle tip",
  "advice": "one helpful tip. This is not real medical advice.",
  "see_doctor": true,
  "doctor_reason": "reason here"
}
Only suggest homeopathic remedies like Arnica, Belladonna, Nux Vomica, Pulsatilla etc.
Always mention potency (6C, 30C, 200C) in dosage.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms")
        patient_name = data.get("patient", "Anonymous")

        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Patient symptoms: " + symptoms}
            ],
            temperature=0.3
        )

        raw_text = response.choices[0].message.content.strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw_text)

        # Save to database
        medicines_text = ", ".join([m["name"] + " " + m["dosage"] for m in result["medicines"]])
        save_consultation(
            patient_name,
            symptoms,
            result["condition"],
            medicines_text,
            result["advice"]
        )

        return jsonify(result)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# New route to see all patient history
@app.route("/history")
def history():
    consultations = get_all_consultations()
    return render_template("history.html", consultations=consultations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
