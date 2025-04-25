# Project Technical Walkthrough: UK Job Adverts Data Intensity Pipeline

# Project Technical Walkthrough: UK Job Adverts Data Intensity Pipeline



# File: `synthetic_soc_data.py`
**Purpose:**
To assign a Standard Occupational Classification (SOC) code to each job advert in the scraped dataset. Since Reed job adverts do not come with SOC codes, this script uses simple rule-based logic and fallback random assignment to simulate SOC tagging. This prepares the data for downstream task classification and aggregation.

---

### Step-by-Step Breakdown

#### Step 1: Load Input Data
```python
df = pd.read_csv("Data/reed_jobs_uk_extended.csv")
```
**What it does:** Loads the raw job adverts scraped from the Reed API.

**Expected columns include:**
- `jobId`: Unique job identifier
- `jobTitle`: Job title
- `jobDescription`: The full description text

---

#### Step 2: Define Keyword-Based SOC Mapping
```python
landmark_rules = {
    "data entry": "4112",
    "data analytics": "2425",
    "data science": "3421"
}
```
**What this does:**
Specifies a fixed rule dictionary where specific substrings (case-insensitive) in the job description map to known SOC codes for:
- 4112: Data Entry Clerks
- 2425: Data Analysts
- 3421: Science/Tech Professionals (e.g., data scientists)

**Why this step is important:**
It creates a simulated analogue to "landmark occupations" used in proprietary datasets like BGT.

---

#### Step 3: Apply Rule-Based and Fallback SOC Assignment
```python
soc_codes = []
landmark_flags = []

for desc in df["jobDescription"]:
    matched = False
    if pd.isna(desc):
        desc = ""

    desc = desc.lower()
    for keyword, code in landmark_rules.items():
        if keyword in desc:
            soc_codes.append(code)
            landmark_flags.append(1)
            matched = True
            break

    if not matched:
        soc_codes.append(str(np.random.randint(1000, 9999)))
        landmark_flags.append(0)
```
**Explanation:**
- Each job description is converted to lowercase for keyword matching.
- If any keyword from `landmark_rules` is found, the respective SOC code is assigned and the landmark flag is set to 1.
- If no match is found — including cases where the description is empty or null — a **random** 4-digit SOC code between 1000 and 9999 is assigned, and the flag is set to 0.

**Note:** There is no hardcoded fallback like "9999" — all unmatched and empty descriptions receive a random SOC code. This mimics distributional noise found in uncontrolled real-world datasets.
**Explanation:**
- For each job description, check if any of the keywords exist (in lowercase form).
- If matched, assign the corresponding SOC code and mark it as a landmark match (1).
- If no keyword matches, assign a random 4-digit code to simulate a broader SOC space.
- If the description is missing, assign a dummy fallback code `"9999"`.

**Note:** This rule-based logic is simple but extendable. In production, a trained classifier or dictionary-based NLP tagging model would replace this.

---

#### Step 4: Attach SOC Codes and Save
```python
df["soc_code"] = soc_codes
df["landmark_flag"] = landmark_flags
df.to_csv("Data/enriched_with_soc.csv", index=False)
```
**Final output:** A modified dataset where each job advert now has:
- `soc_code`: Assigned based on rules or random fallback
- `landmark_flag`: 1 if keyword-matched, 0 if random

---

### Sample Output: `enriched_with_soc.csv`
| jobId | jobTitle         | jobDescription                         | soc_code | landmark_flag |
|--------|------------------|----------------------------------------|----------|----------------|
| 12345  | Data Analyst     | Use SQL and Python to analyse trends   | 2425     | 1              |
| 12346  | Office Assistant | Filing documents and entering records  | 4112     | 1              |
| 12347  | Admin Clerk      | General admin tasks and phone support  | 7254     | 0              |
| 12348  | Data Scientist   | Machine learning model development     | 3421     | 1              |

This enriched file is used as input for `bgt_gb_noun_chunks.py` in the next stage of the pipeline.



# File: `bgt_gb_noun_chunks.py`
**Purpose:**
This script extracts **noun chunks** from cleaned job descriptions and calculates their cosine similarity to the word "data" using SpaCy’s word vectors. It produces a semantic representation of how data-related each noun phrase is, laying the foundation for task classification and aggregation.

---

### Step-by-Step Breakdown

#### Step 1: Load Enriched Dataset
```python
df = pd.read_csv("/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/enriched_with_soc.csv")
df.dropna(subset=["jobDescription"], inplace=True)
```
**What it does:** Loads the enriched job advert dataset that contains synthetic SOC codes. Removes rows with missing descriptions to ensure text is available for NLP processing.

---

#### Step 2: Clean Descriptions by Removing Digits
```python
def remove_numbers(text):
    return ''.join(filter(lambda c: not c.isdigit(), str(text)))

df["clean_description"] = df["jobDescription"].apply(remove_numbers)
```
**Purpose:**
Numerical values like salaries, version numbers, etc., are removed because they don't contribute to semantic meaning in most NLP similarity tasks. This helps SpaCy better interpret linguistic structure.

---

#### Step 3: Load SpaCy Model and Define Comparison Token
```python
nlp = spacy.load("en_core_web_lg")
target_token = nlp("data")[0]
```
**Why this step is crucial:**
- `en_core_web_lg` includes GloVe word vectors, which are essential for semantic similarity tasks.
- The word "data" is transformed into a SpaCy token so that we can compute cosine similarity against every noun chunk.

---

#### Step 4: NLP Pipeline for All Descriptions
```python
docs = list(nlp.pipe(df["clean_description"], disable=["ner", "lemmatizer"]))
```
**What it does:**
Processes all job descriptions in a memory-efficient way using SpaCy’s `pipe()` generator.

**Disabled components:**
- Named Entity Recognition (NER) and lemmatizer are turned off to speed up processing since they are not needed for noun chunk and similarity analysis.

---

#### Step 5: Extract Noun Chunks and Compute Cosine Similarity
```python
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
```
**Detailed logic:**
- Loops over each SpaCy-parsed document.
- For each noun chunk, checks whether it has a vector (not all do — e.g., rare words).
- If so, computes its cosine similarity to the word "data".
- Stores relevant metadata like job ID, SOC code, and original text.

---

#### Step 6: Save Output to File
```python
result_df = pd.DataFrame(output)
result_df.to_csv("noun_chunks_with_similarity.csv", index=False)
```
**Result:**
A structured file containing every noun chunk across all descriptions and its semantic closeness to the concept of "data".

**Optional:** The script includes a commented line to save the same output in Parquet format for big-data contexts.

---

### Sample Output: `noun_chunks_with_similarity.csv`
| job_id | title           | noun_chunk     | similarity_to_data | soc_code | description                       | date       |
|--------|------------------|----------------|---------------------|----------|-----------------------------------|------------|
| 10001  | Data Analyst     | data report    | 0.84                | 2425     | Analyse SQL reports for insights | 2025-01-01 |
| 10001  | Data Analyst     | SQL statements | 0.79                | 2425     | Analyse SQL reports for insights | 2025-01-01 |
| 10002  | Office Admin     | input form     | 0.56                | 4112     | Maintain records and data entry  | 2025-01-02 |

---




## File: `job_classification.py`
**Purpose:**
Classify noun chunks extracted from job descriptions into three categories (data_entry, database, data_analytics), aggregate results at the job and SOC level, and export filtered intermediate datasets for further analysis.

---

### Step-by-Step Breakdown

#### Step 1: Load Input Data
```python
pd.read_csv("noun_chunks_with_similarity.csv")
```
**What it does:** Loads the noun chunks extracted from the previous SpaCy processing step. These chunks include their similarity scores to the word "data".

**Expected columns:**
- `job_id`: Unique identifier for the job advert
- `title`: Job title
- `noun_chunk`: Extracted noun phrase (e.g., "data entry", "SQL server")
- `similarity_to_data`: Cosine similarity to the word "data" (float 0–1)
- `soc_code`: 4-digit SOC occupation code (can be real or synthetic)
- `description`: Full job description
- `date`: Posting date

---

#### Step 2: Filter by Similarity Threshold
```python
SIMILARITY_THRESHOLD = 0.45
df = df[df['similarity_to_data'] >= SIMILARITY_THRESHOLD]
```
**Why this step?**
The goal is to remove irrelevant or generic chunks that don't semantically relate to "data". Based on empirical testing, 0.45 balances inclusion and specificity.

**What remains:**
Only those chunks like "data table", "Python script", "input form" that have meaningful relevance to data-related work.

---

#### Step 3: Classification Logic
```python
def chunk_tagger(chunk):
    chunk = chunk.lower()
    if any(w in chunk for w in ["typing", "form", "input", "record", "admin"]):
        return "data_entry"
    elif any(w in chunk for w in ["sql", "database", "oracle", "server", "data warehouse"]):
        return "database"
    elif any(w in chunk for w in ["analytics", "model", "analysis", "visualisation", "python", "machine learning"]):
        return "data_analytics"
    return "other"
```
**Why these tags?**
These categories are inspired by the methodology from the screenshot-based analysis, which groups tasks into functional types:
- **data_entry**: clerical tasks (typing, admin, record-keeping)
- **database**: storage and systems (SQL, server)
- **data_analytics**: interpretive/technical (Python, ML, analysis)

**Why use rule-based logic?**
We simulate BGTOcc-level tagging without having BGT landmark occupation IDs. The goal is to approximate task categories using keywords known to signal those types.

---

#### Step 4: Add Counter Column
```python
df["counter"] = 1
```
This temporary column is used to make it easy to sum or count values during groupings and pivoting operations.

---

#### Step 5: Aggregate to Job Level
```python
job_level = df.pivot_table(index="job_id", columns="Type", values="counter", aggfunc="sum", fill_value=0).reset_index()
```
**What it does:** Creates a wide-format table where each row = one job, and each column = count of a particular chunk type.

**Example Output:**
| job_id | data_entry | database | data_analytics |
|--------|------------|----------|----------------|
| 12345  | 2          | 1        | 3              |

---

#### Step 6: Filter Low-Activity Jobs
```python
job_level["Count_DataTerms"] = job_level[["data_entry", "database", "data_analytics"]].sum(axis=1)
job_level = job_level[job_level["Count_DataTerms"] > 2]
```
**Why this filter?**
To avoid over-interpreting job ads that mention data-related terms just once or twice in passing. This improves signal-to-noise.

---

#### Step 7: Merge Job-Level Data Back to Chunk-Level
```python
df = df[df["job_id"].isin(job_level["job_id"])]
df = df.merge(job_level, on="job_id", suffixes=("", "_job"))
```
Now, every noun chunk record has the overall counts for its job (for reference or further aggregation).

---

#### Step 8: Aggregate to SOC Level
```python
soc_agg = df.groupby("soc_code").agg({
    "data_entry": "sum",
    "database": "sum",
    "data_analytics": "sum",
    "job_id": "count"
}).reset_index()
soc_agg["data_intensity"] = soc_agg[["data_entry", "database", "data_analytics"]].sum(axis=1)
```
**What it produces:**
A per-SOC summary showing total data-related activity and number of jobs.

---

#### Step 9: Export Outputs
```python
df.to_csv("filtered_chunks.csv")
job_level.to_csv("job_level_aggregated.csv")
soc_agg.to_csv("soc_level_aggregated.csv")
```
These files form the core outputs of this processing stage and are used by the next scripts in the pipeline.

---

### Sample Outputs

#### `filtered_chunks.csv`
| job_id | noun_chunk   | Type           | similarity_to_data | soc_code |
|--------|--------------|----------------|---------------------|----------|
| 12345  | data report  | data_analytics | 0.76                | 2425     |
| 12345  | SQL table    | database       | 0.71                | 2425     |
| 12345  | input form   | data_entry     | 0.58                | 2425     |

#### `job_level_aggregated.csv`
| job_id | data_entry | database | data_analytics | Count_DataTerms |
|--------|------------|----------|----------------|------------------|
| 12345  | 1          | 1        | 1              | 3                |

#### `soc_level_aggregated.csv`
| soc_code | data_entry | database | data_analytics | job_id | data_intensity |
|----------|------------|----------|----------------|--------|----------------|
| 2425     | 150        | 100      | 200            | 50     | 450            |




# File: `sector_analysis_with_fake_mapping.py`
**Purpose:**
To simulate a sector-level view of data-related activity using SOC-level aggregate data. It randomly assigns sectors to SOC codes and generates dummy economic values (GVA and Investment) for analysis. This acts as a placeholder for a real SOC-to-sector concordance and real Supply and Use Table (SUT) data.

---

### Step-by-Step Breakdown

#### Step 1: Load SOC-Level Aggregated Data
```python
df_soc = pd.read_csv("soc_level_aggregated.csv")
```
**What it does:** Loads the SOC-level file generated from `job_classification.py`. This file contains the count of data_entry, database, and data_analytics tasks by SOC code.

**Expected columns:**
- `soc_code`
- `data_entry`, `database`, `data_analytics`
- `job_id`: number of jobs
- `data_intensity`: sum of the three types

---

#### Step 2: Generate Random SOC-to-Sector Mapping
```python
unique_soc_codes = df_soc["soc_code"].astype(str).unique()
sector_labels = ["Retail", "Health", "Admin", "Tech", "Legal", "Finance", "Transport", "IT", "Engineering"]
soc_to_sector = {soc: random.choice(sector_labels) for soc in unique_soc_codes}
df_map = pd.DataFrame(list(soc_to_sector.items()), columns=["soc_code", "sector"])
```
**Why this step?**
Since we do not yet have a real concordance from SOC codes to economic sectors, this randomly assigns each SOC code to one sector label. In production, this should be replaced with a proper lookup from ONS.

---

#### Step 3: Create Dummy GVA and Investment Data (Synthetic SUT)
```python
df_sut = pd.DataFrame(sector_labels, columns=["sector"])
df_sut["GVA"] = np.random.randint(300000000, 1000000000, size=len(df_sut))
df_sut["Investment"] = np.random.randint(10000000, 50000000, size=len(df_sut))
```
**What it does:**
Generates random GVA and Investment values for each sector.

**Why?**
In production, these values would be taken from the UK Supply and Use Tables (SUT) from the Office for National Statistics.

---

#### Step 4: Merge SOC-Level Data with Sectors
```python
df_merged = df_soc.merge(df_map, on="soc_code", how="left")
```
Links each SOC to a randomly assigned sector. Now each row has data intensity and sector association.

---

#### Step 5: Aggregate to Sector Level
```python
df_sector = df_merged.groupby("sector").agg({
    "data_entry": "sum",
    "database": "sum",
    "data_analytics": "sum"
}).reset_index()
df_sector["data_total"] = df_sector[["data_entry", "database", "data_analytics"]].sum(axis=1)
```
**What it does:**
Summarizes total counts of each type of data work per sector.

---

#### Step 6: Merge with GVA and Investment and Calculate Metrics
```python
df_sector = df_sector.merge(df_sut, on="sector", how="left")
df_sector["alpha"] = df_sector["data_total"] / df_sector["Investment"]
df_sector["share_of_GVA"] = df_sector["data_total"] / df_sector["GVA"]
```
**Alpha** measures data intensity per unit of investment in the sector.

**Share of GVA** indicates how much of a sector’s output is tied to data-related activity.

---

#### Step 7: Export Results
```python
df_sector.to_csv("sector_level_intensity.csv", index=False)
```
**This file is the final result** that will be visualized later. It contains sector-level summaries of data activity and economic metrics.

---

### Sample Output: `sector_level_intensity.csv`
| sector     | data_entry | database | data_analytics | data_total | GVA        | Investment | alpha        | share_of_GVA |
|------------|------------|----------|----------------|-------------|------------|------------|--------------|---------------|
| Tech       | 52         | 8        | 32             | 92          | 985126461  | 33647630   | 0.0027       | 0.000093      |
| Retail     | 56         | 0        | 67             | 123         | 942621108  | 25714555   | 0.0048       | 0.00013       |
| Health     | 41         | 18       | 21             | 80          | 428492780  | 43361172   | 0.0018       | 0.00019       |

This output is then passed to the `visualisation.py` script for rendering a multi-page PDF report.


# File: `visualisation.py`
**Purpose:**
This script creates a multi-page PDF report that visually summarizes sector-level data intensity metrics. It reads the output of `sector_analysis_with_fake_mapping.py`, generates three bar charts and a data table, and saves them into a formatted PDF.

---

### Step-by-Step Breakdown

#### Step 1: Setup File Paths and Directories
```python
output_dir = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Reports"
os.makedirs(output_dir, exist_ok=True)
data_path = "/Users/saurabhkumar/Desktop/UK_JOB_OECD/Data/sector_level_intensity.csv"
pdf_path = os.path.join(output_dir, "sector_level_report.pdf")
```
- Ensures the `Reports` folder exists.
- Defines input and output file paths.

---

#### Step 2: Load Sector Data
```python
df = pd.read_csv(data_path)
pdf = PdfPages(pdf_path)
```
- Reads the sector-level aggregated metrics (data_entry, database, data_analytics, GVA, investment, etc.).
- Initializes a `PdfPages` object to collect multiple figures.

---

#### Step 3: Plot Alpha by Sector
```python
df_sorted_alpha = df.sort_values("alpha", ascending=False)
plt.bar(df_sorted_alpha["sector"], df_sorted_alpha["alpha"], color='steelblue')
```
**Alpha** measures the ratio of data-related activity to total sector investment.

**Chart Details:**
- Bar height = `data_total / Investment`
- Sorted from highest to lowest alpha values.

---

#### Step 4: Plot Share of GVA by Sector
```python
df_sorted_gva = df.sort_values("share_of_GVA", ascending=False)
plt.bar(df_sorted_gva["sector"], df_sorted_gva["share_of_GVA"], color='seagreen')
```
**Share of GVA** shows the contribution of data activity to a sector’s economic output.

**Chart Details:**
- Y-axis = `data_total / GVA`
- Helps identify sectors most dependent on data tasks.

---

#### Step 5: Stacked Bar – Breakdown of Data Activities
```python
df.set_index("sector")[["data_entry", "database", "data_analytics"]].plot(..., stacked=True)
```
**What it shows:**
- Each sector’s composition of data work types.
- Reveals whether a sector is dominated by analytics, infrastructure, or entry-level data activity.

**Color Legend (tab20c):**
- Often used to distinguish multiple categories in stacked bars.

---

#### Step 6: Render Sector Summary Table
```python
ax.table(cellText=df.round(6).values, colLabels=df.columns, loc='center')
```
- Renders a complete table of all numeric metrics used in prior plots.
- Ensures numerical precision is visible (`round(6)`).

---

#### Step 7: Save the PDF
```python
pdf.close()
print(f"✅ PDF report generated and saved to:\n{pdf_path}")
```
**Final Output:**
`sector_level_report.pdf` saved to the Reports directory.

---

### Sample Pages in PDF Output

**Page 1:** Bar Chart – Alpha by Sector  
**Page 2:** Bar Chart – Share of GVA by Sector  
**Page 3:** Stacked Bar – Breakdown of Data Tasks  
**Page 4:** Tabular Summary – All Metrics by Sector



# Appendix: Understanding Synthetic Data Used in the Project (Layman's Terms)

This section explains the **synthetic (fake but realistic)** data used in this project and where you can get the real versions from government or official sources when scaling this to a production system.

---

## 1. SOC Codes (Occupation Codes)

**Synthetic Used:**
- We created SOC codes using simple rules based on keywords (e.g., "data entry" → `4112`).
- When no match was found, we randomly picked a 4-digit number between 1000–9999.

**Why?**
- Reed job adverts do not come with SOC codes.

**Official Source:**
- [ONS Standard Occupational Classification (SOC) 2020](https://www.ons.gov.uk/methodology/classificationsandstandards/standardoccupationalclassificationsoc)
- In production, SOC codes are often assigned using classifiers trained on labeled job data.

---

## 2. SOC to Sector Mapping

**Synthetic Used:**
- We assigned each SOC code a random sector label (e.g., "Retail", "Health") using a fixed list of common sectors.

**Why?**
- We didn’t have a SOC→Sector concordance table.

**Official Source:**
- UK SOC codes can be mapped to **Standard Industrial Classification (SIC)** codes using concordances.
- [ONS SOC → SIC Concordance](https://www.nomisweb.co.uk/)

---

## 3. Sector-Level Economic Metrics (GVA, Investment)

**Synthetic Used:**
- We generated random Gross Value Added (GVA) and investment values for each sector.
- GVA values were between £300 million and £1 billion.
- Investment values were between £10 million and £50 million.

**Why?**
- This mimicked real economic conditions for testing analysis without needing sensitive or restricted data.

**Official Source:**
- [UK National Accounts – Supply and Use Tables (SUT)](https://www.ons.gov.uk/economy/grossdomesticproductgdp/articles/usinginputoutputtounderstandtheukeconomy/2021-02-19)
- These contain sector-level breakdowns of GVA and capital investment.

---

## 4. Reed Job Adverts Dataset

**Synthetic Notes:**
- While this was scraped from a real API (Reed UK Jobs), the SOC code and economic metadata were not part of the API response and were synthetically generated.

**Where to Get Real Data:**
- Reed Jobs API (with a developer key)
- For richer datasets, refer to:
  - [Adzuna Job Data via ONS Open Geography Portal](https://www.ons.gov.uk/datasets/online-job-advert-estimates)
  - [Lightcast / BGT job data (licensed)](https://www.lightcast.io/)

---

## Summary Table
| Data Element           | Synthetic Source                     | Official Source / Replacement                                                                 |
|------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------|
| SOC codes              | Rule-based keyword mapping + random | ONS SOC 2020 classification, ML classification models                                         |
| SOC to Sector mapping | Random label assignment              | SOC → SIC concordance (ONS, Nomis)                                                            |
| GVA & Investment       | Randomized per sector                | UK National Accounts – Supply and Use Tables (ONS)                                            |
| Job Adverts            | Reed API + synthetic enrichments     | Reed, Adzuna, Lightcast/Burning Glass Technologies (licensed sources)                        |

---



## 3. Sector-Level Economic Metrics (GVA, Investment)

**What is GVA?**
- **GVA** stands for **Gross Value Added**. It tells us how much value a sector adds to the economy after subtracting the cost of inputs. It is like profit at the national level — the contribution of a specific industry to the total economy.

**What is Investment?**
- In this context, investment refers to **capital expenditure** made by each sector — money spent on things like buildings, machinery, software, etc.

**Synthetic Used:**
- We generated random values:
  - GVA between £300 million and £1 billion
  - Investment between £10 million and £50 million

**Why?**
- We needed these values to simulate real economic dynamics.

**Official Source:**
- [UK National Accounts – Supply and Use Tables (SUT)](https://www.ons.gov.uk/economy/grossdomesticproductgdp/articles/usinginputoutputtounderstandtheukeconomy/2021-02-19)

---

## 4. Alpha and Share of GVA – What They Really Mean

These are **indicators** we calculated to tell us how important data-related work is for each sector.

### Alpha
**Formula:**
```
alpha = data_total / Investment
```
- This shows how much data-related activity exists **for every £1 of investment** in the sector.
- **High alpha** = lots of data tasks with less money spent → more data-intensive per pound

**Real-world analogy:**
If Sector A does 100 units of data work with £1 million, but Sector B does 300 units with the same money, Sector B has a higher alpha — it is more data-productive.

### Share of GVA
**Formula:**
```
share_of_GVA = data_total / GVA
```
- This shows the **percentage of economic output** that relates to data work.
- **High share of GVA** = data is more central to the sector's economic value.

**Real-world analogy:**
If two sectors generate £1 billion each, but one has 200 data tasks and the other has 20, the first sector is clearly more data-driven.

---





# Appendix: Interpreting the Charts in the PDF Report

This section explains what each chart in the automatically generated PDF report means, how to read it, and how it helps interpret sector-level data intensity.

---

## Chart 1: Alpha by Sector
**Metric:** `alpha = data_total / investment`

**What it shows:**
- Sectors are sorted from highest to lowest in terms of data task efficiency per £1 of capital investment.
- A high alpha value means a sector performs a lot of data-related work relative to the amount it invests.

**Interpretation Tips:**
- Look for outliers at the top — these sectors may be digitally mature or labor-intensive.
- Low alpha doesn’t mean low tech; it may mean heavy capital (e.g., Transport).

**Use Case:**
- Identify where low-cost data transformation might be delivering high impact.

---

## Chart 2: Share of GVA by Sector
**Metric:** `share_of_GVA = data_total / GVA`

**What it shows:**
- The proportion of economic output in each sector that is attributed to data-related job tasks.

**Interpretation Tips:**
- A high share indicates that the sector is **data-dependent** in terms of value generation.
- Compare this with alpha — some sectors may have high output dependence but low investment efficiency.

**Use Case:**
- Helps frame arguments for where policy or investment support could amplify economic returns.

---

## Chart 3: Stacked Bar – Data Task Breakdown by Sector
**Metric:**
- Plots the number of chunks tagged as `data_entry`, `database`, and `data_analytics` per sector.

**What it shows:**
- The internal structure of how different sectors engage with data.
- Some sectors may be admin-heavy (more `data_entry`), while others focus on analytics or infrastructure.

**Interpretation Tips:**
- Use to compare the **complexity of data work** across sectors.
- Tech may lean toward `data_analytics`, Admin toward `data_entry`, etc.

**Use Case:**
- Design skilling or education programs tailored to dominant task types.

---

## Chart 4: Data Table – Full Sector Metrics
**What it shows:**
- The raw values used to generate all charts, rounded to 6 decimal places for precision.
- Useful for validation or exporting to other systems (e.g., dashboards).

---

These visual insights offer a multi-dimensional view of how UK job sectors engage with data-related work. They can be extended to support strategy, investment, and workforce planning discussions.

