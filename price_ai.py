import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# 1. Historical Mock Data (Month, Rain_mm, Temp_C, Demand_Index) -> Price_per_kg
data = {
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'rain_mm': [10, 5, 20, 40, 60, 120, 150, 130, 90, 40, 15, 5],
    'temp_c': [22, 25, 29, 33, 35, 30, 28, 27, 28, 26, 24, 21],
    'demand_index': [80, 85, 90, 85, 95, 110, 120, 115, 100, 90, 85, 80],
    'price_per_kg': [20, 22, 25, 24, 30, 45, 50, 48, 35, 28, 24, 21]
}
df = pd.DataFrame(data)

# 2. Separate Features (Inputs) and Target (Output)
X = df[['month', 'rain_mm', 'temp_c', 'demand_index']]
y = df['price_per_kg']

# 3. Train the AI Model
print("🧠 Training Random Forest AI...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Predict Next Week's Price
# Scenario: Next month (September/9), 80mm rain, 29C temp, 105 demand
next_week = pd.DataFrame([[9, 80, 29, 105]], columns=['month', 'rain_mm', 'temp_c', 'demand_index'])
predicted_price = model.predict(next_week)[0]

print("✅ AI Training Complete!")
print(f"🍅 Forecasted Tomato Price for Next Week: ₹{predicted_price:.2f} per kg")