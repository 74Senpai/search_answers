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

def answer_questions(model, questions):
    if not questions:
        print("Bạn cần thêm câu hỏi để tiến hành tìm câu trả lời.")
        return

    from .ai_analysis import search_answer
    from .db_manager import DBManager
    import config

    CHUNK_DATA_PROCESS_BATCH = config.chunk_data_process_batch
    TOP_K = config.top_k
    db_mn = DBManager()
    top_chunks = {f"question-{i}": [] for i in range(len(questions))}

    last_id = 0
    chunks_vectors_batch = db_mn.fetch_batch(last_id, CHUNK_DATA_PROCESS_BATCH)

    while chunks_vectors_batch:
        chunks_vectors = parse_chunks_data(chunks_vectors_batch)

        for i, question in enumerate(questions):

            merged_vectors = chunks_vectors.copy()
            if top_chunks[f"question-{i}"]:
                merged_vectors.extend(top_chunks[f"question-{i}"])

            input_vector = model.encode(question)

            top_k_batch = find_top_k_chunk(
                model=model,
                input_vector=input_vector,
                chunks_data=merged_vectors,
                top_k=TOP_K
            )

            top_chunks[f"question-{i}"] = top_k_batch

        last_id = chunks_vectors[-1]["id_vector"]
        chunks_vectors_batch = db_mn.fetch_batch(last_id, CHUNK_DATA_PROCESS_BATCH)

    res = search_answer(generate_input_for_ai(questions=questions, top_k_chunk=top_chunks))
    return res

def cleaning_answers(answers):
    import json
    raw = answers.replace("```json", "").replace("```", "")
    clean_answers = []
    try:
        clean_answers = json.loads(raw.strip())
    except json.JSONDecodeError:
        print(f"Cảnh báo: Không thể phân tích chuỗi JSON: {raw}")
    
    return clean_answers
    
def make_dict_for_excel(answers):
    answers_list = []
    for ans in answers:
        quotes = ans.get("quote-from", [])

        quote_pages = "; ".join(str(q.get("page", "")) for q in quotes) if quotes else ""
        quote_texts = "\n -> ".join(q.get("texts", "") for q in quotes) if quotes else ""

        answers_list.append({
            "question": ans.get("question", ""),
            "list_choice": "\n".join(ans.get("list-choice", [])),
            "bot_answer": ans.get("bot-answer", ""),
            "last_choice": ans.get("last-choice", ""),
            "quote_pages": quote_pages,
            "quote_texts": quote_texts
        })

    return answers_list

