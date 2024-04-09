# app.py
from dash import Dash
from components.layout import serve_layout

app = Dash(__name__)

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
