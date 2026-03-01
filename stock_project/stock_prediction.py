import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import glob
import os

# Auto-detect CSV files in the same folder as this script
script_dir = os.path.dirname(os.path.realpath(__file__))
csv_paths = sorted(glob.glob(os.path.join(script_dir, "*.csv")))
if not csv_paths:
    raise FileNotFoundError("No CSV files found in the project folder. Add your CSV(s) and retry.")

print("Found CSV files:", csv_paths)

# Read and concatenate CSV files (assumes same columns). If different columns, adjust accordingly.
dfs = []
for p in csv_paths:
    try:
        df = pd.read_csv(p)
        dfs.append(df)
    except Exception as e:
        print(f"Warning: failed to read {p}: {e}")

if not dfs:
    raise ValueError("No readable CSV files found.")

data = pd.concat(dfs, ignore_index=True)
print("Combined data shape:", data.shape)
print(data.head())

# Ensure required columns exist
required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
missing = [c for c in required_cols if c not in data.columns]
if missing:
    raise ValueError(f"Required columns missing from data: {missing}. Check your CSV files.")

# Plot closing price (first 200 points to keep plot readable)
plt.plot(data['Close'].iloc[:200])
plt.title("Closing Price Trend (first 200 rows)")
plt.xlabel("Rows")
plt.ylabel("Price")
plt.show()

# Prepare data (simple features)
X = data[['Open', 'High', 'Low', 'Volume']]
y = data['Close']

# Train-test split (no shuffle for time-series)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
print("RMSE:", rmse)
