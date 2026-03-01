import os, glob, argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def find_csv(folder):
    paths = sorted(glob.glob(os.path.join(folder, "*.csv")))
    paths = [p for p in paths if os.path.basename(p).lower() not in ("predictions.csv","data_summary.csv")]
    for p in paths:
        if os.path.basename(p).lower() == "stock_data.csv":
            return p
    return paths[0] if paths else None

def ensure_cols(df):
    req = ['Open','High','Low','Close','Volume']
    missing = [c for c in req if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df

def compute_mas(df):
    df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
    df['MA50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['MA200'] = df['Close'].rolling(window=200, min_periods=1).mean()
    return df

def plot_and_save(fig, out_path, show):
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    print("Saved:", out_path)
    if show:
        plt.show()
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-plots", action="store_true", help="Display plots in windows")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = find_csv(script_dir)
    if not csv_path:
        raise FileNotFoundError("No CSV found in folder. Place your stock_data.csv here.")
    print("Loading:", csv_path)
    df = pd.read_csv(csv_path)
    df = ensure_cols(df)
    df = df.dropna(subset=['Open','High','Low','Close','Volume']).reset_index(drop=True)
    df = compute_mas(df)

    # Full series with MAs
    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(df['Close'], label='Close', linewidth=0.8)
    ax1.plot(df['MA20'], label='MA20', linewidth=0.9)
    ax1.plot(df['MA50'], label='MA50', linewidth=1.0)
    ax1.plot(df['MA200'], label='MA200', linewidth=1.2)
    ax1.set_title("Closing Price with Moving Averages")
    ax1.set_xlabel("Row index")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(alpha=0.3)
    plot_and_save(fig1, os.path.join(script_dir,"plot_full.png"), args.show_plots)

    # Log-scale full series (helps with big spikes)
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(df['Close'], label='Close', linewidth=0.8)
    ax2.set_yscale('log')
    ax2.set_title("Closing Price (Log scale)")
    ax2.set_xlabel("Row index")
    ax2.set_ylabel("Log Price")
    ax2.grid(alpha=0.3)
    plot_and_save(fig2, os.path.join(script_dir,"plot_full_log.png"), args.show_plots)

    # Volume bars + close overlay (first 1500 rows for readability)
    n = min(len(df), 1500)
    fig3, ax3 = plt.subplots(figsize=(12,5))
    ax3.bar(range(n), df['Volume'].iloc[:n], alpha=0.4, label='Volume')
    ax3_twin = ax3.twinx()
    ax3_twin.plot(df['Close'].iloc[:n], color='black', linewidth=0.8, label='Close')
    ax3.set_xlabel("Row index")
    ax3.set_ylabel("Volume")
    ax3_twin.set_ylabel("Close price")
    ax3.set_title("Volume (bars) and Close (line) - first {} rows".format(n))
    ax3.grid(alpha=0.2)
    plot_and_save(fig3, os.path.join(script_dir,"plot_volume.png"), args.show_plots)

    # Zoomed-in plots: early, middle, recent
    total = len(df)
    segments = {
        "early": (0, min(500, total)),
        "mid": (max(0, total//3), min(total//3 + 500, total)),
        "recent": (max(0, total-500), total)
    }
    for name, (s,e) in segments.items():
        if s >= e:
            continue
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(df['Close'].iloc[s:e], label='Close', linewidth=0.9)
        ax.plot(df['MA20'].iloc[s:e], label='MA20', linewidth=0.9)
        ax.set_title(f"{name.capitalize()} zoom ({s} to {e})")
        ax.set_xlabel("Row index (segment)")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(alpha=0.3)
        plot_and_save(fig, os.path.join(script_dir,f"plot_{name}.png"), args.show_plots)

    # Simple model and Pred vs Actual
    X = df[['Open','High','Low','Volume']]
    y = df['Close']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,shuffle=False)
    model = LinearRegression().fit(X_train,y_train)
    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test,preds)**0.5
    print(f"Model RMSE: {rmse:.4f}")

    # Pred vs Actual plot
    figp, axp = plt.subplots(figsize=(10,5))
    axp.plot(y_test.values, label='Actual', linewidth=0.9)
    axp.plot(preds, label='Predicted', linewidth=0.9)
    axp.set_title("Predicted vs Actual (test set)")
    axp.set_xlabel("Test sample index")
    axp.set_ylabel("Price")
    axp.legend()
    axp.grid(alpha=0.3)
    plot_and_save(figp, os.path.join(script_dir,"plot_pred_vs_actual.png"), args.show_plots)

    # Save predictions to CSV
    out = os.path.join(script_dir,"predictions.csv")
    res = X_test.copy()
    res['Actual'] = y_test.values
    res['Predicted'] = preds
    res.to_csv(out, index=False)
    print("Saved predictions to", out)

if __name__ == "__main__":
    main()
