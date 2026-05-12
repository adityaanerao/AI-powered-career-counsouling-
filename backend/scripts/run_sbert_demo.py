from ai_modules.semantic_matcher import SemanticMatcher

# Sample data
user_profile = "I like technology, coding, and problem solving"

career_descriptions = [
    "Software Engineer requires programming and analytical skills",
    "Graphic Designer focuses on creativity and visual design",
    "Mechanical Engineer works with machines and manufacturing"
]

matcher = SemanticMatcher()
results = matcher.match_careers(user_profile, career_descriptions)

print("Top career matches:")
for index, score in results:
    print(index, score)
