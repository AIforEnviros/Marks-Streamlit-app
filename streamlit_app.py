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
import pymannkendall as mk

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

def create_plot(df, analyte, figsize=(14, 7), dpi=150,
                date_min=None, date_max=None,
                y_scale='linear', y_min=None, y_max=None,
                force_x_limits=False):
    """Create a plot for a specific analyte.

    Args:
        df: DataFrame with the data
        analyte: Analyte name to plot
        figsize: Figure size tuple
        dpi: Resolution
        date_min: Minimum date for filtering (optional)
        date_max: Maximum date for filtering (optional)
        y_scale: 'linear' or 'log' for Y-axis scale
        y_min: Minimum Y-axis value (optional, for manual scaling)
        y_max: Maximum Y-axis value (optional, for manual scaling)
        force_x_limits: If True, force X-axis to show full date range even if no data
    """
    # Filter data for this analyte
    analyte_data = df[df['Analyte'] == analyte].copy()

    # Apply date range filter if specified
    if date_min is not None:
        analyte_data = analyte_data[analyte_data['Date'] >= date_min]
    if date_max is not None:
        analyte_data = analyte_data[analyte_data['Date'] <= date_max]

    # Check if there's valid data
    if len(analyte_data) == 0 or analyte_data['Value'].isna().all():
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

    # Set Y-axis scale
    ax.set_yscale(y_scale)

    # Set Y-axis limits if specified
    if y_min is not None or y_max is not None:
        current_ylim = ax.get_ylim()
        new_ymin = y_min if y_min is not None else current_ylim[0]
        new_ymax = y_max if y_max is not None else current_ylim[1]
        ax.set_ylim(new_ymin, new_ymax)

    # Set X-axis limits to ensure consistent date range across all plots (optional)
    if force_x_limits and date_min is not None and date_max is not None:
        ax.set_xlim(date_min, date_max)

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

def perform_mann_kendall_analysis(df, date_min=None, date_max=None):
    """Perform Mann-Kendall trend analysis for each analyte and bore.

    Args:
        df: DataFrame with the data
        date_min: Minimum date for filtering (optional)
        date_max: Maximum date for filtering (optional)

    Returns:
        DataFrame with Mann-Kendall results
    """
    # Apply date filter if specified
    filtered_df = df.copy()
    if date_min is not None:
        filtered_df = filtered_df[filtered_df['Date'] >= date_min]
    if date_max is not None:
        filtered_df = filtered_df[filtered_df['Date'] <= date_max]

    results = []

    # Group by analyte and bore
    for analyte in filtered_df['Analyte'].unique():
        analyte_data = filtered_df[filtered_df['Analyte'] == analyte]

        for bore in analyte_data['Bore_ID'].unique():
            bore_data = analyte_data[analyte_data['Bore_ID'] == bore].sort_values('Date')

            # Remove NaN values
            values = bore_data['Value'].dropna()

            # Need at least 3 data points for Mann-Kendall test
            if len(values) >= 3:
                try:
                    # Convert to numpy array and ensure proper format
                    values_array = values.values if hasattr(values, 'values') else values

                    # Perform Mann-Kendall test
                    mk_result = mk.original_test(values_array)

                    results.append({
                        'Analyte': analyte,
                        'Bore_ID': bore,
                        'Trend': mk_result.trend,
                        'P-value': mk_result.p,
                        'Tau': mk_result.Tau,  # Note: capital T
                        'Slope': mk_result.slope,
                        'N_points': len(values),
                        'Significant': 'Yes' if mk_result.p < 0.05 else 'No'
                    })
                except Exception as e:
                    # If test fails, record the error with details
                    error_msg = str(e)[:50]  # Truncate long error messages
                    results.append({
                        'Analyte': analyte,
                        'Bore_ID': bore,
                        'Trend': f'Error: {error_msg}',
                        'P-value': None,
                        'Tau': None,
                        'Slope': None,
                        'N_points': len(values),
                        'Significant': 'N/A'
                    })
            else:
                # Not enough data points
                results.append({
                    'Analyte': analyte,
                    'Bore_ID': bore,
                    'Trend': 'Insufficient data',
                    'P-value': None,
                    'Tau': None,
                    'Slope': None,
                    'N_points': len(values),
                    'Significant': 'N/A'
                })

    return pd.DataFrame(results)

def create_all_plots_zip(df, analytes, progress_bar, status_text,
                         figsize=(14, 7), dpi=150,
                         date_min=None, date_max=None,
                         y_scale='linear', y_min=None, y_max=None,
                         force_x_limits=False):
    """Create a ZIP file containing all plots.

    Args:
        df: DataFrame with the data
        analytes: List of analyte names to plot
        progress_bar: Streamlit progress bar object
        status_text: Streamlit text object for status updates
        figsize: Figure size tuple
        dpi: Resolution
        date_min: Minimum date for filtering (optional)
        date_max: Maximum date for filtering (optional)
        y_scale: 'linear' or 'log' for Y-axis scale
        y_min: Minimum Y-axis value (optional)
        y_max: Maximum Y-axis value (optional)
        force_x_limits: If True, force X-axis to show full date range
    """
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, analyte in enumerate(analytes):
            # Update progress
            progress = (idx + 1) / len(analytes)
            progress_bar.progress(progress)
            status_text.text(f"Creating plot {idx + 1}/{len(analytes)}: {analyte}")

            # Create plot with filters
            fig = create_plot(df, analyte,
                            figsize=figsize, dpi=dpi,
                            date_min=date_min, date_max=date_max,
                            y_scale=y_scale, y_min=y_min, y_max=y_max,
                            force_x_limits=force_x_limits)

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

            # Global filters and settings
            st.subheader("🎛️ Global Plot Settings")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Date Range Filter**")
                global_date_min = st.date_input(
                    "Start Date",
                    value=df['Date'].min(),
                    min_value=df['Date'].min(),
                    max_value=df['Date'].max(),
                    help="Filter all plots to show data from this date onwards"
                )
                global_date_max = st.date_input(
                    "End Date",
                    value=df['Date'].max(),
                    min_value=df['Date'].min(),
                    max_value=df['Date'].max(),
                    help="Filter all plots to show data up to this date"
                )

            with col2:
                st.markdown("**Y-Axis Settings**")
                global_y_scale = st.radio(
                    "Y-Axis Scale",
                    options=['linear', 'log'],
                    horizontal=True,
                    help="Choose between linear or logarithmic Y-axis scale"
                )

                col2a, col2b = st.columns(2)
                with col2a:
                    global_y_min = st.number_input(
                        "Y-Axis Min (optional)",
                        value=None,
                        help="Leave empty for auto-scale"
                    )
                with col2b:
                    global_y_max = st.number_input(
                        "Y-Axis Max (optional)",
                        value=None,
                        help="Leave empty for auto-scale"
                    )

            # X-axis consistency option
            st.markdown("**X-Axis Settings**")
            force_consistent_x_axis = st.checkbox(
                "📅 Force consistent X-axis range across all plots",
                value=False,
                help="When enabled, all plots will show the same date range (from start to end date above), even if some analytes have no data for certain periods. This makes all graphs directly comparable."
            )

            # Convert dates to pandas Timestamp for filtering
            global_date_min = pd.Timestamp(global_date_min)
            global_date_max = pd.Timestamp(global_date_max)

            st.markdown("---")

            # Get unique analytes
            analytes = sorted(df['Analyte'].unique())

            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Single Analyte", "📊 Batch Download", "📈 Trend Analysis", "📋 Data Preview"])
            
            with tab1:
                # Single analyte selection and plotting
                selected_analyte = st.selectbox(
                    "Select Analyte to Plot",
                    options=analytes,
                    help="Choose an analyte to visualize"
                )

                # Per-plot override controls
                with st.expander("⚙️ Override Global Settings (Optional)", expanded=False):
                    st.markdown("Override the global settings for this specific plot only")

                    override_enabled = st.checkbox("Enable custom settings for this plot")

                    if override_enabled:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Date Range Override**")
                            override_date_min = st.date_input(
                                "Override Start Date",
                                value=global_date_min,
                                min_value=df['Date'].min(),
                                max_value=df['Date'].max(),
                                key="override_date_min"
                            )
                            override_date_max = st.date_input(
                                "Override End Date",
                                value=global_date_max,
                                min_value=df['Date'].min(),
                                max_value=df['Date'].max(),
                                key="override_date_max"
                            )

                        with col2:
                            st.markdown("**Y-Axis Override**")
                            override_y_scale = st.radio(
                                "Override Y-Axis Scale",
                                options=['linear', 'log'],
                                index=0 if global_y_scale == 'linear' else 1,
                                horizontal=True,
                                key="override_y_scale"
                            )

                            col2a, col2b = st.columns(2)
                            with col2a:
                                override_y_min = st.number_input(
                                    "Override Y-Min",
                                    value=global_y_min,
                                    key="override_y_min"
                                )
                            with col2b:
                                override_y_max = st.number_input(
                                    "Override Y-Max",
                                    value=global_y_max,
                                    key="override_y_max"
                                )

                        # Use override values
                        plot_date_min = pd.Timestamp(override_date_min)
                        plot_date_max = pd.Timestamp(override_date_max)
                        plot_y_scale = override_y_scale
                        plot_y_min = override_y_min
                        plot_y_max = override_y_max
                    else:
                        # Use global values
                        plot_date_min = global_date_min
                        plot_date_max = global_date_max
                        plot_y_scale = global_y_scale
                        plot_y_min = global_y_min
                        plot_y_max = global_y_max

                if st.button("Generate Plot", type="primary"):
                    with st.spinner(f"Creating plot for {selected_analyte}..."):
                        fig = create_plot(df, selected_analyte,
                                        figsize=(plot_width, plot_height),
                                        dpi=plot_dpi,
                                        date_min=plot_date_min,
                                        date_max=plot_date_max,
                                        y_scale=plot_y_scale,
                                        y_min=plot_y_min,
                                        y_max=plot_y_max,
                                        force_x_limits=force_consistent_x_axis)

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

                            # Create plot with global filters
                            fig = create_plot(df, analyte,
                                            figsize=(plot_width, plot_height),
                                            dpi=plot_dpi,
                                            date_min=global_date_min,
                                            date_max=global_date_max,
                                            y_scale=global_y_scale,
                                            y_min=global_y_min,
                                            y_max=global_y_max,
                                            force_x_limits=force_consistent_x_axis)

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
                            zip_buffer = create_all_plots_zip(
                                df, analytes, progress_bar, status_text,
                                figsize=(plot_width, plot_height),
                                dpi=plot_dpi,
                                date_min=global_date_min,
                                date_max=global_date_max,
                                y_scale=global_y_scale,
                                y_min=global_y_min,
                                y_max=global_y_max,
                                force_x_limits=force_consistent_x_axis
                            )

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
                # Mann-Kendall Trend Analysis
                st.subheader("📈 Mann-Kendall Trend Analysis")
                st.markdown("""
                This analysis performs the Mann-Kendall test to detect monotonic trends in the data.
                Results show the trend direction, statistical significance, and Kendall's Tau coefficient for each bore.
                """)

                if st.button("🔍 Run Trend Analysis", type="primary", key="run_mk_analysis"):
                    with st.spinner("Performing Mann-Kendall analysis..."):
                        # Perform analysis with global date filter
                        mk_results = perform_mann_kendall_analysis(df, global_date_min, global_date_max)

                    if len(mk_results) > 0:
                        st.success(f"Analysis complete! Found {len(mk_results)} bore-analyte combinations.")

                        # Filter options
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            show_only_significant = st.checkbox(
                                "Show only significant trends (p < 0.05)",
                                value=False
                            )

                        with col2:
                            filter_trend = st.multiselect(
                                "Filter by Trend",
                                options=['increasing', 'decreasing', 'no trend', 'Insufficient data', 'Error'],
                                default=None,
                                key="mk_filter_trend"
                            )

                        with col3:
                            filter_analyte_mk = st.multiselect(
                                "Filter by Analyte",
                                options=sorted(mk_results['Analyte'].unique()),
                                default=None,
                                key="mk_filter_analyte"
                            )

                        # Apply filters
                        display_results = mk_results.copy()

                        if show_only_significant:
                            display_results = display_results[display_results['Significant'] == 'Yes']

                        if filter_trend:
                            display_results = display_results[display_results['Trend'].isin(filter_trend)]

                        if filter_analyte_mk:
                            display_results = display_results[display_results['Analyte'].isin(filter_analyte_mk)]

                        # Display results
                        st.markdown(f"**Showing {len(display_results)} of {len(mk_results)} results**")

                        # Style the dataframe
                        st.dataframe(
                            display_results.style.format({
                                'P-value': lambda x: f'{x:.4f}' if pd.notna(x) else 'N/A',
                                'Tau': lambda x: f'{x:.4f}' if pd.notna(x) else 'N/A',
                                'Slope': lambda x: f'{x:.6f}' if pd.notna(x) else 'N/A'
                            }),
                            use_container_width=True,
                            height=500
                        )

                        # Summary statistics
                        st.markdown("---")
                        st.subheader("Summary Statistics")

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            increasing = len(mk_results[mk_results['Trend'] == 'increasing'])
                            st.metric("Increasing Trends", increasing)

                        with col2:
                            decreasing = len(mk_results[mk_results['Trend'] == 'decreasing'])
                            st.metric("Decreasing Trends", decreasing)

                        with col3:
                            no_trend = len(mk_results[mk_results['Trend'] == 'no trend'])
                            st.metric("No Trend", no_trend)

                        with col4:
                            significant = len(mk_results[mk_results['Significant'] == 'Yes'])
                            st.metric("Significant (p<0.05)", significant)

                        # Download button
                        csv = mk_results.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Download Trend Analysis Results as CSV",
                            data=csv,
                            file_name=f"mann_kendall_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No results found. Please check your data.")

            with tab4:
                # Data preview
                st.subheader("Data Preview")
                
                # Filters
                col1, col2 = st.columns(2)
                with col1:
                    filter_bore = st.multiselect(
                        "Filter by Bore ID",
                        options=sorted(df['Bore_ID'].unique()),
                        default=None,
                        key="preview_filter_bore"
                    )
                with col2:
                    filter_analyte = st.multiselect(
                        "Filter by Analyte",
                        options=analytes,
                        default=None,
                        key="preview_filter_analyte"
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
