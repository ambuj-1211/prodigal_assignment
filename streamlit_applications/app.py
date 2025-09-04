import json
import os
import re
import sys
from pathlib import Path

# Add the parent directory to Python path to import ml_model
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

import streamlit as st
import yaml
# from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from ml_model.predictor import CallAnalysisPredictor

# Load environment variables from .env file
load_dotenv()


def normalize_yaml_to_json(data):
    """
    Converts YAML parsed structure into a JSON-like list of dicts,
    same as what json.loads would return.
    """
    # If YAML has "transcript" key, unwrap it
    if isinstance(data, dict) and "transcript" in data:
        return data["transcript"]
    # If YAML is already a list (like JSON), return as is
    if isinstance(data, list):
        return data
    # Otherwise return empty list (invalid format)
    return []

# --- Helper Functions ---
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
def parse_conversation_file(uploaded_file):
    """
    Parses an uploaded file (JSON or YAML) and returns the conversation data and call ID.
    """
    if uploaded_file is not None:
        # Use filename as call_id
        call_id = os.path.splitext(uploaded_file.name)[0]
        content = uploaded_file.getvalue().decode("utf-8")
        try:
            # Try parsing as JSON first
            data = json.loads(content)
            return data, call_id
        except json.JSONDecodeError:
            try:
                # If JSON fails, try parsing as YAML
                yaml_data = yaml.safe_load(content)
                data = normalize_yaml_to_json(yaml_data) 
                return data, call_id
            except yaml.YAMLError:
                st.error("Invalid file format. Please upload a valid JSON or YAML file.")
                return None, None
    return None, None

def parse_conversation_text(text_input, call_id_name="manual_input"):
    """
    Parses conversation text (JSON or YAML) from a text area.
    """
    if text_input:
        try:
            data = json.loads(text_input)
            return data, call_id_name
        except json.JSONDecodeError:
            try:
                yaml_data = yaml.safe_load(text_input)
                data = normalize_yaml_to_json(yaml_data)
                return data, call_id_name
            except yaml.YAMLError:
                st.error("Invalid text format. Please enter valid JSON or YAML.")
                return None, None
    return None, None


def format_conversation_to_string(conversation_data):
    """
    Converts the structured conversation data into a single formatted string.
    """
    if not conversation_data:
        return ""
    
    full_conversation = []
    for entry in conversation_data:
        speaker = entry.get("speaker", "Unknown")
        text = entry.get("text", "")
        stime = entry.get("stime", 0)
        etime = entry.get("etime", 0)
        full_conversation.append(f"[{stime}-{etime}] {speaker}: {text}")
        
    return "\n".join(full_conversation)

# --- Analysis Functions ---

def analyze_with_regex(conversation_text, entity):
    """
    Analyzes the conversation using regular expressions based on the selected entity.
    """
    if entity == "Profanity Detection":
        # Simple regex for common profane words (add more as needed)
        # Using \b for word boundaries to avoid matching words like "assist"
        profanity_pattern= re.compile(
        r'\b('
        r'hell|damn|ass(hole)?|bitch|'
        r'fuck(er|ing|ed)?|shit(ty)?|'
        r'crap|piss(ed)?|bastard|cunt|dick|prick'
        r')\b',
        re.IGNORECASE
    )
        if profanity_pattern.search(conversation_text):
            return "Found"
        return "Not Found"

    elif entity == "Privacy and Compliance Violation":
        # Regex to find sensitive info like 'balance' or 'account'
        sensitive_info_pattern = re.compile(r'\b(balance|account details)\b', re.IGNORECASE)
        
        # Regex to find verification phrases
        verification_pattern = re.compile(r'\b(date of birth|address|social security number|ssn)\b', re.IGNORECASE)

        sensitive_match = sensitive_info_pattern.search(conversation_text)
        
        if sensitive_match:
            # Check if any verification phrase appears *before* the sensitive info
            text_before_sensitive = conversation_text[:sensitive_match.start()]
            if verification_pattern.search(text_before_sensitive):
                # Verification happened before sensitive info was shared
                return "Not Found"
            else:
                # Sensitive info shared without prior verification
                return "Found"
        return "Not Found"
        
    return "Not Applicable"

def analyze_with_llm(conversation_text, entity, api_key):
    """
    Analyzes the conversation using a Groq LLM based on the selected entity.
    """
    if not api_key:
        st.error("GROQ_API_KEY is not set. Please add it to your .env file.")
        return None

    try:
        # Initialize the LLM
        llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0, max_tokens=None)

        # Define prompts based on the entity
        if entity == "Profanity Detection":
            template = """
            You are a call transcript analyst. Your task is to detect profanity in the following conversation.
            Analyze the text and determine if any speaker uses profane language.
            Respond with only "Found" or "Not Found".

            Conversation:
            {conversation}
            """
        elif entity == "Privacy and Compliance Violation":
            template = """
            You are a compliance analyst. Your task is to detect privacy violations in a call transcript.
            A violation occurs if an agent shares sensitive information like a balance or account details
            BEFORE verifying the customer's identity (e.g., asking for date of birth, address, or Social Security Number).

            Analyze the conversation below. Does the agent share sensitive information before identity verification?
            Respond with only "Found" if a violation occurred, or "Not Found" if it did not.

            Conversation:
            {conversation}
            """
        else:
            return "Invalid entity for LLM analysis."

        prompt = PromptTemplate(template=template, input_variables=["conversation"])
        # llm_chain = LLMChain(prompt=prompt, llm=llm)
        llm_chain = prompt | llm | StrOutputParser()
        
        # Get the result from the LLM
        response = llm_chain.invoke({"conversation": conversation_text})
        # The actual result is in the 'text' key of the response dictionary
        # result = response.get('text', 'Error processing response').strip()
        
        return response

    except Exception as e:
        st.error(f"An error occurred with the LLM API: {e}")
        return None
    
def analyze_with_ml_model(conversation_data, entity):
    predictor = CallAnalysisPredictor()
    predictor.load_models()
    conversation_json = json.dumps(conversation_data, ensure_ascii=False)
    if entity == "Profanity Detection":
        profanity_result = predictor.predict_profanity(conversation_json)
        if profanity_result == "found":
            profanity_result="Found"
        return profanity_result
    if entity == "Privacy and Compliance Violation":
        sensitive_result = predictor.predict_sensitive_data(conversation_json)
        if sensitive_result == "found":
            sensitive_result="Found"
        return sensitive_result

# --- Streamlit App UI ---

st.set_page_config(layout="wide", page_title="Call Conversation Analyzer")

st.title("📞 Call Conversation Analyzer")
st.markdown("Upload or paste a call transcript in JSON or YAML format to analyze it for specific entities.")

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    input_method = st.radio("Choose Input Method", ["File Upload", "Text Input"])

    uploaded_file = None
    text_input = None

    if input_method == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload a JSON or YAML file",
            type=["json", "yaml", "yml"]
        )
    else:
        text_input = st.text_area(
            "Paste your JSON or YAML content here",
            height=300,
            placeholder='[\n  {\n    "speaker": "Agent",\n    "text": "Hello...",\n    ...\n  }\n]'
        )

    entity = st.selectbox(
        "Select Entity to Detect",
        ("Profanity Detection", "Privacy and Compliance Violation")
    )

    approach = st.selectbox(
        "Select Analysis Approach",
        ("Pattern Matching (Regex)", "Machine Learning", "LLM (Groq)")
    )

    analyze_button = st.button("Analyze Conversation", type="primary")


# Main content area
if analyze_button:
    conversation_data = None
    call_id = None

    if uploaded_file:
        conversation_data, call_id = parse_conversation_file(uploaded_file)
    elif text_input:
        conversation_data, call_id = parse_conversation_text(text_input)
    else:
        st.warning("Please upload a file or paste content to analyze.")

    if conversation_data and call_id:
        st.header("Analysis Result")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Call ID:** `{call_id}`")
            st.info(f"**Entity:** `{entity}`")
            st.info(f"**Approach:** `{approach}`")
            
            # Perform analysis based on selected approach
            conversation_string = format_conversation_to_string(conversation_data)
            result = "Not Analyzed"

            if approach == "Pattern Matching (Regex)":
                with st.spinner("Analyzing with Regex..."):
                    result = analyze_with_regex(conversation_string, entity)
            
            elif approach == "LLM (Groq)":
                with st.spinner("Analyzing with LLM..."):
                    result = analyze_with_llm(conversation_string, entity, groq_api_key)
            
            elif approach == "Machine Learning":
                # st.info("The Machine Learning model feature is currently under development.")
                with st.spinner("Analyze with the ml model approach..."):
                    result = analyze_with_ml_model(conversation_data, entity)
                # result = "Not Implemented"

            if result:
                st.success(f"**Result:** {entity}: **{result}**")
        
        with col2:
            st.subheader("Full Conversation Transcript")
            st.text_area(
                "Conversation",
                value=format_conversation_to_string(conversation_data),
                height=400,
                disabled=True
            )
else:
    st.info("Upload a file or paste text and click 'Analyze Conversation' to see the results.")