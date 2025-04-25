import pandas as pd

# Load data (adjust path as needed)
df = pd.read_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Scripts/noun_chunks_with_similarity.csv")

# ----------------------------
# STEP 1: Filter by similarity
# ----------------------------
SIMILARITY_THRESHOLD = 0.45
df = df[df['similarity_to_data'] >= SIMILARITY_THRESHOLD]

# ----------------------------
# STEP 2: Classify noun chunks
# ----------------------------
def chunk_tagger(chunk):
    chunk = chunk.lower()
    if any(w in chunk for w in ["typing", "form", "input", "record", "admin"]):
        return "data_entry"
    elif any(w in chunk for w in ["sql", "database", "oracle", "server", "data warehouse"]):
        return "database"
    elif any(w in chunk for w in ["analytics", "model", "analysis", "visualisation", "python", "machine learning"]):
        return "data_analytics"
    return "other"

df["Type"] = df["noun_chunk"].apply(chunk_tagger)

# ----------------------------
# STEP 3: Add 1 counter per chunk
# ----------------------------
df["counter"] = 1  # for aggregations

# ----------------------------
# STEP 4: Pivot to job level
# ----------------------------
job_level = df.pivot_table(index="job_id", 
                           columns="Type", 
                           values="counter", 
                           aggfunc="sum",
                           fill_value=0).reset_index()

# Fill missing types
for col in ["data_entry", "database", "data_analytics"]:
    if col not in job_level.columns:
        job_level[col] = 0

# Total count of data-related noun chunks
job_level["Count_DataTerms"] = job_level[["data_entry", "database", "data_analytics"]].sum(axis=1)

# ----------------------------
# STEP 5: Filter jobs with low counts
# ----------------------------
DATA_TERM_THRESHOLD = 2
job_level = job_level[job_level["Count_DataTerms"] > DATA_TERM_THRESHOLD]

# ----------------------------
# STEP 6: Filter main df to relevant job_ids
# ----------------------------
df = df[df["job_id"].isin(job_level["job_id"])]

# Merge job-level aggregates into main df
df = df.merge(job_level, on="job_id", suffixes=("", "_job"))

# ----------------------------
# STEP 7: Aggregate to SOC level
# ----------------------------
soc_agg = df.groupby("soc_code").agg({
    "data_entry": "sum",
    "database": "sum",
    "data_analytics": "sum",
    "job_id": "count"
}).reset_index()

# Compute data intensity per SOC
soc_agg["data_intensity"] = soc_agg[["data_entry", "database", "data_analytics"]].sum(axis=1)

# ----------------------------
# STEP 8: Save Outputs
# ----------------------------
df.to_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/filtered_chunks.csv", index=False)
job_level.to_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/job_level_aggregated.csv", index=False)
soc_agg.to_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/soc_level_aggregated.csv", index=False)

print("✅ Pipeline complete. Outputs saved.")
