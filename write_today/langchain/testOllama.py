import os
from langchain_community.llms import Ollama

llm = Ollama(temperature=0, model="llama2")

diary_input = "듣고 싶은 강의가 있었는데 해당 강의가 갑자기 휴강이 되어서 너무 슬펐어."
emotions_input = "속상함, 슬픔, 좌절, 우울"

prompt = f"""Please leave a comment of sympathy from your best friend's perspective based on the contents of the following diary.
condition :
1. The writer's emotions will be given along with the diary.
2. Must follow informal language as best friend.
3. Make sure to write comments in Korean.
4. You need to feel the same way writer's emotions.

diary : {diary_input}

emotions : {emotions_input}
"""

result = llm.invoke(prompt)
print(result)