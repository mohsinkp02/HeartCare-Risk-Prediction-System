# HeartCare Risk Prediction System

An end-to-end machine learning–based web application for predicting cardiovascular disease risk using lifestyle and health attributes.

## Key Features

- **FastAPI Backend**: Modern, high-performance web API.
- **Machine Learning Integration**: Real-time risk prediction using a trained Random Forest model.
- **Modern UI**: Clean, responsive interface for user data entry and results visualization.
- **Git LFS**: Large model files managed via Git Large File Storage.

## Project Structure

```
production_solution/
├── app/                    # Application Source Code
│   ├── api/                # API Route Definitions
│   ├── core/               # App Configuration and Logging
│   ├── models/             # Trained ML Models (LFS tracked)
│   ├── schemas/            # Data Validation Schemas
│   ├── services/           # Business Logic (Preprocessing & Prediction)
│   ├── static/             # CSS, JavaScript, and Images
│   ├── templates/          # HTML Templates
│   └── main.py             # FastAPI Application Factory
├── .gitattributes          # Git LFS Configuration
├── .gitignore              # Git Ignore Rules
├── requirements.txt        # Python Dependencies
└── run_app.py              # Application Entry Point
```

## Getting Started

### Prerequisites

- Python 3.9+
- [Git LFS](https://git-lfs.com/) (Required to download the model file)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mohsinkp02/HeartCare-Risk-Prediction-System.git
   cd HeartCare-Risk-Prediction-System
   ```

2. **Initialize Git LFS**:
   ```bash
   git lfs install
   git lfs pull
   ```

3. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the application using the runner script:

```bash
python run_app.py
```

The application will be available at [http://localhost:8000](http://localhost:8000).

## Troubleshooting

### Network Issues (Port 443)
If you encounter "Failed to connect to github.com port 443" errors during push/pull:
- Check if your firewall or antivirus (like Avast) is blocking Git.
- Try temporarily disabling your antivirus shields or adding Git to the whitelist.
- Alternatively, try using a mobile hotspot or a different network.

## Deployment Note
The model file (`app/models/heart_disease_model.pkl`) is stored using **Git LFS**. Ensure you have Git LFS installed to properly download the model when cloning.
