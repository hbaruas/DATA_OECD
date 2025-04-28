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
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')
text = (
    "How Data-Related Task Counts Were Created from Job Advertisements\\n\\n"
    "Understanding data-related activity inside job adverts is not as simple as looking for the word 'data'.\\n"
    "Instead, we used a structured, intelligent process to detect meaningful activities about handling, storing, or analyzing information.\\n\\n"
    "Step 1: Reading job descriptions automatically\\n"
    "- We used a natural language processing (NLP) technique called 'noun chunking' to read each job description.\\n"
    "- A noun chunk is a small group of words centered around a noun, like 'data analysis', 'SQL server', or 'business reports'.\\n\\n"
    "Step 2: Checking for data relevance\\n"
    "- Each noun chunk was compared to the concept of 'data' using semantic similarity (cosine similarity).\\n"
    "- If the phrase was meaningfully related to data work, it was kept.\\n"
    "- This allowed us to capture a wider range of phrases than simple keyword matching (e.g., 'customer database', 'predictive modeling').\\n\\n"
    "Step 3: Classifying into types of data work\\n"
    "- The kept noun chunks were classified into three broad types:\\n"
    "  • data_entry: routine tasks like entering information, processing forms, handling spreadsheets.\\n"
    "  • database: tasks related to organizing or maintaining structured information systems, like SQL, data warehouses.\\n"
    "  • data_analytics: tasks focused on making sense of information, finding patterns, using statistics or machine learning.\\n\\n"
    "Step 4: Counting the activities\\n"
    "- We counted how many times each type of data work appeared per job advert.\\n"
    "- These counts were then summed across occupations (SOC codes) and sectors.\\n"
    "- This gave us a numeric way to measure how 'data-heavy' different jobs and industries are.\\n\\n"
    "What this represents\\n"
    "- The counts are a proxy for real-world data work expected from jobseekers.\\n"
    "- Instead of relying on job titles (which can be misleading), this method measures the actual content of job tasks.\\n"
    "- Sectors with higher counts are more deeply embedded with data responsibilities across their workforce.\\n\\n"
    "Important:\\n"
    "- No manual labeling was done — the system automatically detected, scored, and classified thousands of job descriptions without human bias.\\n"
    "- The counts were later used to create sector-level indicators like Alpha (data activity per £ invested) and Share of GVA (economic importance of data work).\\n"
)
ax.text(0.05, 0.95, text, va='top', wrap=True)
pdf.savefig()
plt.close()
