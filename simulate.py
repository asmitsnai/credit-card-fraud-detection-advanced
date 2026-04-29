import pandas as pd
import requests
import time

print("Loading dataset and preparing a mixed simulation batch...")
df = pd.read_csv('data/creditcard.csv')

# Force the simulation to include actual frauds
# Grab 10 actual frauds and 90 normal transactions
try:
    frauds = df[df['Class'] == 1].sample(n=10, random_state=42)
    normals = df[df['Class'] == 0].sample(n=90, random_state=42)
except ValueError:
    # Fallback just in case the dataset has fewer rows than expected
    frauds = df[df['Class'] == 1]
    normals = df[df['Class'] == 0].head(90)

# Combine and shuffle them so the frauds appear randomly in the stream
simulation_data = pd.concat([normals, frauds]).sample(frac=1, random_state=42)

print("🚀 Starting Live Fraud Simulation (Mixed Batch)...")

for index, row in simulation_data.iterrows():
    # Format the data exactly how our FastAPI expects it
    payload = {
        "features": row.drop(['Class', 'Amount', 'Time']).tolist(),
        "amount": row['Amount'],
        "time": row['Time']
    }
    
    # Send the POST request to our API
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        data = response.json()
        
        # Color code the terminal output for dramatic effect
        if data["fraudulent"]:
            print(f"🚨 ALERT | Amount: ${row['Amount']:<8.2f} | STATUS: BLOCK | Prob: {data['probability']:.4f}")
        else:
            print(f"✅ PASS  | Amount: ${row['Amount']:<8.2f} | STATUS: SAFE  | Prob: {data['probability']:.4f}")
            
    except Exception as e:
        print("API offline or error:", e)
        
    # Wait 2 seconds before the next transaction
    time.sleep(2)