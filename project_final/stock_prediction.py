import pandas as pd
import glob, os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# --- 1. SETUP DEVICE (GPU vs CPU) ---
# This checks if Cuda (Nvidia) or MPS (Mac) is available
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

def find_csv_in_folder(folder):
    paths = sorted(glob.glob(os.path.join(folder, "*.csv")))
    paths = [p for p in paths if os.path.basename(p).lower() not in ("predictions.csv","data_summary.csv")]
    if not paths:
        return []
    for p in paths:
        if os.path.basename(p).lower() == "stock_data.csv":
            return [p]
    return paths

def plot_close(data, show=True):
    plt.figure()
    plt.plot(data['Close'])
    plt.title("Closing Price Trend")
    plt.xlabel("Row index")
    plt.ylabel("Close price")
    plt.tight_layout()
    if show:
        plt.show()

# --- 2. DEFINE PYTORCH MODEL ---
class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim):
        super(LinearRegressionModel, self).__init__()
        # Linear layer: takes 'input_dim' features, outputs 1 value (Price)
        self.linear = nn.Linear(input_dim, 1)

    def forward(self, x):
        return self.linear(x)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-show", action="store_true", help="Do not display plot windows")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    csvs = find_csv_in_folder(script_dir)
    if not csvs:
        raise FileNotFoundError(f"No CSV found in {script_dir}")
    chosen = csvs[0]
    print("Loading:", chosen)
    
    # Load Data
    data = pd.read_csv(chosen)
    required = ['Open','High','Low','Close','Volume']
    for c in required:
        if c not in data.columns:
            raise ValueError(f"Missing column: {c}")
    data = data.dropna(subset=required).reset_index(drop=True)

    plot_close(data, show=not args.no_show)

    # --- 3. PREPROCESSING (CRITICAL FOR PYTORCH) ---
    X_raw = data[['Open','High','Low','Volume']].values
    y_raw = data['Close'].values.reshape(-1, 1)

    # Split data first
    X_train_raw, X_test_raw, y_train_raw, y_test_raw = train_test_split(X_raw, y_raw, test_size=0.2, shuffle=False)

    # Scale Data: Neural networks struggle with big numbers (like Volume). 
    # We scale everything to be roughly around 0.
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    X_train_scaled = scaler_x.fit_transform(X_train_raw)
    X_test_scaled = scaler_x.transform(X_test_raw)
    
    y_train_scaled = scaler_y.fit_transform(y_train_raw)
    # Note: We don't fit scaler_y on test data, only transform!

    # --- 4. CONVERT TO TENSORS & MOVE TO GPU ---
    # Convert numpy arrays to Torch Tensors and push to the 'device' (GPU)
    X_train = torch.tensor(X_train_scaled, dtype=torch.float32).to(device)
    y_train = torch.tensor(y_train_scaled, dtype=torch.float32).to(device)
    X_test = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)

    # --- 5. INITIALIZE MODEL ---
    model = LinearRegressionModel(input_dim=4).to(device)
    
    # Loss and Optimizer
    criterion = nn.MSELoss()
    # Adam is usually better/faster than SGD for this without tuning
    optimizer = optim.Adam(model.parameters(), lr=0.01) 

    # --- 6. TRAINING LOOP ---
    epochs = 1000
    print("Training on GPU...")
    model.train() # Set to training mode
    for epoch in range(epochs):
        # Forward pass
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        
        # Backward pass and optimization
        optimizer.zero_grad() # Clear old gradients
        loss.backward()       # Calculate new gradients
        optimizer.step()      # Update weights

        if (epoch+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

    # --- 7. PREDICTION ---
    model.eval() # Set to evaluation mode
    with torch.no_grad(): # Disable gradient calculation for speed
        predicted_scaled = model(X_test)
        
        # Move predictions back to CPU to save to CSV
        predicted_scaled_cpu = predicted_scaled.cpu().numpy()

    # Inverse transform to get actual prices back (undo the scaling)
    preds = scaler_y.inverse_transform(predicted_scaled_cpu)

    # Calculate RMSE (Using the original unscaled Y test data)
    rmse = np.sqrt(np.mean((y_test_raw - preds) ** 2))
    print(f"RMSE: {rmse:.4f}")

    # Save results
    out = os.path.join(script_dir,"predictions_gpu.csv")
    # We create a clean DataFrame for output
    res = pd.DataFrame(X_test_raw, columns=['Open','High','Low','Volume'])
    res['Actual'] = y_test_raw
    res['Predicted'] = preds
    res.to_csv(out, index=False)
    print("Saved predictions to", out)

if __name__ == "__main__":
    main()