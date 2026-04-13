# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

This recommender suggests the top 5 songs from a small CSV catalog using a transparent weighted score. It assumes each user can be represented by genre, mood, target energy, and acoustic preference. This is for classroom exploration and debugging recommender logic, not for production use.

---

## 3. How the Model Works  

Each song has attributes such as genre, mood, energy, and acousticness. A user profile provides preferred genre, preferred mood, desired energy level, and whether acoustic songs are preferred. The model gives fixed points for genre/mood matches and partial points for numeric closeness (energy and acoustic fit). After scoring every song, it ranks all songs from highest to lowest and returns the top 5 with plain-language reasons.

---

## 4. Data  

The catalog contains 18 songs in [data/songs.csv](data/songs.csv). It includes genres such as pop, lofi, rock, jazz, synthwave, indie pop, r&b, electronic, world, classical, hip hop, metal, house, folk, and ambient, with moods like happy, chill, intense, focused, moody, calm, and nostalgic. I expanded the starter catalog with additional rows to improve diversity. The dataset is still small and does not include lyrics, language, cultural context, or listening-session behavior.

---

## 5. Strengths  

The system works well for clear preference profiles such as “High-Energy Pop,” “Chill Lofi,” and “Deep Intense Rock.” It captures intuitive patterns: high energy profiles receive energetic tracks, and acoustic-friendly profiles move toward more acoustic songs. Because reasons are printed for each recommendation, it is easy to inspect why a result appeared.

---

## 6. Limitations and Bias 

One weakness is that genre matching is a large fixed bonus, which can dominate outcomes and reduce discovery. In the adversarial profile (`genre=lofi`, `mood=sad`, `energy=0.9`), the model still returned multiple lofi songs even though their energy is far from the target, because genre points outweigh contradictory signals. This can create a filter bubble where users keep seeing familiar genre labels instead of better mood/energy fits. Another limitation is sparse mood coverage (for example, “sad” is underrepresented), which pushes the model to rely on whichever signals are available. Finally, the model ignores context features like time of day, recent skips, and novelty, so it may repeat similar songs too often.

---

## 7. Evaluation  

I tested five scenarios in the CLI: High-Energy Pop, Chill Lofi, Deep Intense Rock, an adversarial conflicting profile, and an energy-heavy weight-shift experiment. I looked for whether top songs matched common-sense vibe expectations and whether reasons aligned with score math. The strongest result was profile alignment: “Library Rain”/“Midnight Coding” rose for Chill Lofi, and “Storm Runner” rose for Deep Intense Rock. The biggest surprise was adversarial behavior: lofi songs still ranked high despite poor energy match because genre had a strong fixed weight. In the weight-shift experiment (half genre, double energy), rankings became more energy-driven and more diverse, with non-pop high-energy songs moving upward.

---

## 8. Future Work  

I would add diversity constraints so the top 5 cannot be dominated by one genre or artist. I would also include recency and skip-rate style feedback to simulate collaborative signals. Another improvement is dynamic weight tuning per user rather than one global setting. Finally, I would support multi-objective ranking (match quality + novelty + diversity) for less repetitive results.

---

## 9. Personal Reflection  

I learned that even a simple weighted scorer can feel surprisingly realistic when the data fields are meaningful. I also learned how small weight changes can produce noticeably different recommendation lists. This project made me more aware that real apps are not just “smart”; they are strongly shaped by data coverage and design choices, and those choices can accidentally narrow what users discover.
