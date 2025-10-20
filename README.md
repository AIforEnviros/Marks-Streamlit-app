# Analyte Time Series Analysis Tools

**Two powerful tools for groundwater analyte analysis - choose the one that fits your needs!**

---

## Quick Start: Which Tool Should I Use?

### Use the Streamlit Web App for:
- Quick, routine analysis (2-minute workflow)
- No code interaction
- Monthly reporting
- Sharing with colleagues
- Working from anywhere

### Use the Jupyter Notebook for:
- Understanding the methodology
- Learning Python
- Custom analysis
- Experimenting with parameters
- Educational purposes

**Both tools produce identical results using the same analysis code!**

---

## Tool #1: Streamlit Web App (Production Tool)

### Features
- Beautiful web interface
- Upload CSV → Generate plots → Download results
- Interactive filtering (date ranges, analytes, bores)
- Mann-Kendall trend analysis
- Batch plot generation (all analytes at once)
- Export options (PNG, ZIP, CSV)

### Installation

```bash
pip install streamlit pandas matplotlib pymannkendall
```

### Usage

```bash
streamlit run streamlit_app.py
```

Your browser will automatically open to `http://localhost:8501`

### Workflow
1. Upload your CSV file
2. Review data summary
3. Select single analyte or batch generate all
4. Apply filters (date range, Y-axis controls)
5. Run trend analysis if needed
6. Download results

**Time: ~2-5 minutes for complete analysis**

### See Full Documentation
For detailed Streamlit app instructions, see: [STREAMLIT_README.md](STREAMLIT_README.md)

---

## Tool #2: Jupyter Notebook (Learning Tool)

### Features
- Full code visibility
- Step-by-step educational workflow
- Extensive explanations of methodology
- Customizable parameters
- Same analysis as Streamlit app
- Perfect for learning Python

### Installation

**Option 1: Using pip**
```bash
pip install jupyter pandas matplotlib pymannkendall
```

**Option 2: Using Anaconda (recommended)**
```bash
conda install jupyter pandas matplotlib
pip install pymannkendall
```

### Usage

**Launch Jupyter:**
```bash
jupyter notebook
```

**Or using VS Code:**
1. Install Python extension
2. Open `analyte_analysis_notebook.ipynb`
3. Click "Run All" or run cells individually

### Notebook Structure

The notebook includes 9 comprehensive sections:

1. **Introduction** - When to use notebook vs. app
2. **Import Libraries** - Setting up your environment
3. **Load & Prepare Data** - Reading and cleaning CSV
4. **Data Exploration** - Understanding your dataset
5. **Define Plotting Function** - Core plotting code explained
6. **Single Analyte Plots** - Create individual plots
7. **Batch Plot Generation** - Generate all plots at once
8. **Mann-Kendall Analysis** - Statistical trend detection
9. **Advanced Customization** - Custom date ranges, Y-axis, etc.
10. **Summary & Resources** - Next steps and learning resources

### Getting Started with the Notebook

1. **Open the notebook**: `analyte_analysis_notebook.ipynb`
2. **Read the markdown cells** for explanations
3. **Look for "CHANGE THIS"** comments where you need to modify values
4. **Run cells in order** from top to bottom (Shift+Enter)
5. **Experiment!** Try different parameters

**Key customizations to make:**
- Cell in Section 2: Update `csv_file` variable to point to your CSV
- Cell in Section 5: Change `selected_analyte` to plot different analytes
- Throughout: Modify parameters to customize analysis

### What You'll Learn

- How to load and clean data with pandas
- How to create professional plots with matplotlib
- How Mann-Kendall trend analysis works
- How to interpret statistical results
- Python basics (functions, loops, data structures)
- Data exploration techniques

**No previous Python experience required!**

---

## Installation Requirements

Both tools require the same Python packages:

### Using pip:
```bash
pip install pandas matplotlib pymannkendall
```

### For Streamlit app also install:
```bash
pip install streamlit
```

### For Jupyter notebook also install:
```bash
pip install jupyter
```

### Or install everything at once:
```bash
pip install streamlit jupyter pandas matplotlib pymannkendall
```

### Requirements file:
A `requirements.txt` file is included. Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## CSV Data Format

Both tools expect the same CSV format:

| Column | Description | Example |
|--------|-------------|---------|
| **Bore_ID** | Bore hole identifier | LCLBOR01 |
| **Date** | Measurement date | 25/07/2016 |
| **Analyte** | Analyte name | Aluminium |
| **Value** | Numeric measurement | 12.0 |

**Notes:**
- Date format: DD/MM/YYYY
- Column names are case-sensitive
- Extra spaces in names will be automatically cleaned

---

## Features Comparison

| Feature | Streamlit App | Jupyter Notebook |
|---------|---------------|------------------|
| **Time series plots** | ✅ | ✅ |
| **Batch plot generation** | ✅ | ✅ |
| **Mann-Kendall analysis** | ✅ | ✅ |
| **Date filtering** | ✅ | ✅ |
| **Y-axis controls** | ✅ | ✅ |
| **Export plots (PNG/ZIP)** | ✅ | ✅ |
| **Export statistics (CSV)** | ✅ | ✅ |
| **Interactive filtering** | ✅ | ❌ |
| **Web interface** | ✅ | ❌ |
| **Code visibility** | ❌ | ✅ |
| **Educational explanations** | ❌ | ✅ |
| **Full customization** | ❌ | ✅ |
| **No coding required** | ✅ | ❌ |
| **Learning resource** | ❌ | ✅ |

---

## Mann-Kendall Trend Analysis

Both tools perform the same statistical trend analysis:

### What it does:
- Detects monotonic trends (increasing/decreasing) in time series data
- Non-parametric test (no distribution assumptions)
- Robust to outliers
- Separate analysis for each bore-analyte combination

### Results include:
- **Trend**: increasing, decreasing, or no trend
- **P-value**: Statistical significance (p < 0.05 = significant)
- **Tau**: Strength of correlation (-1 to +1)
- **Slope**: Rate of change per time unit
- **Significance**: Yes/No indicator

### Applications:
- Detecting contamination trends
- Confirming remediation effectiveness
- Regulatory compliance reporting
- Early warning system

---

## Example Workflows

### Routine Monthly Reporting (Use Streamlit App)
1. Launch: `streamlit run streamlit_app.py`
2. Upload latest CSV
3. Batch download all plots
4. Run trend analysis
5. Download results
6. Insert into report

**Time: ~5 minutes**

### Learning the Methodology (Use Jupyter Notebook)
1. Launch: `jupyter notebook`
2. Open `analyte_analysis_notebook.ipynb`
3. Read through explanations
4. Run cells step-by-step
5. Experiment with parameters
6. Understand the analysis

**Time: 1-2 hours to read through; 10-15 minutes to run**

### Custom Analysis (Use Jupyter Notebook)
1. Open notebook
2. Modify plotting function for specific needs
3. Add custom filtering logic
4. Create specialized visualizations
5. Export custom results

**Time: Varies based on customization**

---

## File Structure

```
📁 Marks-Streamlit-app/
├── streamlit_app.py                    # Streamlit web app
├── analyte_analysis_notebook.ipynb     # Jupyter notebook (educational)
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── STREAMLIT_README.md                 # Detailed Streamlit guide
├── DUAL_APPROACH_PLAN.md              # Development plan document
├── database.csv                        # Your data (not tracked in git)
└── .gitignore                         # Git ignore rules
```

---

## Troubleshooting

### "Module not found" errors
**Solution:** Install missing packages
```bash
pip install streamlit jupyter pandas matplotlib pymannkendall
```

### Jupyter notebook won't open
**Solution:** Check Jupyter is installed
```bash
pip install jupyter
jupyter notebook
```

### Streamlit port already in use
**Solution:** Use different port
```bash
streamlit run streamlit_app.py --server.port 8502
```

### CSV loading errors
**Solution:**
- Verify CSV has required columns: Bore_ID, Date, Analyte, Value
- Check date format is DD/MM/YYYY
- Ensure no missing column headers

### No data for analyte
**Solution:**
- Check analyte name spelling (case-sensitive)
- Verify analyte exists in dataset
- Check date filters aren't excluding all data

---

## Learning Resources

### Python & Data Analysis
- [Python for Data Analysis](https://wesmckinney.com/book/) - Comprehensive guide
- [Pandas Documentation](https://pandas.pydata.org/docs/) - Official docs
- [Real Python](https://realpython.com/) - Excellent tutorials

### Statistical Methods
- [Mann-Kendall Test](https://en.wikipedia.org/wiki/Mann%E2%80%93Kendall_test) - Wikipedia
- [pymannkendall Docs](https://pypi.org/project/pymannkendall/) - Library documentation
- [USGS Statistical Methods](https://www.usgs.gov/mission-areas/water-resources/science/statistical-methods)

### Visualization
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Python Graph Gallery](https://python-graph-gallery.com/)

### Jupyter Notebooks
- [Jupyter Documentation](https://jupyter-notebook.readthedocs.io/)
- [Jupyter Shortcuts](https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330)

---

## Version History

### v2.0 (Current) - Dual Tool Approach
- ✅ Streamlit web app (production-ready)
- ✅ Jupyter notebook (educational tool)
- ✅ Mann-Kendall trend analysis
- ✅ Date filtering and Y-axis controls
- ✅ Consistent X-axis option for plot comparison
- ✅ Batch plot generation with preview
- ✅ Comprehensive documentation

### v1.0 - Initial Streamlit App
- ✅ Basic plotting functionality
- ✅ Single analyte and batch modes
- ✅ CSV upload and data preview

---

## Deployment

### Streamlit Cloud (Free Hosting)
The Streamlit app can be deployed to Streamlit Cloud for web access:

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

**Benefits:**
- No installation for users
- Access from anywhere
- Automatic updates when you push changes
- Free for public repositories

### See Also
- [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md) - Deployment instructions

---

## Development

### Architecture
Both tools share the same core analysis functions:
- `create_plot()` - Time series plotting
- `perform_mann_kendall_analysis()` - Trend analysis

This ensures identical results between Streamlit app and Jupyter notebook.

### Code Reuse Philosophy
- Don't Repeat Yourself (DRY)
- Single source of truth for analysis logic
- Separate presentation (Streamlit/Jupyter) from logic (functions)

### See Also
- [DUAL_APPROACH_PLAN.md](DUAL_APPROACH_PLAN.md) - Design philosophy

---

## Support

### Getting Help
1. **Read the docs** - Check this README and STREAMLIT_README.md
2. **Try the notebook** - Educational explanations may answer questions
3. **Check troubleshooting** - Common issues listed above

### Common Questions

**Q: Do I need both tools?**
A: No! Choose based on your needs. Most users will only need the Streamlit app.

**Q: Will the results be the same?**
A: Yes! Both use identical analysis code.

**Q: Can I modify the code?**
A: Absolutely! The Jupyter notebook is perfect for learning and customization.

**Q: Which Python version?**
A: Python 3.8 or newer recommended.

**Q: Is this production-ready?**
A: Yes! The Streamlit app is deployed and being used in production.

---

## License

This project is created for Mark's hydrogeological analysis work.

---

## Quick Reference

### Streamlit App
```bash
# Install
pip install streamlit pandas matplotlib pymannkendall

# Run
streamlit run streamlit_app.py

# Stop
Ctrl+C in terminal
```

### Jupyter Notebook
```bash
# Install
pip install jupyter pandas matplotlib pymannkendall

# Run
jupyter notebook

# Open
analyte_analysis_notebook.ipynb
```

### Both Tools
```bash
# Install everything
pip install -r requirements.txt
```

---

## Summary

You now have **two powerful tools** for analyte analysis:

1. **Streamlit App** - Fast, reliable, production tool
2. **Jupyter Notebook** - Educational, customizable learning tool

**Choose the tool that fits your current need:**
- Need results quickly? → Streamlit
- Want to learn how it works? → Jupyter
- Need custom analysis? → Jupyter
- Sharing with others? → Streamlit

**Both produce identical, reliable results!**

---

Happy analyzing! 📊🌊🔬
