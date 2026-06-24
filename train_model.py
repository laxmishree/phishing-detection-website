import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Read dataset
data = pd.read_csv("dataset/dataset.csv")

# Remove index column
data = data.drop("index", axis=1)

# Last column is output
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Train model
model = RandomForestClassifier(random_state=42)

model.fit(X, y)
print("Number of features:", X.shape[1])
print("Training completed")

# Save model
joblib.dump(model, "model/phishing_model.pkl")

print("Model trained successfully!")
