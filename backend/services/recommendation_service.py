from ai_modules.semantic_matcher import match_careers

def get_career_recommendations(user_input, careers):
    recommendations = match_careers(user_input, careers)
    return recommendations