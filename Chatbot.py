from Utils.OpenAI import OpenAIHandler
from streamlit import chat_message
import streamlit as st



if not "chain_object" in st.session_state:
    st.session_state.chain_object = OpenAIHandler()

if not "chain_object" in st.session_state:
    st.session_state.key = ""

if not "chat_history" in st.session_state:
    st.session_state.chat_history = []

if not "session_activate" in st.session_state:
    st.session_state.session_activate = False

def displayMessages(chat_history):
    count = 1
    for message in (chat_history):
        if count % 2 == 0:
            with chat_message("user"):
                st.write(message)
        else:
            with chat_message("assistant"):
                st.write(message)
        count += 1

def display_user_message(user_message):
        with chat_message("user"):
            st.write(user_message)

def display_bot_message(bot_message):
        with chat_message("assistant"):
            st.write(bot_message)

def main():

        st.header("Chat with me 🤖")
    
        with st.sidebar:

            st.image("./image/summarify-logo-300.png")
            "contacts"

            st.text("http:/summarify.io")
            
            st.session_state.key = st.text_input("Your OpenAI Key:")

        # check if the api key entered
        if st.session_state.key:

            # check if the api key really exist
            key_exist = st.session_state.chain_object.add_api_key(st.session_state.key)

            if key_exist:
                st.info("OPENAI keyiniz doğrulandı. Konuşmaya başlayabilirsiniz.", icon="📢") 

                # if api key exist, start the session for chat.
                if not st.session_state.session_activate:
                    st.session_state.session_activate = True 
                    st.session_state.chain_object.set_chain()
            else:
                 st.info("Lütfen doğru OpenAI api keyinizi giriniz!", icon="📢") 

        # user question
        question = st.text_input("Chat now!", key="input") 

        button = st.checkbox(label=("Show all Chat 💬"))

        if button:
            question = ""
            st.write("< All Chat History >")
            displayMessages(st.session_state.chat_history)

        if question:
            
            if st.session_state.key=="":

                st.info("Lütfen OpenAI api keyinizi giriniz!", icon="📢") 

            else:
                
                st.write("---")

                # sending request to openai...
                response = st.session_state.chain_object.run_chain(question)
                
                #displaying messages
                display_user_message(question)
                display_bot_message(response)

                #saving messages for later look up.
                st.session_state.chat_history.append(question)
                st.session_state.chat_history.append(response)

                st.write("---")


if __name__ == "__main__":
    main()