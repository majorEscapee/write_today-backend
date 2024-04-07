from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # 출력 스트림 용도

# LLAMA2는 더이상 ggmlv3 형식을 지원하지 않기 때문에 GGUF 형식을 사용해야 함 

template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template = template, input_variables = ["question"])

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
                model_path = "models/llama-2-7b-chat.Q2_K.gguf",
                input = {"temperature": 0.75,
                       "max_length": 2000,
                       "top_p": 1},
                callback_manager=callback_manager,
                verbose=True,
                )

llm_chain = LLMChain(prompt=prompt, llm=llm)

prompt = """
Question: Explain the Large Language Models.
"""
response = llm_chain.run(prompt)