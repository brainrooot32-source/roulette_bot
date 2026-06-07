import random
from dataclasses import dataclass
from typing import List

@dataclass
class Segment:
    prize_stars: int
    probability: float
    color: str

WHEEL_SEGMENTS = [
    Segment(15,  0.14, "#FF6B6B"),
    Segment(15,  0.14, "#FF8E8E"),
    Segment(25,  0.27, "#4ECDC4"),
    Segment(25,  0.27, "#6ED8D1"),
    Segment(50,  0.06, "#45B7D1"),
    Segment(50,  0.06, "#6AC5D8"),
    Segment(100, 0.03, "#96CEB4"),
    Segment(100, 0.03, "#AAD8C4"),
]

WEIGHTS = [s.probability for s in WHEEL_SEGMENTS]

def spin_wheel() -> dict:
    index = random.choices(range(len(WHEEL_SEGMENTS)), weights=WEIGHTS, k=1)[0]
    segment = WHEEL_SEGMENTS[index]
    return {
        "segment_index": index,
        "prize_stars": segment.prize_stars,
    }