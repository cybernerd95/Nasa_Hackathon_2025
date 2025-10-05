import pandas as pd
import glob
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# -----------------------------
# Step 1: Load all CSV files
# -----------------------------
files = glob.glob(r"D:\NASA_hackathon_2025\shark_data\*.csv")
all_data = [pd.read_csv(f) for f in files]
data = pd.concat(all_data, ignore_index=True)

# -----------------------------
# Step 2: Prepare data
# -----------------------------
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(['id', 'date'])
plane_ids = data['id'].unique()

# Optional: reduce number of frames for performance
data['time_frame'] = data['date'].dt.floor('1H')  # 1-hour resolution
time_frames = sorted(data['time_frame'].unique())

# -----------------------------
# Step 3: Initialize Dash app
# -----------------------------
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("SHARK Movement Visualizer"),
    html.Label("Select SHARK:"),
    dcc.Dropdown(
        id='plane-dropdown',
        options=[{'label': pid, 'value': pid} for pid in plane_ids] + [{'label': 'All', 'value': 'All'}],
        value='All'
    ),
    html.Button("Clear Selection", id='clear-btn', n_clicks=0),
    dcc.Slider(
        id='time-slider',
        min=0,
        max=len(time_frames)-1,
        step=1,
        value=0,
        marks={i: str(time_frames[i].strftime('%Y-%m-%d %H:%M')) for i in range(0, len(time_frames), max(1, len(time_frames)//10))},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Graph(id='plane-map', style={'height': '700px'})
])

# -----------------------------
# Step 4: Callback to update map
# -----------------------------
@app.callback(
    Output('plane-map', 'figure'),
    Input('plane-dropdown', 'value'),
    Input('time-slider', 'value'),
    Input('clear-btn', 'n_clicks')
)
def update_map(selected_plane, slider_index, clear_clicks):
    current_time = time_frames[slider_index]
    
    if selected_plane == 'All' or selected_plane is None:
        filtered_data = data[data['time_frame'] <= current_time]
    else:
        filtered_data = data[(data['id'] == selected_plane) & (data['time_frame'] <= current_time)]
    
    fig = go.Figure()
    
    # Draw paths for each plane
    for pid in filtered_data['id'].unique():
        plane_data = filtered_data[filtered_data['id'] == pid]
        fig.add_trace(go.Scattergeo(
            lon=plane_data['lon'],
            lat=plane_data['lat'],
            mode='lines+markers',
            name=pid,
            line=dict(width=2),
            marker=dict(size=6),
            hovertext=plane_data['date'].astype(str)
        ))
    
    fig.update_geos(showcoastlines=True, showland=True, showcountries=True, fitbounds="locations")
    fig.update_layout(title=f"SHARK Movements until {current_time}", margin={"r":0,"t":50,"l":0,"b":0})
    
    return fig

# -----------------------------
# Step 5: Run app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
