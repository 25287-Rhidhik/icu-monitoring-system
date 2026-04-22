🏥 ICU Monitoring System using Edge AI & Firebase

📌 Project Overview

This project implements a real-time ICU patient monitoring system using Edge AI and Firebase Cloud.

The system collects environmental data (temperature & humidity) using sensors connected to Arduino, processes it locally using a TensorFlow Lite model, and stores the data in Firebase Realtime Database.

A Streamlit dashboard visualizes multi-patient data in real-time and provides alerts for critical conditions.

---

🎯 Objectives

- Monitor ICU environmental conditions in real-time
- Perform on-device AI-based risk prediction (Edge AI)
- Store and access data via cloud (Firebase)
- Provide real-time alerts for abnormal conditions
- Enable multi-patient monitoring through dashboard

---

🧩 System Architecture

🔄 Complete Workflow

1. Sensor Layer
   
   - DHT11/DHT22 sensor reads temperature & humidity

2. Microcontroller Layer (Arduino)
   
   - Processes sensor data
   - Sends data via Serial communication

3. Edge Layer (Python - Edge Monitor)
   
   - Reads serial data from Arduino
   - Runs TensorFlow Lite model for prediction
   - Sends processed data to Firebase Realtime Database

4. Cloud Layer (Firebase)
   
   - Stores patient data in real-time
   - Enables remote access

5. Application Layer (Dashboard)
   
   - Fetches data from Firebase
   - Displays real-time graphs & patient status
   - Triggers alerts for abnormal conditions

---

⚙️ Technologies Used

🔌 Hardware

- Arduino Uno
- DHT11 / DHT22 Sensor
- LED (Alert System)

💻 Software

- Python
- Streamlit
- TensorFlow Lite
- Pandas, Plotly
- PySerial
- Firebase Realtime Database

---

📁 Project Structure

health_edge_ai/
│
├── arduino/
│   └── patient_monitoring.ino
├── dashboard.py          # Firebase dashboard
├── edge_monitor.py       # Edge processing + Firebase upload
├── train_model.py        # Model training
├── convert.py            # Convert model to TFLite
├── model.h5
├── model.tflite
├── health_log.csv        # Backup local storage
├── requirements.txt
├── README.md
├── HLD.md
├── LLD.md

---

🔌 Arduino Functionality

- Reads temperature & humidity from DHT sensor
- Sends data via Serial in CSV format
- Controls LED for alert conditions:
  - Temperature > 30°C
  - Humidity > 60%

---

🤖 AI Model

- Built using TensorFlow
- Converted to TensorFlow Lite for edge deployment
- Predicts risk level based on environmental conditions
- Enables low-latency processing without cloud dependency

---

📊 Dashboard Features

- Real-time multi-patient monitoring
- Temperature & humidity trend graphs
- AI-based risk prediction display
- Patient selection system
- Industrial-style UI (dark theme)
- Live Firebase data streaming

---

🚨 Alert System

- LED alert (hardware level)
- Dashboard alert (software level)

Status Levels:

- 🟢 SAFE → Normal condition
- 🟡 WARNING → Slight abnormality
- 🔴 CRITICAL → Immediate attention required

---

☁️ Cloud Integration (Firebase)

- Uses Firebase Realtime Database
- Stores patient data in structured format
- Enables:
  - Remote monitoring
  - Real-time updates
  - Scalability

---

🧪 How to Run

1️⃣ Setup Environment

pip install -r requirements.txt

---

2️⃣ Connect Hardware

- Connect Arduino + DHT sensor
- Upload Arduino code
- Note COM port (e.g., COM3)

---

3️⃣ Run Edge Monitor

python edge_monitor.py

---

4️⃣ Run Dashboard

streamlit run dashboard.py

---

📈 Output

- Live ICU monitoring dashboard
- Multi-patient temperature & humidity graphs
- AI-based risk prediction
- Real-time alert system
- Cloud-synced patient data

---

🚀 Future Enhancements

- Add advanced sensors (SpO2, Heart Rate)
- Mobile app integration
- Cloud deployment (AWS / GCP)
- Advanced deep learning models
- IoT device scaling

---

🏁 Conclusion

This project demonstrates a hybrid Edge + Cloud AI system for healthcare monitoring.

- Edge AI ensures low latency decision-making
- Firebase enables real-time cloud connectivity
- Dashboard provides intuitive visualization

This architecture is scalable and suitable for modern ICU environments.

---

👨‍💻 Author

Rhidhik

---

📜 License

This project is developed for academic and educational purposes.
