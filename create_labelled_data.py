import os
import json
import csv
import openai
from dotenv import load_dotenv
import time

# --- 1. SETUP ---
# Load environment variables from the .env file (for the OpenAI API key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the folder containing the JSON files and the output CSV file name
CONVERSATIONS_DIR = "All_Conversations"
OUTPUT_CSV_FILE = "labeled_conversations.csv"

# --- 2. HELPER FUNCTIONS ---

def format_conversation_to_string(conversation_data):
    """Converts the structured conversation data into a single formatted string for analysis."""
    if not conversation_data:
        return ""
    
    full_conversation = []
    for entry in conversation_data:
        speaker = entry.get("speaker", "Unknown")
        text = entry.get("text", "")
        full_conversation.append(f"{speaker}: {text}")
        
    return "\n".join(full_conversation)

def analyze_conversation_with_llm(conversation_text):
    """
    Analyzes the conversation text using OpenAI's Chat Completion API to detect
    profanity and compliance violations.

    Returns:
        A dictionary with the analysis results, e.g.,
        {'profanity': 'Not Found', 'sensitive_data_compliance': 'Found'}
    """
    if not openai.api_key:
        raise ValueError("OpenAI API key is not set. Please check your .env file.")

    system_prompt = (
        "You are a highly accurate data labeling assistant. Your task is to analyze call "
        "transcripts and classify them based on two criteria: profanity and sensitive data "
        "compliance. You must respond ONLY with a single, valid JSON object and nothing else."
    )
    
    user_prompt = f"""
    Analyze the following conversation transcript.

    Criteria for labeling:
    1. Profanity: Determine if any speaker uses profane, abusive, or curse words.
    2. Sensitive Data Compliance: A compliance violation occurs if the agent reveals sensitive
       customer information (like account balance, transaction details, or full address) *before*
       successfully verifying the customer's identity (e.g., asking for date of birth,
       full address, or other personal identifiers). If the agent asks for verification first
       and then provides the information, it is NOT a violation.

    Based on these criteria, analyze the transcript below.

    Transcript:
    ---
    {conversation_text}
    ---

    Respond with a single JSON object with two keys: "profanity" and "sensitive_data_compliance".
    The value for each key must be either "Found" or "Not Found".
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        # Extract and parse the JSON content from the response
        result_json = response.choices[0].message.content
        analysis_result = json.loads(result_json)
        return analysis_result

    except Exception as e:
        print(f"  [Error] An error occurred with the OpenAI API: {e}")
        # Return a default error state
        return {
            'profanity': 'Error',
            'sensitive_data_compliance': 'Error'
        }

# --- 3. MAIN SCRIPT LOGIC ---

def process_all_conversations():
    """
    Main function to find, process, and label all conversations,
    then save the results to a CSV file.
    """
    print(f"Starting data labeling process...")
    print(f"Looking for .json files in '{CONVERSATIONS_DIR}' directory...")

    json_files = [f for f in os.listdir(CONVERSATIONS_DIR) if f.endswith('.json')]
    
    if not json_files:
        print("No .json files found. Exiting.")
        return

    print(f"Found {len(json_files)} files. Preparing to label them...")

    # Open the CSV file to write the results
    with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['conversation_id', 'conversation', 'profanity', 'sensitive_data_compliance']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()

        # Loop through each JSON file
        for i, filename in enumerate(json_files):
            print(f"\nProcessing file {i+1}/{len(json_files)}: {filename}")
            
            conversation_id = os.path.splitext(filename)[0]
            file_path = os.path.join(CONVERSATIONS_DIR, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    conversation_data = json.load(f)
                
                # Format the conversation for the LLM
                conversation_text = format_conversation_to_string(conversation_data)
                
                # Get the analysis from the LLM
                if conversation_text:
                    print("  > Sending to LLM for analysis...")
                    analysis = analyze_conversation_with_llm(conversation_text)
                    print(f"  > Received labels: {analysis}")
                else:
                    analysis = {'profanity': 'Not Found', 'sensitive_data_compliance': 'Not Found'}
                    print("  > Empty conversation, skipping LLM call.")

                # Prepare row for CSV
                row = {
                    'conversation_id': conversation_id,
                    'conversation': json.dumps(conversation_data), # Store the full JSON as a string
                    'profanity': analysis.get('profanity', 'Error'),
                    'sensitive_data_compliance': analysis.get('sensitive_data_compliance', 'Error')
                }
                
                writer.writerow(row)
                
                # A small delay to avoid hitting API rate limits too quickly
                time.sleep(1) 

            except json.JSONDecodeError:
                print(f"  [Error] Could not decode JSON from {filename}. Skipping.")
            except Exception as e:
                print(f"  [Error] An unexpected error occurred while processing {filename}: {e}")

    print(f"\n✅ Processing complete! Labeled data has been saved to '{OUTPUT_CSV_FILE}'.")


if __name__ == "__main__":
    process_all_conversations()