import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 1. Load your four CSV files
df1 = pd.read_csv('cnbc_news.csv')
df2 = pd.read_csv('cnn_news.csv')
df3 = pd.read_csv('guardian_news.csv')
df4 = pd.read_csv('bbc_news.csv')

# 2. Combine into one DataFrame
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

print("Available columns in CSV:", df.columns.tolist())  # Debugging line

# 3. Combine title and summary if available
if 'summary' in df.columns:
    df['text'] = df['title'].fillna('') + ' ' + df['summary'].fillna('')
else:
    df['text'] = df['title'].fillna('')

# Handle missing categories
df['category'] = df['category'].fillna("Unknown")

# 4. TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(df['text'])

# 5. K-Means clustering into 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# 6. Cross-tabulation: cluster vs. actual category
ct = pd.crosstab(df['cluster'], df['category'])
print("\nCluster vs. Actual Category:\n", ct)

# 7. Sample headlines per cluster
print("\nSample Headlines per Cluster:")
for cluster_label in sorted(df['cluster'].unique()):
    print(f"\nCluster {cluster_label} (n={len(df[df['cluster'] == cluster_label])} items):")
    sample = df[df['cluster'] == cluster_label][['title', 'category']].head(5)
    print(sample.to_string(index=False))

# 8. Save each (category, cluster) group to its own CSV
output_dir = "clustered_outputs"
os.makedirs(output_dir, exist_ok=True)

for (category, cluster), group in df.groupby(['category', 'cluster']):
    safe_category = str(category).strip().replace("/", "_").replace("\\", "_").replace(" ", "_")
    filename = f"{output_dir}/{safe_category}_cluster_{cluster}.csv"
    try:
        group.to_csv(filename, index=False)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

print("\n✅ Clustered files saved by Category and Cluster in 'clustered_outputs/' folder.")
