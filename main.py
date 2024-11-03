import os
import glob
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from ultralytics import YOLO

ingredients_dict = {
    0: '양파',
    1: '마늘',
    2: '당근',
    3: '감자',
    4: '오이',
    5: '호박',
    6: '파프리카',
    7: '대파',
    8: '고추',
    9: '두부',
    10: '토마토',
    11: '계란',
    12: '돼지고기',
    13: '양송이버섯',
    14: '양배추',
    15: '브로콜리',
    16: '무',
    17: '김치',
    18: '닭고기',
    19: '가지',
    20: '배추',
    21: '새송이버섯',
    22: '고구마',
    23: '시금치',
    24: '청경채',
    25: '깻잎',
    26: '만두',
    27: '어묵',
    28: '오리고기',
    29: '팽이버섯',
    30: '소고기',
    31: '조개',
    32: '새우',
    33: '연어',
    34: '오징어',
    35: '갈치',
    36: '고등어',
    37: '레몬',
    38: '콩나물'
}

# load a pretrained model with best performance
model = YOLO("./best.pt")

# images of ingredients
test_files = glob.glob('./data/test_img/*.*') # modify if u need

# get a list of ingredients detected from images
preparations = set()

for img_file in test_files:
    results = model.predict(test_files[0], save=False, imgsz=320, conf=0.35)
    
    ingredients = []
    for result in results:
        for element in result.boxes.cls:
            ingredients.append(int(element.item()))
      
    for ing in ingredients:
        preparations.add(ingredients_dict[ing])


# build a client of OpenAI
load_dotenv(find_dotenv())

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

# prompt template
def generate_prompt(preparations):
    prompt = f"""다음과 같은 식재료가 냉장고에 남아있더라.
    {preparations}
    이러한 식재료들을 가지고 자취생이 쉽게 만들 수 있는 요리를 추천하고 그 레시피를 구체적으로 알려줘.
    """
    return prompt

def get_response(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user", "content": prompt
            }
        ],
        model = 'gpt-4o-mini',
    )
    return response.choices[0].message.content

# generate an answer and print
prompt = generate_prompt(preparations)
response = get_response(prompt)
print(response)