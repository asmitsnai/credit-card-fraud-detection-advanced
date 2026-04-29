from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fraud Detection API")

# Allow Next.js frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
model = joblib.load('models/xgb_model.pkl')
scaler = joblib.load('models/scaler.pkl')

class Transaction(BaseModel):
    features: List[float] # V1 to V28
    amount: float
    time: float

# In-memory storage for dashboard simulation
recent_transactions = []
stats = {"total": 0, "fraud": 0, "safe": 0}

@app.post("/predict")
def predict_fraud(transaction: Transaction):
    # Scale Amount and Time
    scaled_amount = scaler.transform([[transaction.amount]])[0][0]
    scaled_time = scaler.transform([[transaction.time]])[0][0]
    
    # 🛠️ THE FIX: XGBoost requires the EXACT column names it was trained on
    # We generate the list of V1 through V28, plus our two scaled columns
    feature_cols = [f"V{i}" for i in range(1, 29)]
    columns = feature_cols + ["scaled_amount", "scaled_time"]
    
    # Combine features into a DataFrame WITH the explicit column names
    input_data = pd.DataFrame([transaction.features + [scaled_amount, scaled_time]], columns=columns)
    
    # Predict
    probability = model.predict_proba(input_data)[0][1]
    is_fraud = bool(probability > 0.85) # High threshold for precision
    
    # Update Stats
    stats["total"] += 1
    if is_fraud: stats["fraud"] += 1
    else: stats["safe"] += 1
    
    record = {"amount": transaction.amount, "fraud_probability": float(probability), "is_fraud": is_fraud}
    recent_transactions.insert(0, record)
    if len(recent_transactions) > 10: recent_transactions.pop()
    
    return {"fraudulent": is_fraud, "probability": float(probability)}

@app.get("/stats")
def get_stats():
    return {"stats": stats, "recent": recent_transactions}