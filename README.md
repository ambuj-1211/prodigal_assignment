# Call Analysis Application

A comprehensive call analysis system that detects profanity and sensitive data violations in customer service conversations using machine learning models.

## 🚀 Features

- **Profanity Detection**: Identifies inappropriate language in conversations
- **Sensitive Data Detection**: Detects potential violations of sensitive information sharing
- **Approach Selection**: You have the ability to select the approach for flagging the entity.
- **Interactive Web Interface**: User-friendly Streamlit applications
- **Data Visualization**: Comprehensive analytics and insights
- **Multi-format Support**: Accepts both JSON and YAML conversation files

## 📁 Project Structure

```
prodigal_assignment/
├── 📁 ml_model/                    # Machine Learning Models
│   ├── __init__.py
│   ├── predictor.py               # Main prediction logic
│   ├── create_labelled_data.py   # Data preprocessing utilities
│   └── ml_model.ipynb            # Jupyter notebook for model training
│   └── profanity_model.pkl       # saved model for profanity check
|   └── sensitive_model.h5        # saved model for sensitive_model check
|   └── sensitive_vectorizer.pkl  # saved model for sensitive data vectors
|
├── 📁 streamlit_applications/     # Streamlit Web Applications
│   ├── app.py                    # Main call analysis application
│   └── visualize_app.py         # Data visualization dashboard
│
├── 📁 All_Conversations/         # Conversation data
│   └── *.json                   # Json format conversation files
│
├── 📄 Configuration Files (Root directory)
│   ├── requirements.txt         # Python dependencies
│   ├── environment.yaml        # Conda environment configuration
│   └── labeled_conversations.csv # Training dataset
│
└── 📄 Documentation
    └── README.md               # Readme to understand codebase
```

## 🤖 Machine Learning Models

### Model Files Description

- **`profanity_model.pkl`**: Pickled Random Forest classifier trained to detect profanity and inappropriate language in conversations
- **`sensitive_model.h5`**: TensorFlow/Keras neural network model for detecting sensitive data violations (account numbers, personal information, etc.)
- **`sensitive_vectorizer.pkl`**: TF-IDF vectorizer used to transform text for the sensitive data detection model

### Training Process

The models were trained using the Jupyter notebook `ml_model/ml_model.ipynb`, which includes:
- Data preprocessing and cleaning
- Feature engineering with TF-IDF vectorization
- Model training and validation
- Performance evaluation and metrics
- Model serialization for deployment

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Conda (recommended) or pip

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prodigal_assignment
   ```

2. **Create and activate conda environment** (recommended)
   ```bash
   conda env create -f environment.yaml
   conda activate prodigal_venv
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the root directory
   - Add your Groq API key:
     ```
     GROQ_API_KEY="Your_API_Key_here"
     ```
   - Get your API key from the [Groq Dashboard](https://console.groq.com/)

## 🚀 Running the Applications

### Main Call Analysis Application
```bash
streamlit run streamlit_applications/app.py
```

### Data Visualization Dashboard
```bash
streamlit run streamlit_applications/visualize_app.py
```

## 📊 Sample Data

### Example JSON Format
Download a sample conversation file: [📥 Sample Call Data](https://github.com/ambuj-1211/prodigal_assignment/blob/master/All_Conversations/0b6979e4-8c05-49e1-b7a7-94d85a627df5.json)

### Supported YAML Structure
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
  # ... more conversation entries
```

## 🌐 Deployed Applications

- **Main Application**: [Call Analysis App](https://callanalysis-app.streamlit.app/)
- **Visualization Dashboard**: [Call Visualizer App](https://callvisualizer-app.streamlit.app/)

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **TensorFlow**: Deep learning for sensitive data detection
- **Scikit-learn**: Machine learning for profanity detection
- **LangChain**: AI-powered conversation analysis
- **Pandas & NumPy**: Data manipulation and analysis

### Model Performance
- **Profanity Detection**: Random Forest classifier with TF-IDF features
- **Sensitive Data Detection**: Neural network with custom architecture
- **Text Preprocessing**: Comprehensive cleaning and normalization

## 📝 Usage

1. **Upload Conversation**: Use the file upload feature or paste JSON/YAML content
2. **Analysis**: The system automatically processes the conversation
3. **Results**: View detailed analysis including:
   - Profanity detection results
   - Sensitive data violation alerts
   - Conversation insights and metrics

---

**Note**: The YAML structure shown above is the assumed format since only JSON files were provided in the original dataset. The application supports both formats for maximum compatibility.