"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top recommendations for one named profile."""
    print(f"\n=== Profile: {name} ===")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{idx}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        (
            "High-Energy Pop",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.8,
                "likes_acoustic": False,
            },
        ),
        (
            "Chill Lofi",
            {
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.35,
                "likes_acoustic": True,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.92,
                "likes_acoustic": False,
            },
        ),
        (
            "Adversarial: High-Energy Sad Acoustic",
            {
                "genre": "lofi",
                "mood": "sad",
                "energy": 0.9,
                "likes_acoustic": True,
            },
        ),
        (
            "Experiment: Energy-heavy High-Energy Pop",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.8,
                "likes_acoustic": False,
                # Weight-shift experiment: half genre, double energy
                "w_genre": 1.0,
                "w_energy": 3.0,
            },
        ),
    ]

    for name, user_prefs in profiles:
        run_profile(name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
