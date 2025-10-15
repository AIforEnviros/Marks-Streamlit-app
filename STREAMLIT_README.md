# Streamlit Analyte Plotter - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Streamlit (One-Time Setup)
Open your terminal/command prompt and run:
```bash
pip install streamlit pandas matplotlib
```

**That's it!** Everything you need is now installed.

---

### Step 2: Run the App
Navigate to the folder containing this file and run:
```bash
streamlit run streamlit_app.py
```

Your browser will automatically open with the app running!

---

### Step 3: Use the App
1. **Upload** your database.csv file using the sidebar
2. **Explore** individual analytes or batch download all plots
3. **Download** plots as PNG files or as a complete ZIP

---

## 📊 What This App Does

### Single Analyte Mode
- Select any analyte from the dropdown
- Click "Generate Plot" to view
- Click "Download Plot as PNG" to save
- Customize plot settings in sidebar

### Batch Download Mode
- Click "Generate All Plots" button
- Wait 2-3 minutes while it creates all 80 plots
- Download complete ZIP file with all plots
- Perfect for monthly reports!

### Data Preview Mode
- View raw data in table format
- Filter by bore or analyte
- Download filtered data as CSV

---

## ⚙️ Customization Options

All available in the sidebar:

### Plot Settings
- **Plot Width:** 8-20 inches
- **Plot Height:** 4-12 inches  
- **Plot Quality (DPI):** 100-300 (higher = better quality)

Recommended: 14" wide, 7" tall, 150 DPI

---

## 💡 Pro Tips

### Tip 1: Keep Terminal Open
Don't close the terminal window - that's what's running the app. When you're done, press Ctrl+C in the terminal to stop it.

### Tip 2: Refresh After Upload
If you upload a new CSV, the app automatically refreshes.

### Tip 3: Batch Download is the Killer Feature
Instead of manually saving 80 plots, just click "Generate All Plots" and get everything in one ZIP file. This is why Streamlit is the best solution!

### Tip 4: Create a Shortcut (Optional)
**Windows - Create `start_app.bat`:**
```batch
@echo off
cd C:\path\to\your\folder
streamlit run streamlit_app.py
pause
```

**Mac/Linux - Create `start_app.sh`:**
```bash
#!/bin/bash
cd /path/to/your/folder
streamlit run streamlit_app.py
```

Then just double-click to launch!

---

## 🔧 Troubleshooting

### "streamlit: command not found"
**Solution:** Try:
```bash
pip3 install streamlit pandas matplotlib
python3 -m streamlit run streamlit_app.py
```

### "No module named 'streamlit'"
**Solution:** Make sure you ran the install command:
```bash
pip install streamlit pandas matplotlib
```

### App is slow or crashes
**Solution:** 
- Close other programs to free memory
- Lower DPI to 100 for faster processing
- Make sure you have Python 3.8 or newer: `python --version`

### Browser doesn't open automatically
**Solution:** Manually open your browser and go to:
```
http://localhost:8501
```

### Port already in use
**Solution:** Stop the existing Streamlit instance or use a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📁 File Structure

Your folder should contain:
```
📁 analyte_plotter/
├── streamlit_app.py          ← The main app
├── database.csv               ← Your data file
├── README.md                  ← This file
└── requirements.txt           ← Dependencies list (optional)
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| First-time setup | 5-10 minutes |
| Start app | 10 seconds |
| Upload CSV | 5-10 seconds |
| View single plot | 2 seconds |
| Download single plot | 1 second |
| Batch download (all 80) | 2-3 minutes |
| Stop app | Instant (Ctrl+C) |

---

## 🎯 Typical Workflow

### Monthly Reporting
1. Launch app (double-click shortcut or run command)
2. Upload latest database.csv
3. Review data summary to confirm upload
4. Go to "Batch Download" tab
5. Click "Generate All Plots"
6. Wait 2-3 minutes
7. Download ZIP file
8. Extract plots folder
9. Insert plots into your report
10. Stop app (Ctrl+C)

**Total time: ~5 minutes**

---

## 🌟 Why Streamlit is the Best Solution

✅ **Beautiful interface** - Professional, modern web UI  
✅ **One-click batch download** - Get all 80 plots in a ZIP  
✅ **Interactive controls** - Adjust settings in real-time  
✅ **Data preview** - Filter and explore your data  
✅ **Fast** - Optimized for performance  
✅ **Reliable** - Production-ready Python framework  
✅ **Flexible** - Easy to customize if needed  

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Install | `pip install streamlit pandas matplotlib` |
| Run | `streamlit run streamlit_app.py` |
| Stop | Press `Ctrl+C` in terminal |
| Update | `pip install --upgrade streamlit` |
| Help | `streamlit --help` |

---

## 🎓 Next Steps

Once you're comfortable with the basics:

1. **Create a startup shortcut** (see Tip 4)
2. **Customize default settings** in the app code if desired
3. **Set up for your team** by deploying to Streamlit Cloud (free!)

---

## ✅ You're Ready!

You now have everything you need. Just run:
```bash
streamlit run streamlit_app.py
```

Happy plotting! 📊🌊
