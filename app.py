import pandas as pd 
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


file_path = os.path.join(os.path.dirname(__file__), "imdb_top_1000.csv")
df = pd.read_csv("imdb_top_1000.csv")

st.title("Movie Review Analyzer")
df.columns = df.columns.str.strip()

# remove extra spaces and split by comma
df['genre'] = df['genre'].str.split(', ')

# create one row per genre
df_exploded = df.explode('genre')

#plot
fig, ax = plt.subplots()
df['rating'].value_counts().sort_index().plot(kind='bar', ax=ax, color="#F4C2C2")

#labels
ax.set_title("Distribution of Movie Ratings")
ax.set_xlabel("Rating (Rounded)")
ax.set_ylabel("Number of Movies")

st.pyplot(fig)

#box plot - genre vs rating
plt.figure(figsize=(14, 6))
sns.boxplot(x='genre', y='rating', data=df_exploded, color = '#026023')

plt.xticks(rotation=45)
plt.title('Movie Ratings by Genre')
plt.xlabel('Genre')
plt.ylabel('Rating')

plt.tight_layout()
st.pyplot(plt)

#avg rating per genre
genre_avg = (
    df_exploded
    .groupby('genre')['rating']
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))
genre_avg.plot(kind='bar', color = "#722C9E")

plt.title('Average Movie Rating by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Rating')

plt.tight_layout()
st.pyplot(plt)

# --- SEARCH FEATURE ---
st.subheader("Search for a Movie")
search_query = st.text_input("Enter a movie title:", placeholder="e.g. Inception")

if search_query:
    # This looks for the title regardless of capital letters
    result = df[df['movie'].str.contains(search_query, case=False, na=False)]
    
    if not result.empty:
        # If we find movies, show the first one's stats in a nice way
        movie = result.iloc[0]
        st.success(f"**{movie['movie']}**")
        col_img, col_info = st.columns([1, 2])

        with col_img:
            # Check if poster_link exists and show it
            if 'Poster_Link' in movie:
                st.image(movie['Poster_Link'], width=200)
        
        with col_info:
            st.metric("IMDb Rating", f"⭐ {movie['rating']}")
            st.write(f"**Released:** {movie['Released_Year']}")
            st.write(f"**Genre:** {', '.join(movie['genre']) if isinstance(movie['genre'], list) else movie['genre']}")
            st.write(f"**Overview:** {movie['Overview']}")
        
        current_genre = (
        movie['genre'][0]
        if isinstance(movie['genre'], list) 
        else movie['genre'].split(',')[0]
        )
        recommendations = (
            df_exploded[df_exploded['genre'] == current_genre]
            .drop_duplicates(subset='movie')
            .sample(min(3, len(df_exploded))))
        st.write("### You might also like:")
        cols = st.columns(3)
        for i, (idx, rec) in enumerate(recommendations.iterrows()):
            with cols[i]:
                st.image(rec['Poster_Link'], caption=rec['movie'])

    else:
        st.warning("couldn't find that movie, try again")
