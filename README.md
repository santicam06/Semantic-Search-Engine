# Semantic-Search-Engine

LLM used in this application:
- OpenAI Text Embedding 3 Small


## Setup Instructions

Before running the application, follow these steps:

1. For this repository, create a **GitHub Codespace (Cloud)** OR clone it locally and open it with your preferred code editor (e.g. Visual Studio Code, ...).

2. **Install Python** (If not already installed):
   - **Windows**: Download the latest installer from [python.org](https://www.python.org/downloads/windows/) or use: `winget install Python.Python.3.12`
   - **macOS**: Use Homebrew: `brew install python`
   - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install python3 python3-venv python3-pip`
   - **Cloud Workspaces (Codespaces, etc.)**: Python is usually pre-installed. Run `python3 --version` to verify and skip this step.

3. **Create and Activate a Virtual Environment**:

>[!IMPORTANT]
From this point on, make sure that your present working directory on your terminal is the root directory of the application: `./Semantic-Search-Engine`. 

   - Create the environment:
     - **Windows**: `python -m venv .venv`
     - **macOS/Linux**: `python3 -m venv .venv`
   - Activate it:
     - **Windows**: `.\.venv\Scripts\activate`
     - **macOS/Linux**: `source .venv/bin/activate`

4. **Install Dependencies**:
   - Upgrade `pip` and install required libraries:
     ```powershell
     python -m pip install --upgrade pip
     python -m pip install requests openai python-dotenv
     ```

5. **Environment Configuration**:
   - Open the `.env` file located at the root directory. This file contains the required API key for the application, read and set it carefully.

6. Directory Structure
    - `src/`: Contains the source code.
        - `indexer.py`: Script to generate products data and embeddings.
        - `semantic_search.py`: **MAIN SCRIPT** for searching products.
        - `utils.py`: Shared utility functions for serialization, database loading, and similarity calculation.
        - `threshold.py`: Calculates minimum similarity score of potential products according to user search. 
    - `data/`: Local storage for indexed data.
        - `products.json`: Raw product data from the API.
        - `vectors.tsv`: Tab-separated embeddings for the products.
        - `metadata.tsv`: Metadata used for embeddings visualization. 


### Troubleshooting
- **Missing API Key**: Ensure `OPENROUTER_API_KEY` is correctly set in your `.env` file.
- **Dependency Issues**: If running in a new environment, ensure you have executed the commands in **Step 3**.
- **Virtual Environment Not Activated**: If you receive "module not found" errors, ensure your virtual environment is activated **(Step 3)**.


---
### This application is run with ``. Each phase is a separate Python module entrypoint. 
- First 2 phases should be run only for engineering purposes, go down straight to the **Job Advisor** section if you only care about getting that job!