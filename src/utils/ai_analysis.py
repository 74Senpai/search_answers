from google import genai
from google.genai import types

import json
import config

client = genai.Client()
req_limit_per_day = config.rate_limit_per_day

def search_answer(input_data):
    global req_limit_per_day
    if req_limit_per_day <= 0:
      raise PermissionError("Đạt giới hạn gọi API trên ngày")
    
    input_data_json = json.dumps(input_data, ensure_ascii=False)
    token = client.models.count_tokens(model=config.gemini_model, contents=input_data_json)
    print(f"Token của {len(input_data)} câu hỏi là: {token.total_tokens}")
    if token.total_tokens > config.token_limit_per_minute / config.rate_limit_per_minute :
        raise ValueError("Dữ liệu đầu vào quá lớn, vui lòng giảm xuống mức thấp hơn")
    response = client.models.generate_content(
        model=config.gemini_model,
        config = types.GenerateContentConfig(
          thinking_config = types.ThinkingConfig(thinking_budget=config.thinking_budget),
          system_instruction = config.system_introduct,
        ),
        contents= input_data_json,
    )

    req_limit_per_day -= 1
    return response
