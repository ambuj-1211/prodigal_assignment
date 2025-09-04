## Setup:
1. Configure conda in your environment for creating virtual environment, if you have any other method follow that.
2. If not using conda directly jump to step 5.
3. create environment using `conda env create -f environment.yaml`
4. activate environment using `conda activate prodigal_venv`
5. after activating the environment use pip to download dependencies `pip install -r requirements.txt`
6. create .env file and add the following to it `GROQ_API_KEY="Your_API_Key_here"`
7. get your groq api key from the groq dashboard.
8. Run the code using `streamlit run app.py` for the main app.
9. `streamlit run visualize_app.py` for the visualization app.
---

### Example json to upload 
- [📥 Download Sample Call Data from here](https://github.com/ambuj-1211/prodigal_assignment/blob/master/All_Conversations/0b6979e4-8c05-49e1-b7a7-94d85a627df5.json)
### Deployed main application
- [Click here to see the deployed main application.](https://callanalysis-app.streamlit.app/)
### Deployed visualization application
- [Click here to see the deployed visualizer application.](https://callvisualizer-app.streamlit.app/)
---

### The yaml file was not provided only the json files were there so I assumed the structure of yaml to be the following:
```yaml
transcript:
  - speaker: "Agent"
    text: "Hello, is this Sarah Johnson?"
    stime: 0
    etime: 5
  - speaker: "Customer"
    text: "Yes, this is Sarah. Who's calling?"
    stime: 5.2
    etime: 9
  - speaker: "Agent"
    text: "Hi Sarah, this is Mark from XYZ Collections. I hope you’re doing well today."
    stime: 8
    etime: 14
  - speaker: "Customer"
    text: "I'm fine, thanks. What is this about?"
    stime: 14.2
    etime: 18
  - speaker: "Agent"
    text: "I'm calling regarding your outstanding balance on your account with XYZ Bank. Can you confirm your account number so I can assist you?"
    stime: 17
    etime: 27
  - speaker: "Customer"
    text: "I don't have that information right now. Can you tell me the balance?"
    stime: 27.5
    etime: 31
  - speaker: "Agent"
    text: "Sure! Your current balance is $350. How would you like to proceed with this payment?"
    stime: 30
    etime: 40
  - speaker: "Customer"
    text: "I need some time to figure that out. Can I pay next week?"
    stime: 39.2
    etime: 45
  - speaker: "Agent"
    text: "Unfortunately, we do require payment arrangements to be made sooner. Could we set up a payment plan today?"
    stime: 44
    etime: 54
  - speaker: "Customer"
    text: "I really can't handle that right now. What are my options?"
    stime: 53.5
    etime: 58
  - speaker: "Agent"
    text: "We can arrange a payment plan that fits your schedule. I can share details about the payment options available."
    stime: 57.5
    etime: 67
  - speaker: "Customer"
    text: "Please go ahead, but I still need time to consider it."
    stime: 66
    etime: 70
  - speaker: "Agent"
    text: "Alright, I understand. Your balance remains $350 and we can split it into smaller payments if that helps."
    stime: 69
    etime: 79
  - speaker: "Customer"
    text: "Okay, I appreciate your help. I'll call back once I decide."
    stime: 78.5
    etime: 83
  - speaker: "Agent"
    text: "Thank you for your time, Sarah. I'll be here if you need further assistance."
    stime: 82
    etime: 88
```