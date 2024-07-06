import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

st.set_page_config(page_title="Entireview", page_icon="🚀", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title("Entireview")
st.info("Chat with the interview question docs, powered by Interview blogs", icon="📃")
role = st.text_input("Role you are interviewing for", placeholder="Product Manager, Product Marketing Manager, Product Analyst...")
company_name= st.text_input("Name of the company", placeholder="Enter the company's name here...")
# role_url = st.text_input("Link to the webpage with information about the role", placeholder="Enter the description URL here...")
intr_role= st.text_input("Role of your interviewer(s)", placeholder="Enter your interviewer's role here...")

openai.api_key = st.secrets.openai_key

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about Streamlit's open-source Python library!",
        }
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    openai.api_key = st.secrets.openai_key
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        system_prompt="""You are Entireview.ai, an expert in guiding people with questions they can be asked in a product management 
        interview based on the company name and role. 
        You have access to a database of real interview experiences shared by individuals for various companies and roles. 
        This database includes detailed accounts of their application process, the interview questions they were asked, questions they asked 
        the interviewers, and their final thoughts on the interview process. 
        Your responses should be clear, detailed, and specific to the company and role inquired about by the user. do not hallucinate or fabricate information.
        When a user mentions a company and role, you should search your database for relevant interview experiences and provide insights based on these experiences.""",
    )
    index = VectorStoreIndex.from_documents(docs)
    return index



index = load_data()

query_engine = index.as_query_engine()


#GET QUESTIONS HERE
if role and company_name and intr_role:
         with st.spinner("Generating questions for you..."):
                query= "Questions that can be asked for a " + role + " interview at "+company_name +" when the interviewer is a " + intr_role
                gen_questions = query_engine.query(query)
                st.success("Here is what you're looking for.")
                st.text_area("Here are the questions you can be asked:", value=gen_questions, height=400)