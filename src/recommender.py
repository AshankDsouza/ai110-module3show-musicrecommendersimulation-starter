from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = self._score_song(user, song)
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score_song(user, song)
        if not reasons:
            return "General similarity to your listening profile."
        return "; ".join(reasons)

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        # Weighted feature matches
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match (+2.00)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append("mood match (+1.00)")

        energy_closeness = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        energy_points = 1.5 * energy_closeness
        score += energy_points
        reasons.append(f"energy closeness {energy_closeness:.2f} (+{energy_points:.2f})")

        prefers_acoustic = 1.0 if user.likes_acoustic else 0.0
        acoustic_closeness = 1.0 - abs(song.acousticness - prefers_acoustic)
        acoustic_points = 0.5 * acoustic_closeness
        score += acoustic_points
        reasons.append(f"acoustic fit {acoustic_closeness:.2f} (+{acoustic_points:.2f})")

        return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into typed dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the given user preference profile."""
    score = 0.0
    reasons: List[str] = []

    preferred_genre = str(user_prefs.get("genre", "")).lower()
    preferred_mood = str(user_prefs.get("mood", "")).lower()
    target_energy = float(user_prefs.get("energy", 0.5))
    likes_acoustic: Optional[bool] = user_prefs.get("likes_acoustic")
    w_genre = float(user_prefs.get("w_genre", 2.0))
    w_mood = float(user_prefs.get("w_mood", 1.0))
    w_energy = float(user_prefs.get("w_energy", 1.5))
    w_acoustic = float(user_prefs.get("w_acoustic", 0.5))

    # 1) Genre match weight
    if str(song.get("genre", "")).lower() == preferred_genre and preferred_genre:
        score += w_genre
        reasons.append(f"genre match (+{w_genre:.2f})")

    # 2) Mood match weight
    if str(song.get("mood", "")).lower() == preferred_mood and preferred_mood:
        score += w_mood
        reasons.append(f"mood match (+{w_mood:.2f})")

    # 3) Energy closeness weight
    song_energy = float(song.get("energy", 0.0))
    energy_closeness = max(0.0, 1.0 - abs(song_energy - target_energy))
    energy_points = w_energy * energy_closeness
    score += energy_points
    reasons.append(f"energy closeness {energy_closeness:.2f} (+{energy_points:.2f})")

    # 4) Optional acoustic preference
    if likes_acoustic is not None:
        acoustic_target = 1.0 if likes_acoustic else 0.0
        acousticness = float(song.get("acousticness", 0.5))
        acoustic_closeness = 1.0 - abs(acousticness - acoustic_target)
        acoustic_points = w_acoustic * acoustic_closeness
        score += acoustic_points
        reasons.append(f"acoustic fit {acoustic_closeness:.2f} (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top-k recommendations."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "General profile similarity"
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
