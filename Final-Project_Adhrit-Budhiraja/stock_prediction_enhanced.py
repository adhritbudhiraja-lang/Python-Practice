import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

print("Script starting...")

def find_data_file_in_script_folder():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print("Script folder (where script lives):", script_dir)
    files = sorted(glob.glob(os.path.join(script_dir, "*.csv")))
    print("CSV files found in script folder:", [os.path.basename(p) for p in files])
    preferred = ["stock_data_clean_fixed.csv", "stock_data.csv"]
    for p in preferred:
        candidate = os.path.join(script_dir, p)
        if os.path.exists(candidate):
            return candidate
    if files:
        return files[0]
    return None

csv_path = find_data_file_in_script_folder()
if not csv_path:
    print("No CSV found in the script folder. Make sure stock_data_clean_fixed.csv is next to this script.")
    raise SystemExit

print("Loading file ->", csv_path)
dataset = pd.read_csv(csv_path)

cols = [c.strip() for c in dataset.columns]
dataset.columns = cols

required = ["Open", "High", "Low", "Close", "Volume"]
for r in required:
    if r not in dataset.columns:
        print("Warning - missing column:", r)

try:
    df = dataset.dropna().reset_index(drop=True)
except:
    df = dataset.copy()

df["MA20"] = df["Close"].rolling(20, min_periods=1).mean()
df["MA50"] = df["Close"].rolling(50, min_periods=1).mean()
df["MA200"] = df["Close"].rolling(200, min_periods=1).mean()

def show_and_save(fig, filename):
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    print("Saved", filename)
    plt.show(block=False)
    plt.pause(0.1)

fig1, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df["Close"], label="Close")
ax1.plot(df["MA20"], label="MA20")
ax1.plot(df["MA50"], label="MA50")
ax1.plot(df["MA200"], label="MA200")
ax1.legend()
ax1.set_title("Close with Moving Averages")
show_and_save(fig1, "plot_full.png")

fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.plot(df["Close"])
ax2.set_yscale("log")
ax2.set_title("Close (Log Scale)")
show_and_save(fig2, "plot_full_log.png")

n = min(1000, len(df))
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.bar(range(n), df["Volume"].iloc[:n], alpha=0.3)
ax3_t = ax3.twinx()
ax3_t.plot(df["Close"].iloc[:n], color="red")
ax3.set_title("Volume vs Close")
show_and_save(fig3, "plot_volume.png")

X = df[["Open","High","Low","Volume"]]
y = df["Close"]

split = int(len(X)*0.8)
X_train = X[:split]
X_test = X[split:]
y_train = y[:split]
y_test = y[split:]

model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
rmse = mean_squared_error(y_test, preds)**0.5

print("RMSE:", rmse)

fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.plot(y_test.values, label="Actual")
ax4.plot(preds, label="Predicted")
ax4.legend()
ax4.set_title("Predicted vs Actual")
show_and_save(fig4, "plot_pred_vs_actual.png")

pd.DataFrame({"Actual":y_test.values,"Predicted":preds}).to_csv("predictions.csv", index=False)
print("Saved predictions.csv")

input("All windows open. Press ENTER to exit...")
plt.close("all")
