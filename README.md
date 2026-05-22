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
        - `products.json`: Raw product data from the `DummyJSON` API.
        - `vectors.tsv`: Tab-separated embeddings for the products.
        - `metadata.tsv`: Metadata used for embeddings visualization. 


### Troubleshooting
- **Missing API Key**: Ensure `OPENROUTER_API_KEY` is correctly set in your `.env` file.
- **Dependency Issues**: If running in a new environment, ensure you have executed the commands in **Step 3**.
- **Virtual Environment Not Activated**: If you receive "module not found" errors, ensure your virtual environment is activated **(Step 3)**.


---
## This application contains **two** main files: 

### `semantic_search.py` (end-users usage)
The application asks for a product you are looking for and according to your query it displays a Top 5 (or less, if fewer products surpass the minimum threshold for similarity scores) of the most similar products found.

Run command:
```powershell
# Windows
python src\semantic_search.py
# macOS/Linux
python3 src\semantic_search.py
```

### `threshold.py` (engineering analysis only) 
Calculates the MINIMUM similarity score threshold that a product can have related to the user's query, in order to appear in the Top 5.

Run command:
```powershell
# Windows
python src\threshold.py
# macOS/Linux
python3 src\threshold.py
```

#### Script Functionality
This script uses two queries: 
1) A good one which potentially will give desired products.
2) A bad one which will try to fetch products as most similar as possible, but not giving exact ones as desired. 

- Calculates the top three products, for both queries.  
- Calculates the average score in each top.
- Calculates a Grand Mean; from both previous averages, equal to the threshold.

> [!NOTE]
Currently, the threshold is set to be `0.3`, you can modify the queries in this script in order to see the variations.

#### What is the similarity score of a product? 
The similarity score is a floating-point number calculated by performing dot product between the **embedding dimensions** of the user's query with the ones from a single product that is being evaluated to be relevant or not.

The **highest** five product scores (i.e. the most semantically similar to the user's query) are selected for the Top 5.

> [!TIP]
The file `data\vectors.tsv` contains rows (one per product) with embedding dimensions (floating-point numbers) that mathematically represent the semantic features of a product (e.g. its usage, color, brand, size, material, etc...). In total there are 1536 dimensions per row. Each of these rows is used along with the user's query dimensions as aforementioned.

#### Quick example for calculating the similarity score
Imagine we use only **2 dimensions** (instead of 1536) to represent products' embeddings:

- **User Query:** "Smart phone" → Vector: `[0.8, 0.1]`

- **Product A:** "Apple iPhone" → Vector: `[0.9, 0.2]`
- **Product B:** "Wooden Chair" → Vector: `[0.1, 0.8]`

**The Math (Dot Product):**
1. **Score for Product A:** `(0.8 * 0.9) + (0.1 * 0.2)` = **0.74** (Close to 1.0 and above threshold = High Similarity)
2. **Score for Product B:** `(0.8 * 0.1) + (0.1 * 0.8)` = **0.16** (Close to 0.0 and below threshold = Low Similarity)

The engine recognizes that the "Smart phone" query is mathematically much closer to the "iPhone" than the "Chair".