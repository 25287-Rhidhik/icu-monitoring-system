import serial
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import tensorflow as tf
import numpy as np

# SERIAL
ser = serial.Serial('COM3', 9600, timeout=1)

# FIREBASE
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://icu-monitoring-system-bc1c3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# MODEL
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

patients = ["P001", "P002", "P003"]
index = 0

print("Edge Monitor Started...")

while True:
    try:
        line = ser.readline().decode().strip()

        if not line:
            continue

        # ✅ FIXED SAFE SPLIT (no crash)
        values = line.split(",")

        if len(values) < 2:
            continue

        temp = float(values[0])
        hum = float(values[1])

        # ✅ SIMPLE NORMALIZATION (only fix needed)
        input_data = np.array([[temp/50.0, hum/100.0]], dtype=np.float32)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        ai_score = float(interpreter.get_tensor(output_details[0]['index'])[0][0])

        # ✅ SAME SIMPLE STATUS (like before)
        if temp > 38 or hum > 80:
            status = "CRITICAL"
        elif temp > 30 or hum > 70:
            status = "WARNING"
        else:
            status = "SAFE"

        current_time = datetime.now()
        patient_id = patients[index]
        index = (index + 1) % 3

        # ✅ SIMPLE FIREBASE (no complex structure)
        ref = db.reference(f"patients/{patient_id}")
        ref.set({
            "temp": temp,
            "humidity": hum,
            "ai_score": ai_score,
            "status": status,
            "time": str(current_time)
        })

        print(f"{patient_id} | {temp:.1f}C | {hum:.1f}% | {status} | AI:{ai_score:.2f}")

        time.sleep(2)

    except Exception as e:
        print("Error:", e)