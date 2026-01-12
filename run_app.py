import os
import sys
import subprocess
import webbrowser
import threading
import time

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Checking and installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def run_app():
    """Run the FastAPI application."""
    print("Starting Heart Disease Prediction App...")
    
    # Set Environment Variable for Model Path if not set
    if "MODEL_PATH" not in os.environ:
        # Default to the correct path relative to this script
        os.environ["MODEL_PATH"] = "app/models/heart_disease_model.pkl"

    # Add current directory to sys.path
    sys.path.append(os.getcwd())

    # Open browser in a separate thread
    def open_browser():
        time.sleep(3) # Wait for server to start
        print("Opening browser at http://localhost:8000")
        webbrowser.open("http://localhost:8000")

    threading.Thread(target=open_browser, daemon=True).start()

    # Run Uvicorn
    try:
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
    except ImportError:
        print("Error: uvicorn not found. Please run the script again after installation.")
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    # Ensure we are in the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if dependencies are installed
    try:
        import fastapi
        import uvicorn
        import joblib
        import jinja2
    except ImportError:
        install_dependencies()
    
    run_app()
