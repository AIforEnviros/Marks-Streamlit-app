"""
Analyte Plotter - Streamlit Web App
Author: Created for Mark
Date: October 2025

A beautiful, easy-to-use web interface for plotting analyte data.
Just run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime
import zipfile

# Page configuration
st.set_page_config(
    page_title="Analyte Plotter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def load_data(uploaded_file):
    """Load and process the CSV data."""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Clean analyte names
        df['Analyte'] = df['Analyte'].str.strip()
        
        # Convert date to datetime
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        
        # Convert Value to numeric
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def create_plot(df, analyte, figsize=(14, 7), dpi=150):
    """Create a plot for a specific analyte."""
    # Filter data for this analyte
    analyte_data = df[df['Analyte'] == analyte].copy()
    
    # Check if there's valid data
    if analyte_data['Value'].isna().all():
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Plot data for each bore
    bores = sorted(analyte_data['Bore_ID'].unique())
    for bore in bores:
        bore_data = analyte_data[analyte_data['Bore_ID'] == bore].sort_values('Date')
        ax.plot(bore_data['Date'], bore_data['Value'], 
               marker='o', linestyle='-', linewidth=1.5, 
               markersize=4, label=bore, alpha=0.8)
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title(f'{analyte}', fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha='right')
    
    # Add legend
    if len(bores) <= 15:
        ax.legend(title='Bore ID', bbox_to_anchor=(1.02, 1), 
                 loc='upper left', fontsize=9)
    else:
        ax.legend(title='Bore ID', bbox_to_anchor=(1.02, 1), 
                 loc='upper left', fontsize=7, ncol=2)
    
    plt.tight_layout()
    return fig

def plot_to_bytes(fig):
    """Convert matplotlib figure to bytes for download."""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return buf

def create_all_plots_zip(df, analytes, progress_bar, status_text):
    """Create a ZIP file containing all plots."""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, analyte in enumerate(analytes):
            # Update progress
            progress = (idx + 1) / len(analytes)
            progress_bar.progress(progress)
            status_text.text(f"Creating plot {idx + 1}/{len(analytes)}: {analyte}")
            
            # Create plot
            fig = create_plot(df, analyte)
            
            if fig is not None:
                # Save to buffer
                img_buffer = plot_to_bytes(fig)
                
                # Create safe filename
                safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' 
                                       for c in analyte)
                safe_filename = safe_filename.replace(' ', '_') + '.png'
                
                # Add to zip
                zip_file.writestr(safe_filename, img_buffer.read())
                
            plt.close(fig)
    
    zip_buffer.seek(0)
    return zip_buffer

# Main app
def main():
    # Header
    st.title("📊 Analyte Time Series Plotter")
    st.markdown("Upload your CSV file to visualize analyte trends across all bore holes")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Database CSV",
            type=['csv'],
            help="Upload your database.csv file containing Bore_ID, Date, Analyte, and Value columns"
        )
        
        if uploaded_file is not None:
            st.success("✓ File uploaded successfully!")
        
        st.markdown("---")
        
        # Plot settings
        st.subheader("Plot Settings")
        
        plot_width = st.slider("Plot Width", min_value=8, max_value=20, value=14, step=1)
        plot_height = st.slider("Plot Height", min_value=4, max_value=12, value=7, step=1)
        plot_dpi = st.select_slider("Plot Quality (DPI)", options=[100, 150, 200, 300], value=150)
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. Upload your CSV file
        2. Select an analyte from the dropdown
        3. View the interactive plot
        4. Download individual plots or all at once
        """)
    
    # Main content
    if uploaded_file is None:
        # Welcome screen
        st.info("👈 Please upload a CSV file using the sidebar to get started")
        
        st.markdown("### Expected CSV Format")
        st.markdown("""
        Your CSV should have these columns:
        - **Bore_ID**: Identifier for the bore hole
        - **Date**: Date of measurement (DD/MM/YYYY format)
        - **Analyte**: Name of the analyte being measured
        - **Value**: Numeric measurement value
        """)
        
        # Example data
        example_data = pd.DataFrame({
            'Bore_ID': ['LCLBOR01', 'LCLBOR01', 'LCLBOR04'],
            'Date': ['25/07/2016', '25/07/2016', '25/07/2016'],
            'Analyte': ['Aluminium', 'Arsenic', 'Aluminium'],
            'Value': [12.0, 0.021, 15.0]
        })
        st.dataframe(example_data, use_container_width=True)
        
    else:
        # Load data
        with st.spinner("Loading data..."):
            df = load_data(uploaded_file)
        
        if df is not None:
            # Data summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            with col2:
                st.metric("Unique Bores", df['Bore_ID'].nunique())
            with col3:
                st.metric("Unique Analytes", df['Analyte'].nunique())
            with col4:
                date_range = f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}"
                st.metric("Date Range", "")
                st.caption(date_range)
            
            st.markdown("---")
            
            # Get unique analytes
            analytes = sorted(df['Analyte'].unique())
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📈 Single Analyte", "📊 Batch Download", "📋 Data Preview"])
            
            with tab1:
                # Single analyte selection and plotting
                selected_analyte = st.selectbox(
                    "Select Analyte to Plot",
                    options=analytes,
                    help="Choose an analyte to visualize"
                )
                
                if st.button("Generate Plot", type="primary"):
                    with st.spinner(f"Creating plot for {selected_analyte}..."):
                        fig = create_plot(df, selected_analyte, 
                                        figsize=(plot_width, plot_height), 
                                        dpi=plot_dpi)
                        
                        if fig is not None:
                            st.pyplot(fig)
                            
                            # Download button
                            img_buffer = plot_to_bytes(fig)
                            st.download_button(
                                label="⬇️ Download Plot as PNG",
                                data=img_buffer,
                                file_name=f"{selected_analyte.replace(' ', '_')}.png",
                                mime="image/png"
                            )
                            
                            plt.close(fig)
                        else:
                            st.warning(f"No valid data available for {selected_analyte}")
            
            with tab2:
                # Batch download all plots
                st.subheader("Download All Analyte Plots")
                st.markdown(f"Generate and download plots for all **{len(analytes)}** analytes as a ZIP file")

                # Add option to view plots
                col1, col2 = st.columns(2)
                with col1:
                    show_preview = st.checkbox("📋 Show preview of all plots", value=False,
                                              help="Display all plots in the app (may take time to load)")
                with col2:
                    plots_per_row = st.selectbox("Plots per row", [1, 2, 3], index=1)

                if st.button("🎨 Generate All Plots", type="primary"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # Store plots if preview is enabled
                    generated_plots = []

                    if show_preview:
                        st.markdown("---")
                        st.subheader("📊 Plot Gallery")

                        # Create plots and display them
                        for idx, analyte in enumerate(analytes):
                            # Update progress
                            progress = (idx + 1) / len(analytes)
                            progress_bar.progress(progress)
                            status_text.text(f"Creating plot {idx + 1}/{len(analytes)}: {analyte}")

                            # Create plot
                            fig = create_plot(df, analyte,
                                            figsize=(plot_width, plot_height),
                                            dpi=plot_dpi)

                            if fig is not None:
                                generated_plots.append((analyte, fig))

                        status_text.text("✓ All plots created!")
                        progress_bar.empty()

                        # Display plots in grid
                        st.markdown("### All Generated Plots")
                        for idx in range(0, len(generated_plots), plots_per_row):
                            cols = st.columns(plots_per_row)
                            for col_idx, col in enumerate(cols):
                                plot_idx = idx + col_idx
                                if plot_idx < len(generated_plots):
                                    analyte, fig = generated_plots[plot_idx]
                                    with col:
                                        st.markdown(f"**{analyte}**")
                                        st.pyplot(fig)

                        # Create ZIP from the generated plots
                        st.markdown("---")
                        st.markdown("### Download Options")
                        with st.spinner("Creating ZIP file..."):
                            zip_buffer = BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                for analyte, fig in generated_plots:
                                    img_buffer = plot_to_bytes(fig)
                                    safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_'
                                                           for c in analyte)
                                    safe_filename = safe_filename.replace(' ', '_') + '.png'
                                    zip_file.writestr(safe_filename, img_buffer.read())
                                    plt.close(fig)
                            zip_buffer.seek(0)

                        st.success(f"Successfully created {len(generated_plots)} plots!")

                        # Download button for zip
                        st.download_button(
                            label="⬇️ Download All Plots (ZIP)",
                            data=zip_buffer,
                            file_name=f"analyte_plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                            mime="application/zip"
                        )
                    else:
                        # Original behavior - just create ZIP without preview
                        with st.spinner("Creating all plots... This may take a few minutes..."):
                            zip_buffer = create_all_plots_zip(df, analytes, progress_bar, status_text)

                        status_text.text("✓ All plots created!")
                        progress_bar.empty()

                        st.success(f"Successfully created {len(analytes)} plots!")

                        # Download button for zip
                        st.download_button(
                            label="⬇️ Download All Plots (ZIP)",
                            data=zip_buffer,
                            file_name=f"analyte_plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                            mime="application/zip"
                        )
            
            with tab3:
                # Data preview
                st.subheader("Data Preview")
                
                # Filters
                col1, col2 = st.columns(2)
                with col1:
                    filter_bore = st.multiselect(
                        "Filter by Bore ID",
                        options=sorted(df['Bore_ID'].unique()),
                        default=None
                    )
                with col2:
                    filter_analyte = st.multiselect(
                        "Filter by Analyte",
                        options=analytes,
                        default=None
                    )
                
                # Apply filters
                filtered_df = df.copy()
                if filter_bore:
                    filtered_df = filtered_df[filtered_df['Bore_ID'].isin(filter_bore)]
                if filter_analyte:
                    filtered_df = filtered_df[filtered_df['Analyte'].isin(filter_analyte)]
                
                st.dataframe(filtered_df, use_container_width=True, height=400)
                
                # Download filtered data
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Filtered Data as CSV",
                    data=csv,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
