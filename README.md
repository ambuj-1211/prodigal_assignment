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


### Example json to upload 
- [📥 Download Sample Call Data from here](https://github.com/ambuj-1211/prodigal_assignment/blob/master/All_Conversations/0b6979e4-8c05-49e1-b7a7-94d85a627df5.json)
### Deployed main application
- [Click here to see the deployed main application.](https://callanalysis-app.streamlit.app/)
### Deployed visualization application
- [Click here to see the deployed visualizer application.](https://callvisualizer-app.streamlit.app/)
**[Note] Use example json to upload in both cases.**