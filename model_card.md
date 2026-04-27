# 🎧 Model Card: Music Recommender Simulation

## Model Name

VibeFinder 2.0

## Goal / Task

The system suggests the top 5 songs for a user profile.  
It predicts which songs are the best fit based on vibe features.

Additionally, as part of the final project it also:
i. Fecthes the top 3 most similar songs to the songs being listed through a semantic vector search using postgresql's pgvector extension.
ii. Uses the some of the above data in i. to do a RAG based description of the song using an LLM running on one of the docker containers

## Data Used

I used a small CSV catalog with 18 songs in [data/songs.csv](data/songs.csv).  
Main features are `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

Limits:
- Small dataset size
- Some moods are underrepresented (like `sad`)
- No lyrics, language, or listening-history behavior

## Algorithm Summary

The model gives points for exact matches and closeness.

- Genre match adds a strong bonus.
- Mood match adds a medium bonus.
- Energy adds partial points based on closeness to target.
- Acousticness adds partial points based on user preference.

Then it scores every song, sorts by highest score, and returns top 5 with reasons.

## Observed Behavior / Biases

The system can over-prioritize genre.  
In conflicting profiles, songs with the right genre can still rank high even when mood or energy is a weaker fit.

This can create a filter bubble:
- Similar genres repeat often
- Discovery is limited
- Underrepresented moods get weaker results

## Evaluation Process

I tested multiple profiles in the CLI:
- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Adversarial conflicting profile
- Weight-shift experiment (less genre, more energy)

I compared top 5 outputs and checked whether the reasons matched the score math.  
I also compared outputs across profiles in [reflection.md](reflection.md).

## Intended Use and Non-Intended Use

Intended use:
- Classroom simulation
- Learning how recommenders convert user preferences into ranked outputs
- Debugging simple scoring logic

Non-intended use:
- Real user recommendations at scale
- High-stakes or fairness-sensitive decisions
- Personalized production systems without stronger data and validation

## Ideas for Improvement

1. Add diversity rules so results are not dominated by one genre or artist.
2. Add feedback signals (skip/save/like) to mimic collaborative behavior.
3. Add per-user adaptive weights instead of one fixed weighting style.

## Personal Reflection

My biggest learning moment was seeing how one weight change can reorder the full top 5 list.  
AI tools helped me move faster, especially for drafting code and testing profile ideas, but I had to double-check math and assumptions.

What surprised me most is that a simple weighted algorithm can still feel “smart” to a user.  
If I continue this project, I would add diversity-aware ranking and a mixed content + behavior approach.
