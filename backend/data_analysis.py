import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "amazon_cleaned.csv")
df = pd.read_csv(csv_path)
choice_df = df[['final_category']].value_counts()

top_10 = df['final_category'].value_counts().head(10)

ax = top_10.plot(kind='bar', figsize=(10, 6), color='skyblue', title='Top 10 Most Frequent Categories')
ax.set_xlabel("Category")
ax.set_ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

image_path = os.path.join(BASE_DIR, "..", "data", "top_10_categories.png")
plt.savefig(image_path)