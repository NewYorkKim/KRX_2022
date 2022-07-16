import dash
import dash_core_components as dcc
import dash_html_components as html
# import plotly.express as px
import pandas as pd

kakao = pd.read_csv('../sample/feargreed_kakao_rev.csv')
naver = pd.read_csv('../sample/feargreed_naver_rev.csv')

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="공포-탐욕 지수",),
        html.P(
            children="test",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": kakao["LSTM"],
                        "y": kakao["BERT"],
                        "type": "lines",
                    }
                ],
                "layout": {"title": "카카오"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": naver["LSTM"],
                        "y": naver["BERT"],
                        "type":"lines",
                    },
                ],
                "layout": {"title": "네이버"}
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)