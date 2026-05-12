def generate_roadmap(career_name):

    roadmap = {
        "AI Engineer": [
            "Learn Python",
            "Learn Machine Learning",
            "Build AI Projects",
            "Learn Deep Learning"
        ],

        "Doctor": [
            "Prepare for NEET",
            "Complete MBBS",
            "Do Internship",
            "Choose Specialization"
        ],

        "Software Engineer": [
            "Learn Programming",
            "Practice DSA",
            "Build Projects",
            "Apply for Internships"
        ]
    }

    return roadmap.get(career_name, ["No roadmap available"])