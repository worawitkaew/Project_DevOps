resume_text = """
Firstname:  warun\n\n
Lastname:   kunganun\n\n
Nickname: Rowan\n\n

Gender: Male\n\n

BIRTH OF DATE: May 22 , 1999\n\n
Telephone:012-345-6789\n\n
Email: example@gmail.com\n\n

My interest:  I am interested in self-development from Backend developer to full-stack developer.

TOOLS EXPERIENCE:
-   python (fastapi,langchain)
-   docker,docker-compose
-   AWS (amazon web service)
-   react (javascript)
-   Github
-   database (postgresql)
-   postman, swagger

Education:
2017-2021 | Chiang Mai University 
    | Faculty: Science 
    | Department: Computer Science

Career Background:\n\n
Machine learning\n\n
RESEARCHER ASSISTANT | NARIT INTERNSHIP PROGRAM (6 MONTH) | 2020
-   Developed a Machine Learning program using python to analyze additional data with the data of light.
Back-end Developer\n\n
Synapes thailand | 2022-present
-   Develop API systems.

Examples of work in the online:
-   Kaggle (website : https://www.kaggle.com/worawitkaew/trysomefeets)
-   Github  (https://github.com/worawitkaew)

"""
import uuid

from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph,END
from langchain_ollama import OllamaLLM

import streamlit as st




# Define a chat model
if "llm" not in st.session_state:
    st.session_state.llm = OllamaLLM(model="llama3")


# Define the function that calls the model
def call_model(state: MessagesState):
    response = st.session_state.llm.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": response}

# Define a new graph
if "workflow_StateGraph" not in st.session_state:
    st.session_state.workflow_StateGraph = StateGraph(state_schema=MessagesState)
    # Define the two nodes we will cycle between
    st.session_state.workflow_StateGraph.add_edge(START, "model")
    st.session_state.workflow_StateGraph.add_node("model", call_model)
    st.session_state.workflow_StateGraph.add_edge("model", END)
workflow_StateGraph = st.session_state.workflow_StateGraph




# Adding memory is straight forward in langgraph!
if "MemorySaver" not in st.session_state:
    st.session_state.MemorySaver = MemorySaver()


if "app" not in st.session_state:
    st.session_state.app = workflow_StateGraph.compile(
        checkpointer=st.session_state.MemorySaver
    )


# The thread id is a unique key that identifies
# this particular conversation.
# We'll just generate a random uuid here.
# This enables a single application to manage conversations among multiple users.
if "config" not in st.session_state:
    st.session_state.config = {"configurable": {"thread_id": uuid.uuid4()}}

# Streamlit app config
init_query = f"""
    This is Resume information\n\n
    ******************************
    {resume_text}
    ******************************
    Could you act as my assistant chatbot and interact with users who come seeking information from this resume? If a user's question is unrelated to the details provided in the resume
    , kindly inform them that you can only assist with questions pertaining to the information in the resume. 
"""

st.set_page_config(page_title="Chat with websites", page_icon="🤖")
st.title("Chat with websites")

# sidebar
with st.sidebar:
    st.header("Simple in formation")
    website_url = st.write(resume_text)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ] 

# init conversation start request
if "init_boolean" not in st.session_state:
    input_message = SystemMessage(content=init_query)
    for event in st.session_state.app.stream({"messages": [input_message]}, st.session_state.config, stream_mode="values"):
        response = event["messages"][-1].content

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    
    with st.spinner("Thinking..."):
        input_message = HumanMessage(content=user_query)
        for event in st.session_state.app.stream({"messages": [input_message]}, st.session_state.config, stream_mode="values"):
            response = event["messages"][-1].content
    
    
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=response))
    
    

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# สร้างความแตกต่างให้บ้างอย่างทำแค่ตอนเริ่มเข้าเว็บเท่านั้น
st.session_state.init_boolean = True