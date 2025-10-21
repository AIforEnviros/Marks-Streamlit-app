# Dual Approach Plan: Streamlit App + Jupyter Notebook

## Context & Philosophy

**Client Profile:**
- Experienced hydrogeologist
- Not very experienced with Python
- Gets frustrated with setup/installation issues
- Wants to understand the code and learn
- Doesn't have much time
- Needs to do Mann-Kendall trend analysis routinely

**Root Issue:**
Client has cognitive dissonance between:
- What he thinks he should do (learn Python, understand code)
- What he actually needs (quick, reliable analysis tool)
- What he has time for (minimal technical debugging)

**Solution: Give Him Both Tools**

### Tool 1: Streamlit Web App (Production Tool)
**Status:** ✅ Already complete and production-ready
**Purpose:** For routine analysis work
**Benefits:**
- Zero installation for end user
- 2-minute workflow start to finish
- Interactive filtering (by analyte, significance, period, bore)
- Better insights than 400-page PDF reports
- No debugging required

### Tool 2: Jupyter Notebook (Learning/Development Tool)
**Status:** ⏳ To be created
**Purpose:** For when client wants to explore, understand, or modify methodology
**Benefits:**
- Fully functional - does everything the Streamlit app does
- Educational - explains methodology step-by-step
- Allows experimentation with parameters
- Satisfies desire to "understand the code"

---

## Current Status

### What's Already Done
1. **Streamlit app is complete** (`streamlit_app.py`)
   - Upload CSV → Analyze → Download results workflow
   - Interactive filtering (date ranges, Y-axis controls)
   - Mann-Kendall trend analysis
   - Batch plot generation
   - Multiple export options (PNG, ZIP, CSV)

2. **Deployment ready** (`deployment/streamlit-cloud` branch)
   - All code committed
   - `.gitignore` configured
   - Ready to push to GitHub and deploy

### What Needs to Be Done
Create a Jupyter notebook that:
- ✅ Does everything the Streamlit app does (full analysis workflow)
- ✅ Is educational with clear explanations and markdown documentation
- ✅ Allows client to learn by reading and running code step-by-step

---

## Implementation Plan for Jupyter Notebook

### File to Create
`analyte_analysis_notebook.ipynb`

### Notebook Structure

#### Section 1: Introduction
**Markdown cells:**
- Overview of what the notebook does
- When to use this vs. the Streamlit app
- Quick start instructions
- Required CSV format

**Content:**
```
# Analyte Time Series Analysis - Interactive Notebook

## When to Use This Notebook vs. the Streamlit App

**Use the Streamlit App when:**
- You want to do routine analysis quickly
- You just need the results
- You don't want to deal with code

**Use this Notebook when:**
- You want to understand how the analysis works
- You want to modify the methodology
- You want to learn Python
- You want to experiment with parameters

## What This Notebook Does
1. Load and validate analyte data from CSV
2. Create time series plots for all analytes
3. Perform Mann-Kendall trend analysis
4. Export results (plots and statistics)
```

#### Section 2: Setup & Data Loading
**Code cells:**
```python
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pymannkendall as mk
from pathlib import Path
import zipfile
from io import BytesIO

# Explanation: These are the Python packages we'll use
# - pandas: for working with tabular data (like Excel)
# - matplotlib: for creating plots
# - pymannkendall: for statistical trend analysis
```

**Code cells:**
```python
# Load the CSV file
# CHANGE THIS to point to your CSV file
csv_file = "database.csv"  # Update this path

df = pd.read_csv(csv_file)

# Clean and prepare the data
df.columns = df.columns.str.strip()  # Remove extra spaces from column names
df['Analyte'] = df['Analyte'].str.strip()  # Remove extra spaces from analyte names
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)  # Convert dates to proper format
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')  # Convert values to numbers

print(f"✓ Data loaded successfully!")
print(f"Total records: {len(df):,}")
```

**Markdown cells:**
- Explain what data cleaning does and why it's important
- Show expected CSV format

#### Section 3: Data Exploration
**Code cells:**
```python
# View basic information about your data
print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
print(f"Number of unique bores: {df['Bore_ID'].nunique()}")
print(f"Number of unique analytes: {df['Analyte'].nunique()}")

# View first few rows
df.head(10)
```

**Code cells:**
```python
# See all unique analytes in your dataset
analytes = sorted(df['Analyte'].unique())
print(f"Found {len(analytes)} analytes:")
for analyte in analytes:
    count = len(df[df['Analyte'] == analyte])
    print(f"  - {analyte}: {count} measurements")
```

**Markdown cells:**
- Explain importance of understanding your data first
- How to interpret the summary statistics

#### Section 4: Single Analyte Plotting
**Copy the `create_plot()` function from `streamlit_app.py`**

**Code cells:**
```python
def create_plot(df, analyte, figsize=(14, 7), dpi=150,
                date_min=None, date_max=None,
                y_scale='linear', y_min=None, y_max=None,
                force_x_limits=False):
    """
    Create a time series plot for a specific analyte.

    What this function does:
    1. Filters data to just the selected analyte
    2. Plots data for each bore hole separately (different colors)
    3. Formats the plot with labels, legend, and grid
    4. Applies any date range or Y-axis customizations

    Parameters:
    - analyte: Name of the analyte to plot (e.g., "Aluminium")
    - date_min/date_max: Optional date range filtering
    - y_scale: 'linear' or 'log' for Y-axis
    - y_min/y_max: Optional manual Y-axis limits
    """
    # [Include full function code from streamlit_app.py]
```

**Code cells:**
```python
# STEP 1: Choose which analyte to plot
# Change this to any analyte from the list above
selected_analyte = "Aluminium"  # CHANGE THIS

# STEP 2: Create the plot
fig = create_plot(df, selected_analyte,
                  figsize=(14, 7),
                  dpi=150,
                  y_scale='linear')  # Try 'log' for logarithmic scale

if fig is not None:
    plt.show()

    # STEP 3: Save the plot
    output_filename = f"{selected_analyte.replace(' ', '_')}.png"
    fig.savefig(output_filename, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved as: {output_filename}")
else:
    print(f"✗ No data available for {selected_analyte}")
```

**Markdown cells:**
- Explain what time series plots show
- How to interpret trends in the plots
- When to use log scale vs linear scale

#### Section 5: Batch Plot Generation
**Code cells:**
```python
# Generate plots for ALL analytes at once

# STEP 1: Choose settings
plot_width = 14
plot_height = 7
plot_dpi = 150
output_folder = "analyte_plots"

# Create output folder if it doesn't exist
Path(output_folder).mkdir(exist_ok=True)

# STEP 2: Loop through all analytes and create plots
print(f"Generating plots for {len(analytes)} analytes...")

for idx, analyte in enumerate(analytes, 1):
    print(f"  [{idx}/{len(analytes)}] Creating plot for: {analyte}")

    fig = create_plot(df, analyte,
                      figsize=(plot_width, plot_height),
                      dpi=plot_dpi)

    if fig is not None:
        # Create safe filename
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_'
                                for c in analyte)
        safe_filename = safe_filename.replace(' ', '_') + '.png'

        # Save plot
        output_path = Path(output_folder) / safe_filename
        fig.savefig(output_path, dpi=plot_dpi, bbox_inches='tight')
        plt.close(fig)

print(f"✓ All plots saved to: {output_folder}/")
```

**Markdown cells:**
- Explain the batch processing concept
- How to customize plot settings
- Where files are saved

#### Section 6: Mann-Kendall Trend Analysis
**Markdown cells:**
```
## Mann-Kendall Trend Analysis

### What is the Mann-Kendall Test?
The Mann-Kendall test is a statistical test used to detect monotonic trends in time series data.

**What it tells you:**
- Is there a statistically significant increasing or decreasing trend?
- How strong is the trend? (Kendall's Tau coefficient)
- What is the rate of change? (Slope)

**Key concepts:**
- **P-value**: If p < 0.05, the trend is statistically significant
- **Tau**: Measures correlation (-1 to +1). Closer to ±1 = stronger trend
- **Trend**: "increasing", "decreasing", or "no trend"
- **Slope**: Rate of change per time unit

### When is this useful?
- Detecting contamination trends in groundwater
- Identifying improvements after remediation
- Regulatory compliance (demonstrating trends)
```

**Copy the `perform_mann_kendall_analysis()` function**

**Code cells:**
```python
def perform_mann_kendall_analysis(df, date_min=None, date_max=None):
    """
    Perform Mann-Kendall trend analysis for each analyte and bore.

    What this does:
    1. Groups data by analyte and bore
    2. Runs Mann-Kendall test on each group
    3. Returns a table with trend results

    Requirements:
    - At least 3 data points needed per bore-analyte combination
    - No trend analysis on insufficient data
    """
    # [Include full function code from streamlit_app.py]
```

**Code cells:**
```python
# STEP 1: Run the Mann-Kendall analysis
print("Running Mann-Kendall trend analysis...")

# Optional: Set date range for analysis
date_min = None  # Set to pd.Timestamp('2020-01-01') to filter
date_max = None  # Set to pd.Timestamp('2023-12-31') to filter

mk_results = perform_mann_kendall_analysis(df, date_min, date_max)

print(f"✓ Analysis complete! Analyzed {len(mk_results)} bore-analyte combinations")

# STEP 2: View all results
mk_results
```

**Code cells:**
```python
# STEP 3: Filter results to show only significant trends
significant_trends = mk_results[mk_results['Significant'] == 'Yes']

print(f"Found {len(significant_trends)} significant trends (p < 0.05)")
print(f"  - Increasing: {len(significant_trends[significant_trends['Trend'] == 'increasing'])}")
print(f"  - Decreasing: {len(significant_trends[significant_trends['Trend'] == 'decreasing'])}")

# Display significant trends
significant_trends.sort_values('P-value')
```

**Code cells:**
```python
# STEP 4: Filter by specific analyte (optional)
analyte_to_examine = "Aluminium"  # CHANGE THIS

analyte_results = mk_results[mk_results['Analyte'] == analyte_to_examine]
print(f"\nMann-Kendall results for {analyte_to_examine}:")
analyte_results.sort_values('P-value')
```

**Code cells:**
```python
# STEP 5: Export results to CSV
output_csv = f"mann_kendall_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
mk_results.to_csv(output_csv, index=False)
print(f"✓ Results saved to: {output_csv}")
```

**Markdown cells:**
- How to interpret the results
- What different trend types mean
- When to investigate further

#### Section 7: Advanced Customization
**Code cells:**
```python
# Example: Create plots with custom date range and Y-axis settings

# Choose analyte
analyte = "Arsenic"

# Custom settings
custom_date_min = pd.Timestamp('2018-01-01')
custom_date_max = pd.Timestamp('2023-12-31')
custom_y_scale = 'log'  # or 'linear'
custom_y_min = 0.001
custom_y_max = 1.0

# Create custom plot
fig = create_plot(df, analyte,
                  figsize=(14, 7),
                  dpi=150,
                  date_min=custom_date_min,
                  date_max=custom_date_max,
                  y_scale=custom_y_scale,
                  y_min=custom_y_min,
                  y_max=custom_y_max)

if fig:
    plt.show()
```

**Markdown cells:**
- Explain all customization options
- When to use different settings
- How to experiment safely

#### Section 8: Summary & Next Steps
**Markdown cells:**
```
## Summary

You've learned how to:
- ✅ Load and validate analyte data
- ✅ Explore your dataset
- ✅ Create time series plots (single and batch)
- ✅ Perform Mann-Kendall trend analysis
- ✅ Filter and export results
- ✅ Customize plots for specific needs

## When to Use Which Tool

**Use the Streamlit App** (recommended for routine work):
- Quick analysis needed
- No code interaction wanted
- Sharing results with others
- Working from different devices

**Use this Notebook** (for learning/exploration):
- Understanding the methodology
- Experimenting with parameters
- Modifying the analysis approach
- Learning Python

## Resources for Learning More

**Python & Pandas:**
- [Python for Data Analysis](https://wesmckinney.com/book/)
- [Pandas documentation](https://pandas.pydata.org/docs/)

**Mann-Kendall Test:**
- [pymannkendall documentation](https://pypi.org/project/pymannkendall/)
- [Mann-Kendall test explained](https://en.wikipedia.org/wiki/Mann%E2%80%93Kendall_test)

**Matplotlib (plotting):**
- [Matplotlib tutorials](https://matplotlib.org/stable/tutorials/index.html)
```

---

## Implementation Steps

### When You're Ready to Build This:

1. **Create the notebook file**
   - File: `analyte_analysis_notebook.ipynb`
   - Location: Same directory as `streamlit_app.py`

2. **Structure approach**
   - Copy functions from `streamlit_app.py` (reuse code)
   - Add extensive markdown documentation
   - Include example code cells with clear instructions
   - Add "CHANGE THIS" comments where user needs to modify

3. **Key features to include**
   - All functionality from Streamlit app
   - Educational markdown cells explaining methodology
   - Step-by-step workflow (can run cell-by-cell)
   - Clear comments in code
   - Example outputs where helpful

4. **Test the notebook**
   - Run all cells from top to bottom
   - Verify produces same results as Streamlit app
   - Check all explanations are clear
   - Ensure "CHANGE THIS" markers are obvious

5. **Documentation**
   - Add usage instructions to README
   - Explain when to use notebook vs. app
   - Include installation requirements (same `requirements.txt`)

---

## Benefits of This Approach

### For the Client
✅ **Zero friction for routine work** - Just use the web app
✅ **Learning resource available** - Notebook when he wants to understand
✅ **No forced learning** - Can use app without ever touching code
✅ **Gradual learning curve** - Can explore notebook at his own pace
✅ **Same results both ways** - Confidence that methods are consistent

### For You (Developer)
✅ **Reduced support burden** - Client has self-service learning tool
✅ **Code reuse** - Notebook uses same functions as app
✅ **Single maintenance path** - Updates to functions help both tools
✅ **Client satisfaction** - Addresses his desire to learn without forcing it

---

## Timeline Estimate

| Task | Time Estimate |
|------|---------------|
| Create notebook structure | 30 minutes |
| Copy & adapt functions from streamlit_app.py | 30 minutes |
| Write educational markdown cells | 1-2 hours |
| Add example code cells | 1 hour |
| Test end-to-end workflow | 30 minutes |
| Write usage documentation | 30 minutes |
| **Total** | **4-5 hours** |

---

## Next Session Checklist

When you pick this up tomorrow:

- [ ] Create `analyte_analysis_notebook.ipynb`
- [ ] Follow the 8-section structure outlined above
- [ ] Reuse functions from `streamlit_app.py`
- [ ] Add extensive markdown documentation
- [ ] Include clear "CHANGE THIS" markers
- [ ] Test with actual data
- [ ] Update README with notebook usage instructions

---

## Files Involved

**Will create:**
- `analyte_analysis_notebook.ipynb` (new Jupyter notebook)

**Will reference/reuse:**
- `streamlit_app.py` (copy functions from here)
- `requirements.txt` (same dependencies work for both)

**May update:**
- `STREAMLIT_README.md` (add section about notebook)

---

## Questions to Consider

Before building, think about:

1. **Jupyter installation**: Does client have Jupyter installed?
   - If not, add installation instructions
   - Consider VS Code with Jupyter extension as alternative

2. **Data file location**: Should notebook expect:
   - `database.csv` in same folder?
   - User provides path?
   - Both options with examples?

3. **Output organization**: Where should plots/results save?
   - Same folder as notebook?
   - Separate `outputs/` folder?
   - User-specified location?

---

**Status:** Ready to implement
**Priority:** When client requests learning tool or expresses interest in code
**Estimated effort:** 4-5 hours
**Dependencies:** None (Streamlit app already complete)
