# Phase 4 Profile Comparison Notes

Profiles compared:
- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Adversarial: High-Energy Sad Acoustic

## Pairwise comments

1. High-Energy Pop vs Chill Lofi
- High-Energy Pop ranks bright, energetic songs (for example, "Sunrise City" and "Gym Hero").
- Chill Lofi ranks lower-energy, acoustic-leaning songs (for example, "Library Rain" and "Midnight Coding").
- This makes sense because the energy target is much lower and `likes_acoustic=True` for Chill Lofi.

2. High-Energy Pop vs Deep Intense Rock
- Both profiles prefer high-energy songs, so there is overlap in energetic tracks.
- The top-1 changes from "Sunrise City" (pop/happy) to "Storm Runner" (rock/intense) because genre and mood bonuses shift.
- This shows categorical features (genre/mood) can redirect results even when energy is similar.

3. High-Energy Pop vs Adversarial
- The adversarial profile still ranks lofi songs highly because of the strong genre bonus.
- Energy target is high in adversarial mode, but mood "sad" has weak support in the dataset.
- This exposes a bias: genre can overpower contradictory preferences.

4. Chill Lofi vs Deep Intense Rock
- Chill Lofi output centers on calm, low-energy, acoustic tracks.
- Deep Intense Rock output centers on high-energy tracks, especially intense ones.
- The two lists diverge strongly, which is expected given opposite energy and mood targets.

5. Chill Lofi vs Adversarial
- Both include lofi songs near the top because both profiles ask for lofi genre.
- However, adversarial scores are lower quality in vibe consistency because high energy and acoustic/sad signals conflict.
- This suggests the model lacks a conflict penalty when preferences are internally inconsistent.

6. Deep Intense Rock vs Adversarial
- Deep Intense Rock ranks "Storm Runner" first due to exact genre+mood+energy alignment.
- Adversarial ranking shifts toward lofi songs despite poor energy match because genre points are fixed and large.
- This confirms that weight design can create unintuitive results for unusual profiles.
