from ursina import *

### <-------------- SCORES --------------> ###
POINTS_DEBRIS = 1
POINTS_PLANT = 5
POINTS_HAZARD = -10
### <-------------- SCORES --------------> ###

score = 0
score_text = Text(text="Score: 0",
                  position=(-0.85, 0.45),
                  scale=2,
                  color=color.white)

def add_score(amount, reason=""):
    global score
    score += amount
    sign = "+" if amount >= 0 else ""
    score_text.text = f"Score: {score}"
    if reason:
        print(f"{sign}{amount} ({reason}) -> total: {score}")

#©Vardan Grigoryan