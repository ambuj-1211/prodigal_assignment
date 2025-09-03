import streamlit as st
import json
import yaml
import matplotlib.pyplot as plt

def normalize_yaml_to_json(data):
    """
    Converts a parsed YAML structure into a JSON-like list of dictionaries.

    This handles cases where the transcript data is nested under a "transcript" key,
    ensuring a consistent format for the rest of the application.

    Args:
        data: The data loaded from a YAML file using yaml.safe_load().

    Returns:
        list: A list of dictionary objects representing the conversation, or an
              empty list if the format is invalid.
    """
    # If the YAML file has a top-level "transcript" key, extract its value
    if isinstance(data, dict) and "transcript" in data:
        return data["transcript"]
    # If the data is already a list (like a JSON array), return it as is
    if isinstance(data, list):
        return data
    # Return an empty list if the format is not recognized
    return []

def calculate_call_metrics(conversation_data):
    """
    Calculates total time, silence time, and overtalk time from conversation data.

    Args:
        conversation_data (list): A list of dictionaries, where each dict represents
                                  a turn in the conversation with 'stime' and 'etime'.

    Returns:
        dict: A dictionary containing the calculated metrics: 'total', 'silence',
              'overtalk', and 'normal'. Returns zeros if data is insufficient.
    """
    if not conversation_data or len(conversation_data) < 2:
        return {'total': 0, 'silence': 0, 'overtalk': 0, 'normal': 0}

    conversation_data.sort(key=lambda x: x['stime'])

    total_time = conversation_data[-1]['etime'] - conversation_data[0]['stime']
    total_silence = 0
    total_overtalk = 0

    for i in range(len(conversation_data) - 1):
        current_turn_end = conversation_data[i]['etime']
        next_turn_start = conversation_data[i+1]['stime']
        
        gap = next_turn_start - current_turn_end

        if gap > 0:
            total_silence += gap
        elif gap < 0:
            total_overtalk += -gap
            
    normal_talk_time = total_time - total_silence - total_overtalk
    
    if normal_talk_time < 0:
        normal_talk_time = 0

    return {
        'total': total_time,
        'silence': total_silence,
        'overtalk': total_overtalk,
        'normal': normal_talk_time
    }

def create_pie_chart(metrics):
    """
    Creates a matplotlib pie chart from the calculated call metrics.

    Args:
        metrics (dict): A dictionary with 'normal', 'silence', and 'overtalk' times.

    Returns:
        matplotlib.figure.Figure: The figure object for the generated pie chart.
    """
    labels = 'Normal Talk', 'Silence Time', 'Overtalk Time'
    sizes = [metrics['normal'], metrics['silence'], metrics['overtalk']]
    colors = ['#4CAF50', '#607D8B', '#F44336']
    explode = (0, 0.1, 0.1)

    filtered_labels = [label for i, label in enumerate(labels) if sizes[i] > 0]
    filtered_sizes = [size for size in sizes if size > 0]
    filtered_colors = [color for i, color in enumerate(colors) if sizes[i] > 0]
    filtered_explode = [exp for i, exp in enumerate(explode) if sizes[i] > 0]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(
        filtered_sizes,
        explode=filtered_explode,
        labels=filtered_labels,
        colors=filtered_colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=140,
        textprops={'fontsize': 12}
    )
           
    ax.axis('equal')
    ax.set_title("Call Time Distribution", fontsize=16, weight='bold', pad=20)
    
    return fig

# --- Streamlit App UI ---
def main():
    st.set_page_config(layout="centered", page_title="Call Time Visualizer")

    st.title("📊 Call Conversation Visualizer")
    st.markdown("Upload a call transcript in **JSON or YAML** format to analyze the distribution of talk time, silence, and overtalk.")

    uploaded_file = st.file_uploader(
        "Choose a JSON or YAML file",
        type=["json", "yml", "yaml"]
    )

    if uploaded_file is not None:
        conversation_data = None
        content = uploaded_file.getvalue().decode("utf-8")
        
        try:
            # First, attempt to parse the file as JSON
            conversation_data = json.loads(content)
        except json.JSONDecodeError:
            # If JSON fails, attempt to parse it as YAML
            try:
                yaml_data = yaml.safe_load(content)
                conversation_data = normalize_yaml_to_json(yaml_data)
            except yaml.YAMLError:
                st.error("Invalid file format. The file is not a valid JSON or YAML document.")
                return # Stop execution if both parsing attempts fail

        if conversation_data:
            metrics = calculate_call_metrics(conversation_data)

            if metrics['total'] > 0:
                st.header("Call Metrics Summary")

                col1, col2, col3 = st.columns(3)
                col1.metric("Normal Talk", f"{metrics['normal']:.2f} s", help="Time when only one person was speaking.")
                col2.metric("Silence Time", f"{metrics['silence']:.2f} s", help="Time when no one was speaking.")
                col3.metric("Overtalk Time", f"{metrics['overtalk']:.2f} s", help="Time when both people were speaking simultaneously.")
                
                st.info(f"**Total Call Duration:** {metrics['total']:.2f} seconds")
                
                st.divider()

                st.header("Time Distribution Chart")
                pie_chart_fig = create_pie_chart(metrics)
                st.pyplot(pie_chart_fig, use_container_width=True)
            else:
                st.warning("The uploaded file does not contain enough valid data to generate metrics or a chart.")
        
        else:
             st.error("Could not extract valid conversation data from the uploaded file. Please check the file's structure.")
    else:
        st.info("Awaiting your file upload...")

if __name__ == "__main__":
    main()

