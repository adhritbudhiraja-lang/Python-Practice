import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")
df = pd.read_csv(r"C:\Users\Adhrit\Desktop\Coding\Python\AI Applications Lab\Project\Resume.csv")
if 'Resume_html' in df.columns:
    df.drop(columns=['Resume_html'], inplace=True)
category_counts = df['Category'].value_counts()
plt.figure(figsize=(14, 6))
sns.barplot(x=category_counts.values, y=category_counts.index, palette="viridis")
plt.title("Resume Category Distribution", fontsize=14, fontweight='bold')
plt.xlabel("Number of Resumes")
plt.ylabel("Job Category")
plt.tight_layout()
df['resume_length'] = df['Resume_str'].apply(lambda x: len(x.split()))
plt.figure(figsize=(10, 5))
sns.histplot(df['resume_length'], bins=40, kde=True, color='steelblue')
plt.title("Distribution of Resume Word Count", fontsize=14, fontweight='bold')
plt.xlabel("Number of Words")
plt.ylabel("Frequency")
plt.tight_layout()
def clean_resume(text):
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text
df['cleaned_resume'] = df['Resume_str'].apply(clean_resume)
SUITABLE_CATEGORIES = [
    'INFORMATION-TECHNOLOGY',
    'ENGINEERING',
    'BANKING',
    'FINANCE',
    'CONSULTANT',
    'BUSINESS-DEVELOPMENT',
    'DIGITAL-MEDIA',
    'AUTOMOBILE',
]
df['label'] = df['Category'].apply(lambda x: 1 if x in SUITABLE_CATEGORIES else 0)
label_counts = df['label'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(
    label_counts.values,
    labels=['Suitable', 'Unsuitable'],
    autopct='%1.1f%%',
    colors=['#4CAF50', '#F44336'],
    startangle=90
)
plt.title("Suitable vs Unsuitable Resumes", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()