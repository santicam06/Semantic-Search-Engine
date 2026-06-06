# Semantic-Search-Engine

With a catalogue of 195+ products, this engine retrieves the most similar ones according to your query; by following the semantic similarity principle through embeddings. **Search for cosmetics, accesories, furniture, sports apparel/tools, among others!**

## LLM used in this application:
- [OpenAI Text Embedding 3 Small](https://openrouter.ai/openai/text-embedding-3-small)


## ⚙️ Setup Instructions

Before running the application, follow these steps:

1. For this repository, create a **GitHub Codespace (Cloud)** OR clone it locally and open it with your preferred code editor (e.g. Visual Studio Code, ...).

>[!IMPORTANT]
From this point on, make sure that your present working directory on your terminal is the root directory of the application: `.\Semantic-Search-Engine`. 

2. **Install Python** (If not already installed):
   - **Windows**: Download the latest installer from [python.org](https://www.python.org/downloads/windows/) or use: `winget install Python.Python.3.12`
   - **macOS**: Use Homebrew: `brew install python`
   - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install python3 python3-venv python3-pip`
   - **Cloud Workspaces (Codespaces, etc.)**: Python is usually pre-installed. Run `python3 --version` to verify and skip this step.

3. **Create and Activate a Virtual Environment**:

   - Create the environment:
     - **Windows**: `python -m venv .venv`
     - **macOS/Linux**: `python3 -m venv .venv`
   - Activate it:
     - **Windows**: `.\.venv\Scripts\activate`
     - **macOS/Linux**: `source .venv/bin/activate`

4. **Install Dependencies**:
   - Upgrade `pip` and install required libraries:
     ```sh
     python -m pip install --upgrade pip
     python -m pip install requests openai python-dotenv
     ```

5. **Environment Configuration**:
   - Create a local `.env` file by copying the template file `.env.example`. This file contains the required API key for the application, read and set it carefully.
```sh
     # Windows
     copy .env.example .env
     # macOS/Linux or PowerShell
     cp .env.example .env
   ```
> [!IMPORTANT]
Always **copy** the template. Do not rename `.env.example` directly, as it should remain in the repository as a reference for required environment variables.

6. Directory Structure
    - `src\`: Contains the source code.
        - `indexer.py`: Script to generate products data and embeddings.
        - `semantic_search.py`: **MAIN SCRIPT** for searching products.
        - `utils.py`: Shared utility functions for serialization, database loading, and similarity calculation.
        - `threshold.py`: Calculates minimum similarity score of potential products according to user search. 
    - `data\`: Local storage for indexed data.
        - `products.json`: Raw product data from the `DummyJSON` API.
        - `vectors.tsv`: Tab-separated embeddings for the products.
        - `metadata.tsv`: Metadata used for embeddings visualization. 


### 🚨 Troubleshooting
- **Missing API Key**: Ensure `OPENROUTER_API_KEY` is correctly set in your `.env` file.
- **Dependency Issues**: If running in a new environment, ensure you have executed the commands in **Step 3** onwards.
- **Virtual Environment Not Activated**: If you receive "module not found" errors, ensure your virtual environment is activated **(Step 3)**.
- **Persistent Environment Errors**: If you encounter any other unusual errors with your Python environment, manually delete the `.venv` folder and repeat the process starting from **Step 3**.


---
## This application contains **two** main modules + an Extra tool 

### 1) `semantic_search.py` (end-users usage)
The application asks for a product you are looking for and according to your search it displays Top 5 most similar products found (or less, if fewer products surpass the minimum similarity score **threshold**).

Run command:
```sh
# Windows
python src\semantic_search.py
# macOS/Linux
python3 src/semantic_search.py
```

After each search, the application will ask **"DO YOU WANT TO EXIT? (YES/NO)"**:
- **YES**: Terminates the program.
- **NO**: Returns you to the search prompt for another query.

---
### 2) `threshold.py` (engineering/analysis usage only) 
Calculates the MINIMUM similarity score threshold that a product can have related to the user's query, in order to appear in the Top 5.

Run command:
```sh
# Windows
python src\threshold.py
# macOS/Linux
python3 src/threshold.py
```

#### Script Functionality
This script uses two queries: 
1) A good one which potentially will return desired products.
2) A bad one which will try to fetch products as most similar as possible, but not returning exact ones as desired. 

- Calculates the top three products, for each query.  
- Calculates the average score in each top.
- Calculates a Grand Mean; from both previous averages, equal to the threshold.

> [!NOTE]
Currently, the threshold is set to be `0.3`, you can modify the queries in this script in order to see the variations.

#### What is the similarity score of a product? 
The similarity score is a floating-point number calculated by performing dot product between the **embedding dimensions** of the user's query with the ones from a single product that is being evaluated to be relevant or not for the query.

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


## 🔭 Visualizing the products' embeddings in a 3D space (optional tool, knowledge enrichment purposes)
If you are curious about the embeddings logic, you can follow these steps to generate a 3D representation of all the products listed in this application and how do they visually group in an Embedding Space according to their semantic meaning.

1. Open the [TensorFlow Embedding Projector](https://projector.tensorflow.org/).
2. Click the **"Load"** button on the left sidebar.
3. Upload your `data\vectors.tsv` file to the "Step 1: Load a TSV file of vectors" slot.
4. Upload your `data\metadata.tsv` file to the "Step 2: Load a TSV file of metadata" slot.
5. Click outside the modal to close it.

**Explore your data:**

- You should see a 3D cloud of points.
- In the right-hand search bar, search for any **Title** or **Category** present in the `metadata.tsv` file. Notice how all the related products are clustered tightly together? The red spots nearby are the most 
- Click on a spot. The redder the neighboring spots are, the more closely they are correlated. The yellow spots are still related but less so.
- Look at the "Nearest points in the original space" list on the right. You should see other similar items. 


## Final Step: Deactivate the Virtual Environment

Once you are finished working with the application, you can deactivate the virtual environment to return to your global Python context:

```sh
# Terminal
deactivate
```
