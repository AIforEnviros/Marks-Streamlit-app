# Analyte Analysis Jupyter Notebook - Getting Started

Welcome! This guide will help you set up and use the Analyte Analysis Jupyter Notebook for analyzing groundwater monitoring data.

---

## Quick Start (3 Steps)

1. **Install dependencies**: Open a terminal and run `pip install -r requirements.txt`
2. **Launch Jupyter**: Run `python -m notebook`
3. **Open the notebook**: Click on `analyte_analysis_notebook.ipynb` in your browser

---

## What's Included

- **analyte_analysis_notebook.ipynb** - The main analysis notebook
- **requirements.txt** - Required Python packages
- **sample_data.csv** - Example data showing the expected CSV format
- **GETTING_STARTED.md** - This file

---

## Detailed Setup Instructions

### Step 1: Verify Python is Installed

Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and check your Python version:

```bash
python --version
```

You should see Python 3.8 or higher. If not, you may need to use `python3` instead of `python`.

### Step 2: Install Required Packages

Navigate to the folder containing these files, then run:

```bash
pip install -r requirements.txt
```

This will install:
- **jupyter** - For running notebooks
- **pandas** - For data manipulation
- **matplotlib** - For creating plots
- **pymannkendall** - For trend analysis

**Note:** Installation may take a few minutes.

### Step 3: Launch Jupyter Notebook

Run this command:

```bash
python -m notebook
```

**What happens:**
- A web browser window will open automatically
- You'll see a file browser showing the files in this folder
- If a browser doesn't open, look for a URL in the terminal (starts with `http://localhost:8888/...`) and copy it into your browser

### Step 4: Open the Notebook

In the browser file listing, click on:

```
analyte_analysis_notebook.ipynb
```

The notebook will open in a new tab.

---

## How to Use the Notebook

### Understanding the Notebook Structure

The notebook is divided into **9 sections**:

1. **Import Libraries** - Sets up the required tools
2. **Load Data** - Reads your CSV file
3. **Explore Data** - Shows what's in your dataset
4. **Define Plotting Function** - The core plotting code
5. **Single Analyte Plots** - Create individual plots
6. **Batch Plot Generation** - Create all plots at once
7. **Mann-Kendall Analysis** - Statistical trend detection
8. **Advanced Customization** - Date ranges, Y-axis controls, font sizes
9. **Summary** - Next steps and resources

### Running the Notebook

**To run all cells at once:**
1. Click `Kernel` → `Restart & Run All`
2. Wait for all cells to execute (watch for the `[*]` to change to numbers)

**To run cells one at a time:**
1. Click on a cell (it will be highlighted)
2. Press `Shift + Enter` to run it and move to the next cell
3. Or press `Ctrl + Enter` (Windows) / `Cmd + Enter` (Mac) to run and stay on the same cell

### Using Your Own Data

#### CSV File Format

Your CSV file must have these **4 columns** (exact names):

| Column | Description | Example |
|--------|-------------|---------|
| **Bore_ID** | Bore hole identifier | LCLBOR01 |
| **Date** | Measurement date | 25/07/2016 |
| **Analyte** | Analyte name | Aluminium |
| **Value** | Numeric measurement | 12.0 |

**Important:**
- Date format must be **DD/MM/YYYY** (day/month/year)
- Column names are case-sensitive
- See `sample_data.csv` for an example

#### Loading Your Data

1. **Place your CSV file** in the same folder as this notebook
2. **Open the notebook** and find **Section 2** (Cell 4)
3. **Update the filename**:

   ```python
   csv_file = "database.csv"  # Change to your filename
   ```

4. **Run the cell** (Shift + Enter)

If you see errors, check:
- File name is spelled correctly
- File is in the same folder as the notebook
- CSV has the required columns

### Creating Plots

#### Single Analyte Plot

1. Go to **Section 5** (Cell 13)
2. Change the analyte name:
   ```python
   selected_analyte = "Aluminium"  # Change this
   ```
3. Run the cell (Shift + Enter)
4. The plot will appear below the cell and save as a PNG file

#### All Analytes at Once

1. Go to **Section 6** (Cell 17)
2. Run the cell (Shift + Enter)
3. Plots will be created for all analytes and saved in `analyte_plots/` folder

### Running Trend Analysis

1. Go to **Section 7** (Cell 23)
2. Run the cell to analyze all data
3. Results will show:
   - **Trend**: increasing, decreasing, or no trend
   - **P-value**: Statistical significance (< 0.05 is significant)
   - **Tau**: Strength of trend (-1 to +1)
   - **Slope**: Rate of change

### Customizing Plots

**Change date range:**
```python
fig = create_plot(df, "Aluminium",
                  date_min=pd.Timestamp('2018-01-01'),
                  date_max=pd.Timestamp('2023-12-31'))
```

**Use logarithmic scale:**
```python
fig = create_plot(df, "Aluminium", y_scale='log')
```

**Change font sizes:**
```python
fig = create_plot(df, "Aluminium",
                  title_fontsize=18,      # Title
                  axis_label_fontsize=16, # Axis labels
                  tick_fontsize=14,       # Tick numbers
                  legend_fontsize=11)     # Legend
```

See **Section 8** in the notebook for more examples.

---

## Troubleshooting

### "Command 'jupyter' not found"

**Solution:** Use `python -m notebook` instead of `jupyter notebook`

### "ModuleNotFoundError: No module named 'pandas'"

**Solution:** Install requirements again:
```bash
pip install -r requirements.txt
```

If that doesn't work, try:
```bash
pip install --user -r requirements.txt
```

### "FileNotFoundError: database.csv"

**Solution:**
- Check that your CSV file is in the same folder as the notebook
- Update the filename in Cell 4 to match your file exactly
- Use the full path: `csv_file = "C:/path/to/your/data.csv"`

### "No data available for [analyte name]"

**Solution:**
- Check spelling (names are case-sensitive)
- Run Section 3 (Cell 8) to see all available analyte names
- Copy the exact name from that list

### Cells won't run / kernel is dead

**Solution:**
1. Click `Kernel` → `Restart Kernel`
2. When prompted, click `Restart`
3. Run cells again from the top

### Plots don't appear

**Solution:**
- Make sure you ran Cell 2 (imports) first
- Check if there's actually data for that analyte
- Try restarting the kernel and running all cells again

### "Invalid Date" or date parsing errors

**Solution:**
- Dates must be in DD/MM/YYYY format (25/07/2016)
- Check your CSV file has dates in the correct format
- Excel sometimes changes date formats - open in a text editor to verify

---

## Tips for Best Results

### For Print Output (Reports)
The notebook uses **Print preset by default** - fonts are optimized for printing 2 plots per A4 page side-by-side. No changes needed.

### For Digital Viewing (Presentations)
Use the **Screen preset** for smaller fonts better suited to slides or web viewing. See Section 8, Example 5.

### Saving Your Work
- Jupyter **auto-saves** every few minutes
- To manually save: Click the save icon or press `Ctrl+S` (Windows) / `Cmd+S` (Mac)
- All your changes are saved in the `.ipynb` file

### Exporting Results
- **Plots**: Automatically saved as PNG files in the same folder or `analyte_plots/`
- **Statistics**: Trend analysis results exported as CSV files
- **ZIP all plots**: See Section 6, Cell 19

---

## Next Steps

1. **Try the sample data** - Run the notebook with `sample_data.csv` first
2. **Load your own data** - Update Cell 4 with your filename
3. **Explore the analysis** - Run through all sections to see what's available
4. **Read the notebook** - The markdown cells explain what each section does
5. **Experiment** - Try different parameters and see what happens

**Remember:** You can always restart the kernel and start fresh if something goes wrong. You can't break anything!

---

## Getting Help

If you're stuck:

1. **Read error messages carefully** - They often tell you what's wrong
2. **Check the Troubleshooting section** above
3. **Look at the notebook explanations** - Each cell has comments explaining what it does
4. **Consult the Summary section** (Section 9 in the notebook) - Includes common customizations and learning resources

---

## About This Notebook

This notebook performs the same analysis as the Streamlit web app, but with:
- **Full code visibility** - See exactly what's happening
- **Step-by-step workflow** - Run and understand each part
- **Complete customization** - Modify anything you want
- **Educational explanations** - Learn Python and data analysis

**Use the Streamlit app for quick routine analysis. Use this notebook when you want to learn, understand, or customize.**

---

Good luck with your analysis!
