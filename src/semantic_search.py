import sys, traceback, os
from utils import load_database, search_products, DATA_DIR
from indexer import main_indexer


def main():

    try:
        # Check if any of the three database files are missing
        data_files = [
            os.path.join(DATA_DIR, "products.json"),
            os.path.join(DATA_DIR, "vectors.tsv"),
            os.path.join(DATA_DIR, "metadata.tsv")
        ]
        files_missing = any(not os.path.exists(f) for f in data_files)

        if files_missing:
            # Create data directory if it doesn't exist (already handled in indexer but good for safety)
            os.makedirs(DATA_DIR, exist_ok=True)
            main_indexer()

        products = load_database()
        wants_search = True

        while wants_search:
            query = input("\n🛍️  What product are you looking for? ")
            matches = search_products(query, products)

            if len(matches) == 0:
                print("Sorry, we don't have anything like that in stock.")
            else:
                print(f"💡 Found {len(matches)} most similar matches: \n")

                # Print top 5 (or less) most similar products: [SCORE, NAME, PRICE]
                i = 0
                while i < len(matches):
                    print(f"{i + 1}. [Score: {matches[i][0]}] {matches[i][1]} - ${matches[i][2]}\n")
                    i = i + 1

            repeat_command = True
            while repeat_command:
                exit = input("\n\n DO YOU WANT TO EXIT? (YES/ NO) ")
                if exit.lower() == "yes": 
                    wants_search = False 
                    repeat_command = False
                elif exit.lower() == "no": repeat_command = False
                else:
                    print("🤔 Unrecognized input, try again.")


    except Exception as err:
        print(f"🔴 AN ERROR OCCURRED: {err}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
