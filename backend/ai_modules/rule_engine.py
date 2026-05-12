def filter_by_cutoff(percentile, colleges):
    eligible = []

    for college in colleges:
        if percentile >= college["cutoff"]:
            eligible.append(college)

    return eligible