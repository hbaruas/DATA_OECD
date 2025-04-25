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
