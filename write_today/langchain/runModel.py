from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline

#model_id = 'models/M-SOLAR-10.7B-v1.3'
model_id = 'chihoonlee10/T3Q-ko-solar-dpo-v6.0'

# HuggingFacePipeline object
llm = HuggingFacePipeline.from_model_id(
    model_id = model_id, 
    device = 0,               # -1: CPU(default), GPU존재하는 경우는 0번이상(CUDA Device #번호)
    task = "text-generation", # 텍스트 생성
    model_kwargs = {"do_sample": True, "max_length": 128},
)

# template
template = """질문: {question}

답변: """

prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "서울에서 제일 유명한 산이 어디야?"
print(llm_chain.run(question = question))