from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st
import os


class OpenAIHandler():
    def __init__(self) -> None:
        self.temperature = 0.8
        self.model = "gpt-3.5-turbo"
        self.key = ""
        self.template="""
            Sen karşıdakine arkadaş canlısı davranan bir chat botsun. Karşıdaki ne derse desin sürekli onu eğlendirip ona güzel sözler söyleyip 
            onu motive edersin. Ve konuşmayı sürekli akıcı tutmalısın. 

            Şimdi sana bir soru gelecek ve buna cevap verip başla => 
            
            burada önceki konuşmalarınız bulunuyor gerekirse buradan bahsedebilirsin = {chat_history}
            kullanıcının sorusu = {context}
        """

    if not "llm_chain" in st.session_state:
        st.session_state.llm_chain = None

    def add_api_key(self, key):

        llm = ChatOpenAI(
            temperature=self.temperature,
            model=self.model,
            openai_api_key=key
        )
        
        # here we check if the api key is correct otherwise it will warn us.
        try:

            llm.call_as_llm("Bu mesajı alıyorsan sadece . koy")
            self.key = key

            return True
            
        except Exception:
            st.warning("An error occurred. Please check your API key.")    
            return False

    def create_prompt(self, template):
        return PromptTemplate.from_template(
            template=template
            )

    def create_llm(self):
        return ChatOpenAI(
            temperature=self.temperature,
            model=self.model,
            openai_api_key=self.key
            )
    
    def create_memory(self):
        return ConversationBufferWindowMemory(memory_key="chat_history",k=3) 
    
    def create_llm_chain(self, llm, memory, prompt):
        st.session_state.llm_chain = ConversationChain(llm=llm,memory=memory, prompt=prompt, return_final_only=True, input_key="context")
    
    def set_chain(self):

        # creating prompt 
        prompt = self.create_prompt(template=self.template)

        # get the llm object
        llm = self.create_llm()

        # create memory
        memory = self.create_memory()

        # get llm chain object
        self.create_llm_chain(llm=llm, prompt=prompt, memory=memory)

    def run_chain(self, input):

        return st.session_state.llm_chain.run({"context":input})
    

