import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State

df = pd.read_csv('spotify_top100.csv')

# změny pro hostování na webu
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Spotify's top 100 annual list",id="chart_title"),

    dcc.Dropdown(
      id='parameters-dropdown',
      value="bpm",
      options=df.columns[5:15]
),

    html.H3("Choose year:",id="slider_label"),

    dcc.Slider(
    id = "my_slider",
    min=df["top year"].min(),
    max=df["top year"].max(),
    value=df["top year"].max(),
    marks = {i: f'{i:.0f}' for i in sorted(df["top year"].dropna().unique())},
    step=1
),

    dcc.Graph(id="my_graph")
])

@app.callback(Output("my_graph", "figure"),
              Input("my_slider", "value"),
              State("parameters-dropdown", "value")
             ) 

def update_chart(selected_year, selected_parameter):
    df_selected = df[df["top year"]==selected_year]
    top_15 = df_selected.sort_values(by=selected_parameter, ascending=False).head(15)
    chart = px.bar(top_15, 
                   x="title", 
                   y=selected_parameter, 
                   color="artist",
                   title=f"Top 15 songs from {selected_year} by {selected_parameter}",
                  template="plotly_white")
    chart.update_layout(xaxis_tickangle=-45)
    return chart

