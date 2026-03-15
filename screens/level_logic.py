

LEVELS = [
    (0,    "BEGINNER",   "🌱"),
    (100,  "ROOKIE",     "⚡"),
    (300,  "FIGHTER",    "🥊"),
    (600,  "ATHLETE",    "🏋️"),
    (1000, "WARRIOR",    "⚔️"),
    (1500, "CHAMPION",   "🏆"),
    (2500, "ELITE",      "💎"),
    (4000, "LEGEND",     "👑"),
]

BADGES = [
    ("first_workout",  "🎯", "First Step",      "Complete your first workout",         lambda s: s["total_sessions"] >= 1),
    ("rep_10",         "💪", "10 Reps",         "Do 10 total reps",                    lambda s: s["total_reps"] >= 10),
    ("rep_50",         "🔥", "On Fire",         "Do 50 total reps",                    lambda s: s["total_reps"] >= 50),
    ("rep_100",        "💯", "Century",         "Do 100 total reps",                   lambda s: s["total_reps"] >= 100),
    ("rep_500",        "⚡", "Unstoppable",     "Do 500 total reps",                   lambda s: s["total_reps"] >= 500),
    ("rep_1000",       "👑", "Legend",          "Do 1000 total reps",                  lambda s: s["total_reps"] >= 1000),
    ("streak_3",       "📅", "3 Day Streak",    "Workout 3 days in a row",             lambda s: s["best_streak"] >= 3),
    ("streak_7",       "🗓️", "Week Warrior",    "Workout 7 days in a row",             lambda s: s["best_streak"] >= 7),
    ("streak_30",      "🌙", "Iron Discipline", "Workout 30 days in a row",            lambda s: s["best_streak"] >= 30),
    ("sessions_10",    "🎖️", "Dedicated",       "Complete 10 sessions",                lambda s: s["total_sessions"] >= 10),
    ("sessions_50",    "🏅", "Veteran",         "Complete 50 sessions",                lambda s: s["total_sessions"] >= 50),
    ("perfect_form",   "✨", "Perfect Form",    "Get 100% form accuracy in a session", lambda s: s["best_accuracy"] >= 100),
]


def get_level_info(total_reps):
    """Returns (level_index, title, emoji, current_xp, xp_for_next, progress_pct)"""
    xp = total_reps  

    current_level = 0
    for i, (req, title, emoji) in enumerate(LEVELS):
        if xp >= req:
            current_level = i

    level_idx   = current_level
    title       = LEVELS[level_idx][1]
    emoji       = LEVELS[level_idx][2]
    current_req = LEVELS[level_idx][0]

    if level_idx + 1 < len(LEVELS):
        next_req  = LEVELS[level_idx + 1][0]
        xp_in_level     = xp - current_req
        xp_needed       = next_req - current_req
        progress_pct    = int((xp_in_level / xp_needed) * 100)
        progress_pct    = max(0, min(100, progress_pct))
    else:
        next_req     = current_req
        xp_in_level  = xp - current_req
        xp_needed    = 0
        progress_pct = 100

    return level_idx, title, emoji, xp_in_level, xp_needed, progress_pct


def get_earned_badges(stats):
    """Returns list of earned badge dicts"""
    earned = []
    for badge_id, emoji, name, desc, condition in BADGES:
        if condition(stats):
            earned.append({
                "id":    badge_id,
                "emoji": emoji,
                "name":  name,
                "desc":  desc,
            })
    return earned


def get_all_badges_with_status(stats):
    """Returns all badges with earned True/False"""
    all_badges = []
    for badge_id, emoji, name, desc, condition in BADGES:
        all_badges.append({
            "id":     badge_id,
            "emoji":  emoji,
            "name":   name,
            "desc":   desc,
            "earned": condition(stats),
        })
    return all_badges