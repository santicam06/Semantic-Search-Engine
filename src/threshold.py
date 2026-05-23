import os, sys, traceback
from utils import load_database, dot_product
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def calculate_top_three(products: list, query: str) -> list:

    if not OPENROUTER_API_KEY:
            print("❌ Error: OPENROUTER_API_KEY not found")
            sys.exit(1)

    openai = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=OPENROUTER_API_KEY
    )

    # Model embedding call for query that exists
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
        # Tuple = (score, title_product, id)
        products_scores.append((p_score, p['title'], p['id']))

    # x represents each tuple, sort in descending and by scores
    products_scores.sort(key=lambda x: x[0], reverse=True)

    # Print top 3 most similar products
    print(f"📊 TOP 3 FOR MOST SIMILAR PRODUCTS: [SCORE, NAME, ID]\n")
    i = 0
    scores_array = []
    while i < 3:
        print(f"{i + 1}. {products_scores[i][0]}, {products_scores[i][1]}, {products_scores[i][2]}\n")
        scores_array.append(products_scores[i][0])
        i = i + 1

    # Array with top 3 scores    
    return scores_array


def get_threshold() -> float:

    try:
        products = load_database()

        
        # Product that exists probably
        good_query = "Elegant and wealthy watch"
        # Product that does not exist
        bad_query = "FIFA World Cup 2026 Album"


        # Calculate top 3 of most similar products for each query

        print(f"\nGOOD TEST CASE TOP:\n🔎 QUERY: {good_query}\n")
        good_scores = calculate_top_three(products, good_query)
        print(f"\nBAD TEST CASE TOP:\n🔎 QUERY: {bad_query}\n")
        bad_scores = calculate_top_three(products, bad_query)

        # Calculate averages of both top 3s
        good_average = sum(good_scores) / len(good_scores)
        print(f"\nGOOD TEST AVERAGE: {good_average}")
        bad_average = sum(bad_scores) / len(bad_scores)
        print(f"BAD TEST AVERAGE: {bad_average}")

        # Calculate Threshold as the average of both previous averages
        MIN_SIMILARITY_SCORE = (good_average + bad_average) / 2

        print(f"\nTHE THRESHOLD (MINIMUM SEMANTIC SCORE) IS: {MIN_SIMILARITY_SCORE}\n")
        
        # For simplicity, just keep the first decimal point
        return round(MIN_SIMILARITY_SCORE, 1)

    except Exception as err:
        print(f"🔴 AN ERROR OCCURRED: {err}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    get_threshold()

