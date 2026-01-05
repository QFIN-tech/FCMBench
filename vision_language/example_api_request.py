from openai import OpenAI
from evaluation import parse_jsonl
import base64
import pathlib
import json

API_KEY = "YOUR_API_KEY"
BASE_URL = "YOUR_API_BASE_URL" # https://api.openai.com/v1/
DATA_ROOT = "/path/to/unzipped_images" # ./data/oceanus-share/V1.0_IMAGES_TEST/
MODEL_NAME = "YOUR_MODEL_NAME"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
all_test_data = parse_jsonl('FCMBench_v1.0_testset.jsonl')
test_data = all_test_data[0]


def file_to_data_uri(relative_path):
    path = pathlib.Path(DATA_ROOT) / pathlib.Path(relative_path)
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    if path.suffix in [".jpg", ".jpeg", ".JPG"]:
        mime = "image/jpeg"
    elif path.suffix == ".png":
        mime = "image/png"
    return f"data:{mime};base64,{b64}"

content = [{
    "type": "text",
    "text": test_data["prompt"]
}]

for img_rel in test_data["images"]:
    data_uri = file_to_data_uri(img_rel)
    if data_uri is None:
        continue
    content.append(
        {
            "type": "image_url",
            "image_url": {
                "url": data_uri
            },
        }
    )

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.01,
    stream=False,
    messages=[
        {
            "role": "user",
            "content": content,
        }
    ]
)

test_result = {
    "id": test_data["id"], 
    "response": response.choices[0].message.content
}

with open('prediction_results.jsonl', 'w') as f:
    f.write(json.dumps(test_result, ensure_ascii=False) + '\n')
