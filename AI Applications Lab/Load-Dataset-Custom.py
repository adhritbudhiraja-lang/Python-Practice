import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset
file_path = r"C:\Users\Adhrit\Desktop\Coding\Python\AI Applications Lab\cleaned_dataset.csv"
df = pd.read_csv(file_path)

# --- VISUALIZATION SETUP ---
sns.set_theme(style="whitegrid")

# Figure 1: Correlation Heatmap
plt.figure(1, figsize=(10, 8)) # Number '1' identifies this specific window
numeric_df = df.select_dtypes(include=['number'])
# We use a subset or turn off annotations if there are too many columns
sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm') 
plt.title('Figure 1: Correlation Heatmap')

# Figure 2: Distribution of Streams
plt.figure(2, figsize=(10, 6))
sns.histplot(df['Stream'], kde=True, bins=30, color='green')
plt.title('Figure 2: Distribution of Streams')
plt.xlabel('Stream Count')
plt.ylabel('Frequency')

# Figure 3: Box Plot (Stream by Album Type)
plt.figure(3, figsize=(10, 6))
sns.boxplot(x='Album_type', y='Stream', data=df, palette='Set2')
plt.title('Figure 3: Stream Counts by Album Type')

# Figure 4: Scatter Plot (Views vs. Likes)
plt.figure(4, figsize=(10, 6))
sns.scatterplot(x='Views', y='Likes', data=df, alpha=0.6)
plt.title('Figure 4: Youtube Views vs. Likes')
plt.xlabel('Views')
plt.ylabel('Likes')

# Figure 5: Count Plot (Spotify vs Youtube)
plt.figure(5, figsize=(8, 5))
sns.countplot(x='most_playedon', data=df, palette='pastel')
plt.title('Figure 5: Count of Tracks by Platform')

# --- DISPLAY ALL PLOTS ---
print("All plots are now open. The script will finish when you close them.")
plt.show()