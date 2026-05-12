from sentence_transformers import util

def calculate_similarity(embedding1, embedding2):
    similarity = util.cos_sim(embedding1, embedding2)
    return similarity.item()