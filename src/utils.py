import json, sys, traceback, os
from typing import List, Dict, Any
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Path handling: define DATA_DIR relative to this file's location
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(FILE_DIR, "..", "data")


# Combines the product's title, category, description, tags, and brand into a single line
def serialize_product(product: dict) -> str:

    if not product:
        raise ValueError('Product is a null object')

    title = product.get("title") or "-"
    category = product.get("category") or "-"
    description = product.get("description") or "-"

    tags = product.get("tags")
    brand = product.get("brand") or "-"
    
    # Join elements of tags array into a single string, if tags is not an array set default value    
    tags_str = ", ".join(tags) if isinstance(tags, list) else "-"

    return f"Title: {title} | Category: {category} | Description: {description} | Tags: {tags_str} | Brand: {brand}"


def dot_product(vec_a: list[float], vec_b: list[float]) -> float:
    return sum(a * b for a, b in zip(vec_a, vec_b))


def load_database():
    # 1. Read the JSON file
    products_path = os.path.join(DATA_DIR, 'products.json')
    with open(products_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        products = data['products']

    # 2. Read the TSV file
    vectors_path = os.path.join(DATA_DIR, 'vectors.tsv')
    with open(vectors_path, 'r', encoding='utf-8') as f:
        vectors_data = f.read()
        # Array, each line is the vector of a specific product 
        vector_lines = vectors_data.strip().split('\n')

    # 3. Attach vectors to products
    # Python's zip() function pairs the two lists automatically
    products_with_embeddings = []

    for product, line in zip(products, vector_lines):
        # Convert vector tab-separated values to a list of floats
        vector = [float(x) for x in line.split('\t')]

        # Add the embedding to the product dictionary
        product['embedding'] = vector
        products_with_embeddings.append(product)

    return products_with_embeddings


def calculate_top_five(products: list, query: str, min_score: float) -> list:
    if not OPENROUTER_API_KEY:
            print("❌ Error: OPENROUTER_API_KEY not found")
            sys.exit(1)

    openai = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=OPENROUTER_API_KEY
    )

    # Model embedding call for query
    params = {
        "model": "openai/text-embedding-3-small",
        # QUERY
        "input": query,
        "encoding_format": 'float',
    }

    try:
        textembed = openai.embeddings.create(**params) 
        query_vector = textembed.data[0].embedding

    except RateLimitError:
        print("❌ Rate limit exceeded. Please wait and try again later.")
        sys.exit(1)

    # Perform Dot Product for each database product vs query
    # Array to store tuples of each product
    products_scores = []
    for p in products:
        p_score = dot_product(query_vector, p['embedding'])
        # Tuple = (score, title_product, price)
        products_scores.append((p_score, p['title'], p['price']))

    # x represents each tuple, sort in descending and by scores
    products_scores.sort(key=lambda x: x[0], reverse=True)

    # Safe print of top scores (avoids IndexError if results < 5)
    top_raw_scores = [tup[0] for tup in products_scores[:5]]

    # Use truncation instead of rounding to be honest about the threshold filter
    # (e.g., 0.29996 becomes 0.2999 so it doesn't look like it should pass a 0.3 threshold)
    truncated_display = [f"{int(v * 10000) / 10000:.4f}" for v in top_raw_scores]
    print(f"🔍 Top scores before threshold filter: {', '.join(truncated_display)}")
    print(f"🛑 Score threshold is >= {min_score}")
    # Filter and remove products with insufficient score
    products_scores = [tup for tup in products_scores if tup[0] >= min_score]

    # Array with top 5 product tuples  
    return products_scores[:5]



def search_products(
    query: str,
    products: List[Dict[str, Any]],
    # Calculated by `src\threshold.py` 
    min_score: float = 0.3   
) -> List[tuple]:
    
    try:
        return calculate_top_five(products, query, min_score)
    
    except Exception as err:
        print(f"🔴 AN ERROR OCCURRED: {err}")
        traceback.print_exc()
        sys.exit(1)
