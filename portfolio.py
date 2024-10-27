import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, dataset_path="portfolio.csv"):
        self.df = pd.read_csv(dataset_path)
        self.chroma_client = chromadb.PersistentClient('chroma_store')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],  # Wrap single string in list
                    metadatas=[{"links": row["Links"]}],  # Wrap single metadata in list
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        # Ensure skills is a list and convert to list if it's a single string
        if isinstance(skills, str):
            skills = [skills]
        
        try:
            results = self.collection.query(
                query_texts=skills,
                n_results=2
            )
            return results.get('metadatas', [[]])[0]  # Return first set of metadata
        except Exception as e:
            print(f"Error querying portfolio: {e}")
            return []