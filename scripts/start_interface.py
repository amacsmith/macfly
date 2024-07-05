import subprocess
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Start the Streamlit interface
subprocess.run(["streamlit", "run", "dynamic_interface/app.py"])
