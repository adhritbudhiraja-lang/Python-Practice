# Stock Price Prediction Project

## How to Use

This project automatically detects and loads all CSV files in the project folder and concatenates them into one dataset.

Files currently included:
- stock_data_1.csv
- stock_data_2.csv

1. Put your CSV files (Date, Open, High, Low, Close, Volume) into this folder:
   /mnt/data/stock_project

2. Run the script:
   python stock_prediction.py

3. Output:
   - The script prints found CSV files and the combined data shape
   - A closing price graph (first 200 rows)
   - Model RMSE

Notes:
- CSV files will be concatenated in alphabetical order.
- All CSVs should share the same column layout. If they don't, open them and make their columns consistent.

