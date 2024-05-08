from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # 출력 스트림 용도


template = """diary_and_emotions: {input}

Answer: Please leave a comment of sympathy from counselor's perspective based on the contents of the following diary, writer's emotions and meet a condition

condition :
1. The writer's emotions will be given along with the diary.
2. Make sure to write comments in Korean.
3. Write within 3 sentences."""

prompt = PromptTemplate(template = template, input_variables = ["diary_and_emotions"])

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
                model_path = "models/solar-10.7b-instruct-v1.0-uncensored.Q3_K_M.gguf",
                input = {"temperature": 0.75,
                       "max_length": 2000,
                       "top_p": 1},
                callback_manager=callback_manager,
                verbose=True,
                )

llm_chain = LLMChain(prompt=prompt, llm=llm)

input = "오늘 아침 메뉴가 맛있어서 기대했지만 실제로 식당에 가니 맛있는 반찬이 부족했어. 밥을 많이 먹지 못해 속상해 ㅠㅠ / 속상함 80%, 슬픔 10%, 좌절 5%, 우울 5%"

prompt = f"""diary_and_emotions: {input}"""

response = llm_chain.run(prompt)
print(response)