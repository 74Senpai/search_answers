def get_texts_chunks(texts, size=250, befor_chunk_txt="", overlap_ratio=0):
    texts = texts.strip()
    if not texts:
        return []

    texts = texts.replace("\n", " ")
    float_char_count = int(size * overlap_ratio)
    step = size - float_char_count

    chunks = []
    len_txt = len(texts)

    for point in range(0, len_txt, step):
        chunk = befor_chunk_txt[-float_char_count:] + texts[point:point + step]
        chunks.append(chunk)
        befor_chunk_txt = chunk

    return chunks


def parse_chunks_data(chunks_data):
    import json
    import numpy as np
    if not chunks_data:
        return []
    res = []
    
    for chunk_data in chunks_data:
        chunk = {
            "id_vector" : chunk_data[0],
            "id_chunk" : chunk_data[1],
            "vector" : np.array(json.loads(chunk_data[2]))
        }
        res.append(chunk)

    return res

def find_top_k_chunk(model, input_vector, chunks_data, top_k = 3, min_score = -0.5):
    import torch
    import numpy as np
    vectors = np.array([chunk["vector"] for chunk in chunks_data], dtype=np.float32)
    similarity_scores = model.similarity(input_vector, vectors)[0]
    scores, indices = torch.topk(similarity_scores, k=top_k)
    top_chunks = []
    for score, idx in zip(scores, indices):
        if score < min_score: 
            continue
        top_chunks.append(chunks_data[idx])

    return top_chunks


def generate_input_for_ai(questions, top_k_chunk):
    from .db_manager import DBManager
    database = DBManager()
    inputs_data = []
    for i, question in enumerate(questions):
        chunks = top_k_chunk[f"question-{i}"]
        chunks_data = []
        for chunk in chunks:
            # print(chunk)
            chunk_data = database.find_chunk_text(chunk["id_chunk"])
            chunks_data.append({
                "id_chunk" : chunk_data[0],
                "page" : chunk_data[1],
                "texts" : chunk_data[2]
            })

        inputs_data.append({
            "question" : question,
            "chunks-top-k": chunks_data,
        })

        return inputs_data