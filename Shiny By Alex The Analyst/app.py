from matplotlib import ticker
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shiny import App, ui, render
from matplotlib.ticker import MaxNLocator
from pathlib import Path
df = pd.read_csv(Path(__file__).parent/"Global YouTube Statistics.csv")
# Read the CSV file
#df = pd.read_csv('/home/rajaahmedalikhan/Shiny app/Global YouTube Statistics.csv')

# Print columns to debug
print("Columns in DataFrame before filtering:", df.columns)

# Correcting the error in 'to_numeric'
df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')

# Filtering the DataFrame correctly
df_filtered = df[df['subscribers'] > 50_000_000]
df_filtered = df_filtered.dropna(subset=['subscribers'])
df_filtered = df_filtered[np.isfinite(df_filtered['subscribers'])]

# Print columns to debug
print("Columns in DataFrame after filtering:", df_filtered.columns)

# Define the UI with custom CSS for dark mode
app_ui = ui.page_fluid(
    ui.tags.head(ui.tags.style("""
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .slider {
            background-color: #333333;
            color: #ffffff;
        }
        .slider::-webkit-slider-thumb {
            background-color: #ffffff;
        }
    """)),
    ui.input_slider("bins", "Number of bins", 0, 100, 20),
    ui.input_text("text", "Search Youtuber", " "),
    ui.output_plot("distplot"),
    ui.output_data_frame("youtube_df")
)

# Define the server logic
def server(input, output, session):
    @output
    @render.plot
    def distplot():
        searchtext = input.text().strip().lower()
        filtered_df = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na=False)] if searchtext else df_filtered

        # Debugging filtered_df
        print("Filtered DataFrame for distplot:")
        print(filtered_df)

        # Creating plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(filtered_df['subscribers'], bins=input.bins(), color='blue', alpha=0.7, density=True)
        ax.set_title('Distributions of subscribers')
        ax.set_xlabel('Subscribers')
        ax.set_ylabel('Density')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        plt.xticks(rotation=45)
        plt.grid(True)
        return fig

    @output
    @render.data_frame
    def youtube_df():
        searchtext = input.text().strip().lower()
        filtered_df = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na=False)] if searchtext else df_filtered

        # Debugging filtered_df
        print("Filtered DataFrame for youtube_df:")
        print(filtered_df)

        return filtered_df

# Create the app
app = App(app_ui, server)
