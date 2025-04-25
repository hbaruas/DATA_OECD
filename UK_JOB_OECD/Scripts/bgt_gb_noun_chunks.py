import pandas as pd
import spacy

# Load CSV directly (your 2022 job data)
df = pd.read_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/enriched_with_soc.csv")

# Drop rows with missing descriptions (optional but useful)
df.dropna(subset=["jobDescription"], inplace=True)

# Remove numbers from text
def remove_numbers(text):
    return ''.join(filter(lambda c: not c.isdigit(), str(text)))

df["clean_description"] = df["jobDescription"].apply(remove_numbers)

# Load SpaCy model
nlp = spacy.load("en_core_web_lg")  # use 'en_core_web_lg' if available
target_token = nlp("data")[0]  # this is the word you compare to

# Process descriptions
docs = list(nlp.pipe(df["clean_description"], disable=["ner", "lemmatizer"]))

# Extract noun chunks + cosine similarity
output = []

for i, doc in enumerate(docs):
    for chunk in doc.noun_chunks:
        if chunk.has_vector:
            output.append({
                "job_id": df.iloc[i]["jobId"],
                "title": df.iloc[i]["jobTitle"],
                "noun_chunk": chunk.text,
                "similarity_to_data": chunk.similarity(target_token),
                "soc_code": df.iloc[i]["soc_code"],
                "description": df.iloc[i]["jobDescription"],
                "date": df.iloc[i]["date"]
            })

# Save result as a DataFrame
result_df = pd.DataFrame(output)

# Optional: Save to Parquet or CSV
result_df.to_csv("noun_chunks_with_similarity.csv", index=False)
# result_df.to_parquet("noun_chunks_with_similarity.parquet", index=False)

print("Done! Results saved.")