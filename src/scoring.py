
TRY_MULTIPLIER= {

    1 : 1,
    2 : 0.7,
    3 : 0.4

}


RECENCY_WEIGHT = 0.4



def update_mastery(old_mastery, attempt_score, has_history):
    if not has_history:
        return attempt_score
    return (1 - RECENCY_WEIGHT) * old_mastery + RECENCY_WEIGHT * attempt_score

def compute_attempt_score(confidence, tries_used, solved):
    confidence = max(0, min(100, confidence))
    if solved:
        multiplier = TRY_MULTIPLIER.get(tries_used, 0.4)
        raw = confidence * multiplier
    else:
        raw = -confidence
    return (raw + 100) / 2  # map [-100, 100] onto [0, 100]