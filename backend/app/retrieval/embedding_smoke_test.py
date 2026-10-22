from app.retrieval.embeddings import generate_embedding


text = "Refunds greater than INR 50,000 require manager approval."

embedding = generate_embedding(text)

print("Gemini embedding successful")
print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])
