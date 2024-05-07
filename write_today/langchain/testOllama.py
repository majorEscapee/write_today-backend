import os
from langchain_community.llms import Ollama

llm = Ollama(temperature=0, model="solar1")

diary_input = "오늘 아침 메뉴가 맛있어서 기대했지만 실제로 식당에 가니 맛있는 반찬이 부족했어. 밥을 많이 먹지 못해 속상해 ㅠㅠ " # input('일기 내용 : ') # 
emotions_input = "속상함 80%, 슬픔 10%, 좌절 5%, 우울 5%" # input('감정 : ') # 

prompt = f"""Please leave a comment of sympathy from counselor's perspective based on the contents of the following diary, writer's emotions and meet a condition.

condition :
1. The writer's emotions will be given along with the diary.
2. Make sure to write comments in Korean.
3. Write within 3 sentences.

diary : {diary_input}

emotions : {emotions_input}
"""

result = llm.invoke(prompt)
print(result)