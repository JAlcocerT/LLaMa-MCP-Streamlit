import subprocess

def run_streamlit():
    """Run the Streamlit app."""
    subprocess.run(["streamlit", "run", "app/nvidia.py"])