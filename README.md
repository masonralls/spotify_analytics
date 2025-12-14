**Spotify Listening Behavior Analysis (Unsupervised Learning)**

This project analyzes personal Spotify listening history using unsupervised machine learning to identify behavioral patterns in music consumption. Rather than relying on audio features, the analysis focuses on engagement behavior, enabling interpretable insights into listening intent across time and context.


**Methodology**

Data Pipeline

- Built ETL pipelines to extract Spotify listening history and store normalized data in PostgreSQL

- Queried relational tables (tracks, artists, sessions) directly into Python for analysis

Session Modeling

- Constructed listening sessions using time gaps (>30 minutes)

- Engineered behavioral features including session duration, repetition ratio, and time of day

Unsupervised Learning

- Applied KMeans clustering with silhouette analysis to identify:

- Distinct listening modes (session-level)

- Distinct artist engagement types (artist-level)


**Key Findings**

Listening Modes

- Quick check-ins

- Late-night focused sessions

- Extended immersive listening

- Comfort / repeat listening

Artist Engagement Types

- Burst-listened artists

- Short-term interests

- Light exploration

- Core rotation artists

Behavioral Insights

- Exploratory listening dominates most contexts, including immersive and late-night sessions

- Extended sessions are driven more by discovery than repetition

- Artist engagement is often burst-based rather than sustained over time

- Listening intent varies strongly by context despite consistent exploratory behavior


**Tech Stack**

- Python (pandas, NumPy, scikit-learn)

- PostgreSQL (ETL, relational modeling)

- KMeans, silhouette analysis

- Matplotlib / Seaborn

- Jupyter, SQLAlchemy


**Why This Matters**

- This project demonstrates how behavioral patterns can be uncovered without content-based features, highlighting the value of unsupervised learning for interpretability, user modeling, and exploratory analysis.
