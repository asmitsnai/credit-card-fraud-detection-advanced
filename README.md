# 💳 Real-Time Credit Card Fraud Detection System

## 📌 Overview
An end-to-end ML engineering project demonstrating the detection of fraudulent transactions in a highly imbalanced dataset. This project simulates a live streaming environment where transactions are scored in real-time.

## 🏗 Tech Stack
* **Machine Learning:** Python, Scikit-learn, XGBoost (GPU Accelerated), SMOTE
* **Backend API:** FastAPI, Uvicorn
* **Frontend Dashboard:** Next.js, React, Tailwind CSS

## ⚙️ Core Architecture
1. **Data Handling:** SMOTE utilized to handle 99.8% / 0.2% class imbalance.
2. **Inference:** XGBoost classifier exposed via REST API.
3. **Monitoring:** Real-time polling dashboard to visualize operational metrics.

## 🚀 Quick Start
Open three separate terminal splits in VS Code:

Terminal 1 (Backend):

cd backend
uvicorn main:app --reload

Expected Result: Server running on http://127.0.0.1:8000

Terminal 2 (Frontend):

cd frontend
npm run dev

Expected Result: Next.js dashboard running on http://localhost:3000
