import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import time

print("Script starting...")

Tk().withdraw()
csv_path = askopenfilename(
    title="Select your stock CSV file",
    filetypes=[("CSV files", "*.csv")]
)

if not csv_path:
    raise FileNotFoundError("No CSV selected.")

print("Loading file ->", csv_path)

dataset = pd.read_csv(csv_path)

cols = [c.strip() for c in dataset.columns]
dataset.columns = cols

required = ["Open", "High", "Low", "Close", "Volume"]
for r in required:
    if r not in dataset.columns:
        print("Missing column:", r)

try:
    df = dataset.dropna(subset=[c for c in required if c in dataset.columns]).reset_index(drop=True)
except:
    df = dataset.copy()

df["MA20"] = df["Close"].rolling(window=20, min_periods=1).mean()
df["MA50"] = df["Close"].rolling(window=50, min_periods=1).mean()
df["MA200"] = df["Close"].rolling(window=200, min_periods=1).mean()


def show_and_save(fig, name):
    fig.tight_layout()
    fig.savefig(name, dpi=150)
    print("Saved", name)
    plt.show(block=False)
    plt.pause(0.1)


fig1, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df["Close"], label="Close")
ax1.plot(df["MA20"], label="MA20")
ax1.plot(df["MA50"], label="MA50")
ax1.plot(df["MA200"], label="MA200")
ax1.set_title("Close with Moving Averages")
ax1.legend()
show_and_save(fig1, "plot_full.png")

fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.plot(df["Close"])
ax2.set_yscale("log")
ax2.set_title("Close (Log Scale)")
show_and_save(fig2, "plot_full_log.png")

fig3, ax3 = plt.subplots(figsize=(10,5))
n = min(1000, len(df))
ax3.bar(range(n), df["Volume"].iloc[:n], alpha=0.3)
ax3_t = ax3.twinx()
ax3_t.plot(df["Close"].iloc[:n], color="red")
ax3.set_title("Volume vs Close")
show_and_save(fig3, "plot_volume.png")

X = df[["Open","High","Low","Volume"]]
y = df["Close"]

split = int(len(X)*0.8)
X_train,X_test = X[:split],X[split:]
y_train,y_test = y[:split],y[split:]

model = LinearRegression()
model.fit(X_train,y_train)
preds = model.predict(X_test)

fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.plot(y_test.values, label="Actual")
ax4.plot(preds, label="Predicted")
ax4.legend()
ax4.set_title("Predicted vs Actual")
show_and_save(fig4, "plot_pred_vs_actual.png")

pd.DataFrame({"Actual":y_test.values,"Predicted":preds}).to_csv("predictions.csv", index=False)
print("Saved predictions.csv")

input("All plots open. Press ENTER to exit...")
plt.close('all')
