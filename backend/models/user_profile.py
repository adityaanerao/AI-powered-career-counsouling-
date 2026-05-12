class UserProfile:
    def __init__(self, name, email, interests):
        self.name = name
        self.email = email
        self.interests = interests

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "interests": self.interests
        }