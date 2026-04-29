import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# 1. Load Data
print("Loading data...")
df = pd.read_csv('../data/creditcard.csv')

# 2. Scaling
print("Scaling features...")
scaler = StandardScaler()
df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))
df.drop(['Time', 'Amount'], axis=1, inplace=True)

# 3. Split Data
X = df.drop('Class', axis=1)
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Handle Imbalance with SMOTE
print("Applying SMOTE...")
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# 5. Train XGBoost (GPU Enabled)
print("Training model on GPU...")
# Using device="cuda" to utilize your GPU for vastly faster training
model = xgb.XGBClassifier(
    n_estimators=100, 
    max_depth=5, 
    learning_rate=0.1, 
    device="cuda", 
    eval_metric='logloss'
)
model.fit(X_train_res, y_train_res)

# 6. Evaluate
print("Evaluating model...")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Save Model & Scaler
os.makedirs('../backend/models', exist_ok=True)
joblib.dump(model, '../backend/models/xgb_model.pkl')
joblib.dump(scaler, '../backend/models/scaler.pkl')
print("Model and scaler saved to backend/models/")