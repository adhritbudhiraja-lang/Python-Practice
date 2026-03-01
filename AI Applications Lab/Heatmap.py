import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv(r"C:\Users\Adhrit\Desktop\Coding\Python\AI Applications Lab\data.csv")
plt.figure(figsize = (8,6))
sns.heatmap(df.corr(),annot=True,cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show() 
plt.figure(figsize=(8,6))
sns.boxplot(data=df)
plt.title("Box Plot for All Numeric Columns")
plt.show() 