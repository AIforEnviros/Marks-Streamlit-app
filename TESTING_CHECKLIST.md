# Jupyter Notebook Testing Checklist

## Status: ⏳ NOT YET TESTED

**Branch:** `feature/jupyter-notebook`
**File:** `analyte_analysis_notebook.ipynb`
**Created:** October 2025
**Last Updated:** October 2025

---

## ⚠️ IMPORTANT: Testing Required Before Merge

This Jupyter notebook has been created but **NOT YET TESTED** with real data.
Do not merge to main branch until all tests pass.

---

## Pre-Testing Setup

### Required Software
- [ ] Python 3.8 or newer installed
- [ ] Jupyter installed: `pip install jupyter`
- [ ] All dependencies installed: `pip install -r requirements.txt`

### Required Data
- [ ] Have `database.csv` file available
- [ ] CSV has required columns: Bore_ID, Date, Analyte, Value
- [ ] Date format is DD/MM/YYYY

---

## Testing Procedure

### Test 1: Environment Setup
- [ ] Open terminal/command prompt
- [ ] Navigate to project directory
- [ ] Run: `jupyter notebook`
- [ ] Jupyter opens in browser
- [ ] Open `analyte_analysis_notebook.ipynb`
- [ ] Notebook loads without errors

### Test 2: Section 1 - Import Libraries
- [ ] Run first code cell (imports)
- [ ] All libraries import successfully
- [ ] No "ModuleNotFoundError" errors
- [ ] Success message displays

### Test 3: Section 2 - Load Data
- [ ] Update `csv_file` variable to point to your CSV
- [ ] Run data loading cell
- [ ] Data loads without errors
- [ ] Summary statistics display correctly
- [ ] Date range looks correct
- [ ] Bore count matches expectations
- [ ] Analyte count matches expectations
- [ ] Preview cell shows first 10 rows correctly

### Test 4: Section 3 - Data Exploration
- [ ] Run analyte list cell
- [ ] All expected analytes appear
- [ ] Measurement counts look reasonable
- [ ] Run summary statistics cell
- [ ] Statistics display correctly

### Test 5: Section 4 - Plotting Function
- [ ] Run function definition cell
- [ ] No syntax errors
- [ ] Success message displays

### Test 6: Section 5 - Single Analyte Plot
- [ ] Update `selected_analyte` to a known analyte
- [ ] Run plot creation cell
- [ ] Plot displays correctly in notebook
- [ ] PNG file saves successfully
- [ ] Saved file can be opened
- [ ] Run logarithmic scale cell
- [ ] Log scale plot displays correctly

### Test 7: Section 6 - Batch Plot Generation
- [ ] Run batch processing cell
- [ ] Progress updates display correctly
- [ ] `analyte_plots/` folder is created
- [ ] All plots are generated (or appropriately skipped if no data)
- [ ] Success count matches expectations
- [ ] Run ZIP creation cell
- [ ] ZIP file is created
- [ ] ZIP file can be opened
- [ ] ZIP contains expected plots

### Test 8: Section 7 - Mann-Kendall Analysis
- [ ] Run function definition cell
- [ ] No syntax errors
- [ ] Run analysis cell
- [ ] Analysis completes without errors
- [ ] Results DataFrame displays
- [ ] Run significant trends filter cell
- [ ] Significant trends display correctly
- [ ] Run summary statistics cell
- [ ] Counts look reasonable
- [ ] Run analyte-specific filter cell
- [ ] Results filter correctly
- [ ] Run CSV export cell
- [ ] CSV file is created
- [ ] CSV can be opened in Excel

### Test 9: Section 8 - Advanced Customization
- [ ] Run Example 1 (custom date range)
- [ ] Plot displays with correct date range
- [ ] Run Example 2 (manual Y-axis)
- [ ] Plot displays with correct Y-axis limits
- [ ] Run Example 3 (consistent X-axis comparison)
- [ ] All plots use same X-axis range
- [ ] Run Example 4 (high-resolution plot)
- [ ] High-res PNG is created
- [ ] File size is larger than standard plot

### Test 10: End-to-End Workflow
- [ ] Restart kernel (Kernel → Restart & Clear Output)
- [ ] Run all cells from top to bottom (Cell → Run All)
- [ ] All cells execute without errors
- [ ] All expected outputs appear
- [ ] All files are created

---

## Results Verification

### Compare with Streamlit App
To verify the notebook produces identical results to the Streamlit app:

- [ ] Run same analyte in both tools
- [ ] Visual inspection: plots look identical
- [ ] Run Mann-Kendall on same data in both tools
- [ ] Compare results: trend, p-value, tau, slope should match
- [ ] Verify same data filtering behavior

---

## Common Issues to Check For

### Import Errors
- [ ] If pymannkendall fails: `pip install pymannkendall`
- [ ] If matplotlib fails: `pip install matplotlib`
- [ ] If pandas fails: `pip install pandas`

### Data Loading Errors
- [ ] Check CSV path is correct
- [ ] Verify CSV has correct columns
- [ ] Check date format (DD/MM/YYYY)
- [ ] Look for encoding issues (try encoding='utf-8' or 'latin-1')

### Plotting Errors
- [ ] If plots don't display: check `%matplotlib inline` ran
- [ ] If "no data" errors: verify analyte name spelling
- [ ] If date filtering issues: check pd.Timestamp() format

### Mann-Kendall Errors
- [ ] If "Insufficient data" is common: this is expected (need 3+ points)
- [ ] If all errors: check Value column is numeric
- [ ] If specific analyte fails: may have all NaN values

---

## Documentation to Update After Testing

If tests pass:
- [ ] Update this file: Change status to ✅ TESTED
- [ ] Update README.md: Add "tested and verified" note
- [ ] Update DUAL_APPROACH_PLAN.md: Mark notebook as complete
- [ ] Add any discovered issues to troubleshooting section

If tests fail:
- [ ] Document all errors encountered
- [ ] Fix issues in notebook
- [ ] Re-test
- [ ] Update this checklist with lessons learned

---

## Sign-Off

### Tester Information
- **Name:** _____________________
- **Date:** _____________________
- **Python Version:** _____________________
- **Jupyter Version:** _____________________

### Test Results
- **Pass/Fail:** _____________________
- **Notes:**
  ```



  ```

### Issues Found
```




```

### Ready to Merge?
- [ ] YES - All tests passed, notebook works correctly
- [ ] NO - Issues found, need fixes before merge

---

## Next Steps After Testing

### If Tests Pass:
1. Update status in this file to ✅ TESTED
2. Commit updated checklist
3. Merge `feature/jupyter-notebook` into main branch
4. Update deployment documentation
5. Share notebook with client

### If Tests Fail:
1. Document all issues in this file
2. Create GitHub issues for each problem
3. Fix issues
4. Re-run testing checklist
5. Do not merge until all tests pass

---

**REMEMBER:** Do not merge to main branch until this checklist is complete and all tests pass!
