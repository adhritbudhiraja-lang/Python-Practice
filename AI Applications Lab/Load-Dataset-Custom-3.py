import pandas as pd
df = pd.read_csv(r"C:\Users\Adhrit\Desktop\Coding\Python\AI Applications Lab\cleaned_dataset.csv")
print(df.to_string())
print("\n")
print(df.info())
print("\n")
print(df.describe())
print("\n")
print(df.isnull) # Check for missing values
print("\n")
print(df.corr) # Correlation matrix 