import requests, os, json, sys, traceback
from utils import serialize_product, DATA_DIR
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def main_indexer():

    try:
        url = 'https://dummyjson.com/products?limit=200'
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.HTTPError(f"Request failed with status {response.status_code}: {response.text}")

        # Initialize the file with JSON data
        products = response.json()

        if not products or not products.get("products"):
            raise ValueError("No products found in the API response or response format is invalid.")

        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        products_path = os.path.join(DATA_DIR, "products.json")
        with open(products_path, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        # Create array of serialized strings
        array_serials = []
        for product in products["products"]:
            array_serials.append(serialize_product(product))

        # DEBUG: Print first 3 serialized strings to verify format
        print("\n--- DEBUG: FIRST 3 SERIALIZED STRINGS ---")
        for s in array_serials[:3]:
            print(f"DEBUG: {s}\n")
        print("------------------------------------------\n")


        # Model embedding call
        if not OPENROUTER_API_KEY:
            print("❌ Error: OPENROUTER_API_KEY not found")
            sys.exit(1)

        openai = OpenAI(
          base_url="https://openrouter.ai/api/v1",
          api_key=OPENROUTER_API_KEY
        )

        params = {
            "model": "openai/text-embedding-3-small",
            "input": array_serials,
            "encoding_format": 'float',
        }

        try:
            textembed = openai.embeddings.create(**params) 
            embeds_collector = []

            # Collect each embedding vector (1 vector = 1 product)
            for item in textembed.data:
                # Collect one line of dimensions (one line = one product)
                embeds_collector.append('\t'.join(str(dimension) for dimension in item.embedding))

            # Write embeddings to file according to format 
            vectors_path = os.path.join(DATA_DIR, "vectors.tsv")
            with open(vectors_path, "w", encoding="utf-8") as f:
                f.write('\n'.join(embeds_collector))

        except RateLimitError:
            print("❌ Rate limit exceeded. Please wait and try again later.")
            sys.exit(1)


        # Write Visualization tool content
        metadata_path = os.path.join(DATA_DIR, "metadata.tsv")
        with open(metadata_path, "w", encoding="utf-8") as f:
            # HEADERS
            f.write("Title\tCategory\n")

            for product in products["products"]:
                # Use original dictionary to get values per product
                title = str(product.get("title", "-")).replace('\t', ' ').replace('\n', ' ')
                categ = str(product.get("category", "-")).replace('\t', ' ').replace('\n', ' ')

                line = f"{title}\t{categ}"
                f.write(line + '\n')
            

    except Exception as err:
        print(f"🔴 AN ERROR OCCURRED: {err}")
        traceback.print_exc()
        sys.exit(1)



if __name__ == "__main__":
    main_indexer()
