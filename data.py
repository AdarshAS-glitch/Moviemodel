import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
# Save as CSV
#df = pd.read_excel('movies_dataset.xlsx', engine='openpyxl')
#df.to_csv('results_with_crew.csv', index=False)

# Step 1: Load the dataset
df = pd.read_csv("results_with_crew.csv")

# Step 2: Assign proper column names if not already present
df.columns = [
    "id", "title", "year", "duration", "rating", "votes", "revenue",
    "director", "writer", "genre", "imdb_link_id", "imdb_link_title"
]

# Step 3: Clean HTML tags from IMDb link columns
df["imdb_link_id"] = df["imdb_link_id"].apply(lambda x: re.search(r'tt\d+', str(x)).group() if pd.notnull(x) else x)
df["imdb_link_title"] = df["imdb_link_title"].apply(lambda x: re.search(r'>(.*?)<', str(x)).group(1) if pd.notnull(x) else x)

# Step 4: Check basic info and missing values
print("🔍 Dataset Info:")
print(df.info())

print("\n🧹 Missing Values:")
print(df.isnull().sum())

print("\n📊 Descriptive Statistics:")
print(df.describe())

# Step 5: Top 10 movies by rating
top_rated = df.sort_values(by="rating", ascending=False).head(10)
print("\n⭐ Top 10 Rated Movies:")
print(top_rated[["title", "rating", "year", "genre"]])

# Step 6: Plot - Rating vs Revenue
plt.figure(figsize=(10, 6))
sns.scatterplot(x="revenue", y="rating", data=df)
plt.title("Revenue vs Rating", fontsize=16)
plt.xlabel("Revenue (in millions)")
plt.ylabel("IMDb Rating")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 7: Plot - Top 10 Directors by Average Rating
top_directors = df.groupby("director")["rating"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_directors.values, y=top_directors.index, palette="magma")
plt.title("Top 10 Directors by Average IMDb Rating", fontsize=16)
plt.xlabel("Average Rating")
plt.ylabel("Director")
plt.tight_layout()
plt.show()
