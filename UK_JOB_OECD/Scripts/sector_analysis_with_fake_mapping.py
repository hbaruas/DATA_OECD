import pandas as pd
import random

# ----------------------------
# STEP 1: Load SOC-level data
# ----------------------------
df_soc = pd.read_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/soc_level_aggregated.csv")

# ----------------------------
# STEP 2: Prepare soc_code column
# ----------------------------
df_soc["soc_code"] = df_soc["soc_code"].astype(str).str.split(".").str[0]

# ----------------------------
# STEP 3: Generate dummy sector mapping
# ----------------------------
unique_soc_codes = df_soc["soc_code"].unique()
random.seed(42)

# Define fake sector labels
sector_labels = ["Retail", "Health", "Admin", "Tech", "Legal", "Finance", "Transport", "IT", "Engineering"]

# Randomly assign each soc_code to a sector
soc_to_sector = {soc: random.choice(sector_labels) for soc in unique_soc_codes}
df_map = pd.DataFrame(list(soc_to_sector.items()), columns=["soc_code", "sector"])

# ----------------------------
# STEP 4: Generate dummy GVA and Investment for each sector
# ----------------------------
df_sut = pd.DataFrame(sector_labels, columns=["sector"])
df_sut["GVA"] = [random.randint(400_000_000, 1_000_000_000) for _ in sector_labels]
df_sut["Investment"] = [random.randint(15_000_000, 60_000_000) for _ in sector_labels]

# ----------------------------
# STEP 5: Merge and aggregate
# ----------------------------
df_merged = df_soc.merge(df_map, on="soc_code", how="left")

df_sector = df_merged.groupby("sector").agg({
    "data_entry": "sum",
    "database": "sum",
    "data_analytics": "sum"
}).reset_index()

df_sector["data_total"] = df_sector[["data_entry", "database", "data_analytics"]].sum(axis=1)

df_sector = df_sector.merge(df_sut, on="sector", how="left")

df_sector["alpha"] = df_sector["data_total"] / df_sector["Investment"]
df_sector["share_of_GVA"] = df_sector["data_total"] / df_sector["GVA"]

# ----------------------------
# STEP 6: Save result
# ----------------------------
output_path = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/sector_level_intensity.csv"
df_sector.to_csv(output_path, index=False)

print("✅ Sector-level analysis complete. Output saved to:")
print(output_path)
