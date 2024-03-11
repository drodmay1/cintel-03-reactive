import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="DavidRm Penguin", fillable=True)

with ui.sidebar(open="open"):
    
    ui.h2("Sidebar")
    
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 30)
    
    ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 100, 20)

    ui.hr()
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

    ui.a(
        "GitHub",
         href="https://github.com/drodmay1/cintel-02-data.git",
         target="_blank",
         )

# Creates a DataTable showing all data

with ui.layout_columns(col_widths=(4, 8)):        
    with ui.card():
        "DataTable"

    ui.h2("Penguins Table")

    @render.data_frame
    def render_penguins_table():
        return penguins_df

# Creates a DataGrid showing all data

with ui.layout_columns(col_widths=(4, 8)):        
    with ui.card():
        "DataGrid"

    ui.h2("Penguins DataGrid")

@render.ui()
def rows():
    rows = input.penguins_df_selected_rows()  
    selected = ", ".join(str(i) for i in sorted(rows)) if rows else "None"
    return f"Rows selected: {selected}"

@render.data_frame
def penguins_data():
    return render.DataGrid(penguins_df, row_selection_mode="multiple") 

# Creates a Plotly Histogram showing all species

with ui.card(full_screen=True):
    ui.card_header("Plotly Histogram")
    
    @render_plotly
    def plotly_histogram():
        return px.histogram(
            penguins_df, x=input.selected_attribute(), nbins=input.plotly_bin_count()
        )

# Creates a Seaborn Histogram showing all species

with ui.card(full_screen=True):
    ui.card_header("Seaborn Histogram")

    @render.plot(alt="Seaborn Histogram")
    def seaborn_histogram():
        histplot = sns.histplot(data=penguins_df, x="body_mass_g", bins=input.seaborn_bin_count())
        histplot.set_title("Palmer Penguins")
        histplot.set_xlabel("Mass")
        histplot.set_ylabel("Count")
        return histplot

# Creates a Plotly Scatterplot showing all species

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(penguins_df,
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=8, 
        )
