from .models import alert_dict, problem_dict, negative_dict, priority_thresholds

def score(score_alert: int, score_problem:int, score_negative:int) -> float:
    return score_alert*0.2 + score_problem - score_negative # For problem and negative value is * 1/-1

def score_alert(words: set) -> int:
    return sum(value for key, value in alert_dict.items() if key in words)

def score_problem(words: list) -> tuple:
    problem_count = {}
    for word in words:
        problem_count[word] = problem_count.get(word, 0) + 1
    score_value = 0
    for key, value in problem_count.items():
        multiplier = min(value, 3)
        score_value += problem_dict[key] * multiplier
    return (score_value, problem_count)

def score_negative(words: set) -> int:
    return sum(value for key, value in negative_dict.items() if key in words)

def score_critical(score:float, problem_count:dict) -> str:
    if not problem_count:
        return "problem don't found"
    for key, value in problem_count.items():
        if problem_dict[key] >= 130:
            return "critical"
    if len(problem_count) > 2:
        return "critical"
    for level_name, max_score in priority_thresholds:
        if score <= max_score:
            return level_name
    return "critical"

