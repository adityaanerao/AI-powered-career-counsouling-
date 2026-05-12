class Career:
    def __init__(self, name, description, skills):
        self.name = name
        self.description = description
        self.skills = skills

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "skills": self.skills
        }