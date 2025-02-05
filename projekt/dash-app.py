import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

# Layout über html durch dash (super ding)
app.layout = html.Div([
    html.H1("Sinus & Kosinus", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Winkel α (-90° bis 90°)", style={'fontSize': 18}),
        dcc.Slider(
            id='alpha-slider',
            min=-90,
            max=90,
            step=1,
            value=30,
            marks={i: str(i) for i in range(-90, 91, 30)}
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        dcc.Graph(id='triangle-plot')
    ], style={'width': '60%', 'margin': 'auto'}),

    html.Div([
        dcc.Graph(id='trig-plot-sincos'),
        dcc.Graph(id='trig-plot-tancot')
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    html.Div(id='values-display', style={'fontSize': 22, 'textAlign': 'center', 'marginTop': 20})
])

@app.callback(
    [dash.Output('triangle-plot', 'figure'),
     dash.Output('trig-plot-sincos', 'figure'),
     dash.Output('trig-plot-tancot', 'figure'),
     dash.Output('values-display', 'children')],
    [dash.Input('alpha-slider', 'value')]
)

def update_graphs(alpha):
    rad = np.radians(alpha)
    A = (0, 0)
    B = (1, 0)
    C = (np.cos(rad), np.sin(rad))

    # Dreieck & So
    fig_triangle = go.Figure()
    fig_triangle.add_trace(go.Scatter(
        x=[A[0], B[0], C[0], A[0]],
        y=[A[1], B[1], C[1], A[1]],
        fill='toself',
        mode='lines+text',
        text=["A", "B", "C", "A"],
        textposition="top right",
        line=dict(color='blue', width=3)
    ))
    fig_triangle.update_layout(
        title="Dreieck mit Winkel α",
        xaxis=dict(scaleanchor="y", zeroline=True, showgrid=False),
        yaxis=dict(zeroline=True, showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # SIn COS TAN & COT 
    x_vals = np.linspace(0, 360, 500)

    sin_vals = np.sin(np.radians(x_vals))
    cos_vals = np.cos(np.radians(x_vals))
    tan_vals = np.tan(np.radians(x_vals))
    cot_vals = 1 / tan_vals


    # Werte bei tan/cot entfernen
    tan_vals[np.abs(tan_vals) > 10] = np.nan
    cot_vals[np.abs(cot_vals) > 10] = np.nan

    plot_alpha = alpha if alpha >= 0 else 360 + alpha # Negative Alhpa Werte -90 -> 270

    # Diagram für SIN & COS
    fig_sincos = go.Figure()
    fig_sincos.add_trace(go.Scatter(x=x_vals, y=sin_vals, mode='lines', name='sin(α)', line=dict(color='red'))) # Lines
    fig_sincos.add_trace(go.Scatter(x=x_vals, y=cos_vals, mode='lines', name='cos(α)', line=dict(color='blue')))
    fig_sincos.add_trace(go.Scatter(x=[plot_alpha], y=[np.sin(rad)], mode='markers', name=f"sin({alpha}°)", marker=dict(color='red', size=10))) # Punkte
    fig_sincos.add_trace(go.Scatter(x=[plot_alpha], y=[np.cos(rad)], mode='markers', name=f"cos({alpha}°)", marker=dict(color='blue', size=10))) 
    fig_sincos.update_layout(
        title="Sinus & Kosinus",
        xaxis_title="Grad",
        yaxis_title="Wert",
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Diagram für das ander 
    fig_tancot = go.Figure()
    fig_tancot.add_trace(go.Scatter(x=x_vals, y=tan_vals, mode='lines', name='tan(α)', line=dict(color='green'))) # Lines
    fig_tancot.add_trace(go.Scatter(x=x_vals, y=cot_vals, mode='lines', name='cot(α)', line=dict(color='purple')))
    if np.abs(np.tan(rad)) < 10: # Werte bei tan/cot entfernen
        fig_tancot.add_trace(go.Scatter(x=[plot_alpha], y=[np.tan(rad)], mode='markers', name=f"tan({alpha}°)", marker=dict(color='green', size=10))) # Punkte
    if np.abs(1/np.tan(rad)) < 10:
        fig_tancot.add_trace(go.Scatter(x=[plot_alpha], y=[1/np.tan(rad)], mode='markers', name=f"cot({alpha}°)", marker=dict(color='purple', size=10))) 
    fig_tancot.update_layout(
        title="Tangens & Kotangens",
        xaxis_title="Grad",
        yaxis_title="Wert",
        plot_bgcolor='rgba(0,0,0,0)'
    )

    values_text = f"sin({alpha}°) = {np.sin(rad):.3f}, cos({alpha}°) = {np.cos(rad):.3f}, tan({alpha}°) = {np.tan(rad):.3f}, cot({alpha}°) = {1/np.tan(rad):.3f}"

    return fig_triangle, fig_sincos, fig_tancot, values_text

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
