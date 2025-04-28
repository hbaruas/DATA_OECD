import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

# ----------------------------
# Setup: File paths and folders
# ----------------------------
# Create the output folder if it doesn't exist
output_dir = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Reports"
os.makedirs(output_dir, exist_ok=True)

# Input and output files
data_path = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/sector_level_intensity.csv"
pdf_path = os.path.join(output_dir, "sector_level_report.pdf")

# ----------------------------
# Load sector data
# ----------------------------
df = pd.read_csv(data_path)

# Create PDF
pdf = PdfPages(pdf_path)

# ----------------------------
# Plot 1: Alpha by Sector
# ----------------------------
plt.figure(figsize=(10, 6))
df_sorted_alpha = df.sort_values("alpha", ascending=False)
plt.bar(df_sorted_alpha["sector"], df_sorted_alpha["alpha"], color='steelblue')
plt.title("Data Investment Ratio (Alpha) by Sector")
plt.ylabel("Alpha (data_total / Investment)")
plt.xticks(rotation=45)
plt.tight_layout()
pdf.savefig()
plt.close()

# ----------------------------
# Plot 2: Share of GVA by Sector
# ----------------------------
plt.figure(figsize=(10, 6))
df_sorted_gva = df.sort_values("share_of_GVA", ascending=False)
plt.bar(df_sorted_gva["sector"], df_sorted_gva["share_of_GVA"], color='seagreen')
plt.title("Share of GVA from Data Activity by Sector")
plt.ylabel("Share of GVA")
plt.xticks(rotation=45)
plt.tight_layout()
pdf.savefig()
plt.close()

# ----------------------------
# Plot 3: Stacked Bar – Data Activities by Sector
# ----------------------------
plt.figure(figsize=(12, 6))
df.set_index("sector")[["data_entry", "database", "data_analytics"]].plot(
    kind='bar', stacked=True, figsize=(12, 6), colormap='tab20c')
plt.title("Breakdown of Data Activities by Sector")
plt.ylabel("Count of Noun Chunks")
plt.xticks(rotation=45)
plt.tight_layout()
pdf.savefig()
plt.close()

# ----------------------------
# Plot 4: Summary Table
# ----------------------------
fig, ax = plt.subplots(figsize=(12, 5))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.round(6).values,
                 colLabels=df.columns,
                 loc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.2)
plt.title("Sector-level Summary Table")
pdf.savefig()
plt.close()

# ----------------------------
# Save PDF
# ----------------------------
pdf.close()
print(f"✅ PDF report generated and saved to:\n{pdf_path}")





















import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Set paths
output_dir = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Reports"
os.makedirs(output_dir, exist_ok=True)
data_path = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/sector_level_intensity.csv"
pdf_path = os.path.join(output_dir, "sector_level_report.pdf")

# Load data
df = pd.read_csv(data_path)

# Open PDF
pdf = PdfPages(pdf_path)

# Chart 1: Alpha by Sector
plt.figure(figsize=(10,6))
df_sorted_alpha = df.sort_values("alpha", ascending=False)
plt.bar(df_sorted_alpha["sector"], df_sorted_alpha["alpha"], color='steelblue')
plt.title("Alpha by Sector")
plt.xlabel("Sector")
plt.ylabel("Alpha (unitless ratio)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
pdf.savefig()
plt.close()

# Explanation for Chart 1
fig, ax = plt.subplots(figsize=(10,6))
ax.axis('off')
text = (
    "Alpha by Sector\n\n"
    "This chart shows the Alpha value for each sector.\n\n"
    "- Alpha measures how much data-related work happens for every £1 invested.\n"
    "- Higher Alpha = more data productivity per pound.\n\n"
    "How Alpha is calculated:\n"
    "  Alpha = data_total / Investment\n\n"
    "- data_total: Total number of data-related noun chunks (derived)\n"
    "- Investment: Total capital invested in the sector (synthetic)\n\n"
    "Interpretation:\n"
    "  If Alpha = 2.5, it means 2.5 units of data tasks happen for every £1 million invested.\n"
)
ax.text(0.05, 0.95, text, va='top', wrap=True)
pdf.savefig()
plt.close()

# Chart 2: Share of GVA by Sector
plt.figure(figsize=(10,6))
df_sorted_gva = df.sort_values("share_of_GVA", ascending=False)
plt.bar(df_sorted_gva["sector"], df_sorted_gva["share_of_GVA"], color='seagreen')
plt.title("Share of GVA by Sector")
plt.xlabel("Sector")
plt.ylabel("Share of GVA (unitless ratio)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
pdf.savefig()
plt.close()

# Explanation for Chart 2
fig, ax = plt.subplots(figsize=(10,6))
ax.axis('off')
text = (
    "Share of GVA by Sector\n\n"
    "This chart shows the share of a sector's economic output linked to data tasks.\n\n"
    "- Share of GVA measures how much of a sector's value is driven by data activities.\n\n"
    "How Share of GVA is calculated:\n"
    "  Share of GVA = data_total / GVA\n\n"
    "- data_total: Total number of data-related noun chunks (derived)\n"
    "- GVA: Gross Value Added of the sector (synthetic)\n\n"
    "Interpretation:\n"
    "  If Share of GVA = 0.005, it means 0.5% of the sector's economic value comes from data work.\n"
)
ax.text(0.05, 0.95, text, va='top', wrap=True)
pdf.savefig()
plt.close()

# Chart 3: Stacked Bar - Data Task Breakdown
plt.figure(figsize=(10,6))
df.set_index("sector")["data_entry" "database" "data_analytics".split()].plot(kind="bar", stacked=True, figsize=(10,6), colormap='tab20c')
plt.title("Breakdown of Data-Related Tasks by Sector")
plt.xlabel("Sector")
plt.ylabel("Count of Noun Chunks")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
pdf.savefig()
plt.close()

# Explanation for Chart 3
fig, ax = plt.subplots(figsize=(10,6))
ax.axis('off')
text = (
    "Data Task Breakdown by Sector\n\n"
    "This stacked bar shows how different types of data tasks contribute inside each sector.\n\n"
    "Categories:\n"
    "- data_entry: Routine input or processing of information (derived)\n"
    "- database: Management of structured storage (derived)\n"
    "- data_analytics: Analytical or predictive tasks (derived)\n\n"
    "Interpretation:\n"
    "  Helps identify whether a sector is admin-heavy, IT-heavy, or analytics-heavy.\n"
)
ax.text(0.05, 0.95, text, va='top', wrap=True)
pdf.savefig()
plt.close()

# Chart 4: Table - Full Sector Summary
fig, ax = plt.subplots(figsize=(12,8))
ax.axis('off')
ax.table(
    cellText=df.round(6).values,
    colLabels=df.columns,
    loc='center',
    cellLoc='center'
)
pdf.savefig()
plt.close()

# Explanation for Chart 4
fig, ax = plt.subplots(figsize=(10,6))
ax.axis('off')
text = (
    "Sector Summary Table\n\n"
    "This table contains all sector-level metrics used in the report:\n"
    "- sector: Industry label\n"
    "- data_entry, database, data_analytics: Derived counts of noun chunks\n"
    "- data_total: Sum of all data-related chunks (derived)\n"
    "- GVA: Gross Value Added (synthetic, £ millions)\n"
    "- Investment: Capital Investment (synthetic, £ millions)\n"
    "- alpha: Data tasks per £ invested (derived)\n"
    "- share_of_GVA: Proportion of sector value from data work (derived)\n"
)
ax.text(0.05, 0.95, text, va='top', wrap=True)
pdf.savefig()
plt.close()

# Close PDF
pdf.close()

print(f"✅ PDF report generated and saved to:\n{pdf_path}")







# Additional Full Explanation: How Data-Related Task Counts Were Created
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')
text = (
    "1. What are 'noun chunks' in this project?\\n"
    "    • A noun chunk is a small meaningful group of words extracted from a sentence, centered around a noun.\\n"
    "    • Example from a job description:\\n"
    "    • Sentence: 'Experience with SQL databases is essential.'\\n"
    "    • Noun chunks detected: 'Experience', 'SQL databases'\\n"
    "    • We extracted noun chunks automatically from job descriptions using a natural language processing (NLP) tool called SpaCy.\\n"
    "⸻\\n"
    "\\n"
    "2. How did we find 'data-related' noun chunks?\\n"
    "    • After extracting all noun chunks, we compared each noun chunk to the word 'data' using a mathematical similarity measure called cosine similarity.\\n"
    "    • Cosine similarity checks how close two ideas are in meaning, not just matching exact words.\\n"
    "    • If a noun chunk was meaningfully similar to 'data', we kept it.\\n"
    "    • Example:\\n"
    "    • Noun chunk: 'SQL databases' → Similar to 'data' → kept.\\n"
    "    • Noun chunk: 'cafeteria manager' → Not similar → ignored.\\n"
    "⸻\\n"
    "\\n"
    "3. Classification into Categories\\n"
    "    • Each kept noun chunk was then categorized into one of three types:\\n"
    "    • data_entry (e.g., admin tasks like 'data input', 'typing records')\\n"
    "    • database (e.g., tech infrastructure like 'SQL server', 'data warehouse')\\n"
    "    • data_analytics (e.g., analyzing information like 'data modeling', 'predictive analytics')\\n"
    "⸻\\n"
    "\\n"
    "4. Counting the Data Tasks\\n"
    "    • For each job advert:\\n"
    "    • We counted how many noun chunks fell into each category.\\n"
    "    • These counts were then:\\n"
    "        • Summed up per job\\n"
    "        • Aggregated up to SOC codes\\n"
    "        • Aggregated up to Sectors\\n"
    "    • These counts are what we refer to as 'data-related activity' in the report.\\n"
)
ax.text(0.05, 0.95, text, va='top', wrap=True)
pdf.savefig()
plt.close()
