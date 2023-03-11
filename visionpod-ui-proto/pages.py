# Copyright Justin R. Goheen.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import dash
import dash_bootstrap_components as dbc
import torch
from dash import dcc, html
from utilities import create_figure, find_index, make_model_summary, metrics_summary

from visionpod import conf
from visionpod.core.module import PodModule

PREDS = torch.load(conf.PREDSPATH)
TRUTHS = torch.load(conf.VALPATH)
LABELNAMES = TRUTHS.dataset.classes
LABELS = list(range(len(LABELNAMES)))
LABELIDX = find_index(TRUTHS, label=LABELS[0], label_idx=1)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# MODEL SUMMARY
available_checkpoints = os.listdir(conf.CHKPTSPATH)
available_checkpoints.remove("README.md")
latest_checkpoint = available_checkpoints[0]
chkpt_filename = os.path.join(conf.CHKPTSPATH, latest_checkpoint)
model = PodModule.load_from_checkpoint(chkpt_filename)
model_layers, model_params = make_model_summary(model)
metrics = metrics_summary()
metrics_names = list(metrics.keys())
metrics_values = [round(i, 4) for i in list(metrics.values())]

# APP LAYOUT
NavBar = dbc.NavbarSimple(
    brand="VisionTransformer Base 32",
    color="#792ee5",
    dark=True,
    fluid=True,
    className="app-title",
)

Control = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Label", className="card-title"),
            dcc.Dropdown(
                options=LABELNAMES,
                value=LABELNAMES[0],
                multi=False,
                id="dropdown",
                searchable=True,
            ),
        ]
    ),
    className="model-card-container",
)

ModelCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H1("Model Card", id="model_card", className="card-title"),
                html.Br(),
                html.H3("Layers", className="card-title"),
                model_layers,
                html.Br(),
                html.H3("Parameters", className="card-title"),
                html.P(
                    f"{model_params[0]}",
                    id="model_info_1",
                    className="model-card-text",
                ),
                html.P(
                    f"{model_params[1]}",
                    id="model_info_2",
                    className="model-card-text",
                ),
                html.P(
                    f"{model_params[2]}",
                    id="model_info_3",
                    className="model-card-text",
                ),
                html.P(
                    f"{model_params[3]}",
                    id="model_info_4",
                    className="model-card-text",
                ),
            ]
        ),
    ],
    className="model-card-container",
)

SideBar = dbc.Col(
    [
        Control,
        html.Br(),
        ModelCard,
    ],
    width=3,
)

GroundTruth = dcc.Graph(
    id="left-fig",
    figure=create_figure(TRUTHS[LABELIDX][0], "Ground Truth"),
    config={
        "responsive": True,
        "displayModeBar": True,
        "displaylogo": False,
    },
)

Predictions = dbc.Card(
    [
        dbc.CardHeader("Predicted Class"),
        dbc.CardBody(
            [
                html.H3(
                    LABELNAMES[torch.argmax(PREDS[LABELIDX][0])],
                    id="right-fig",
                ),
            ]
        ),
    ],
)

Metrics = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4(metrics_names[0], className="card-title"),
                        html.P(metrics_values[0], id="metric_1_text", className="metric-card-text"),
                    ],
                    id="metric_1_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4(metrics_names[1], className="card-title"),
                        html.P(metrics_values[1], id="metric_2_text", className="metric-card-text"),
                    ],
                    id="metric_2_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4(metrics_names[2], className="card-title"),
                        html.P(metrics_values[2], id="metric_3_text", className="metric-card-text"),
                    ],
                    id="metric_3_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4(metrics_names[3], className="card-title"),
                        html.P(metrics_values[3], id="metric_4_text", className="metric-card-text"),
                    ],
                    id="metric_4_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
    ],
    id="metrics",
    justify="center",
)

Graphs = dbc.Row(
    [
        dbc.Col([GroundTruth], className="pretty-container", width=4),
        dbc.Col(width=1),
        dbc.Col([Predictions], width=4),
    ],
    justify="center",
    align="middle",
    className="graph-row",
)

MainArea = dbc.Col([Metrics, html.Br(), Graphs])

Body = dbc.Container([dbc.Row([SideBar, MainArea])], fluid=True)

# PASS LAYOUT TO DASH
app.layout = html.Div(
    [
        NavBar,
        html.Br(),
        Body,
    ]
)


if __name__ == "__main__":

    from dash.dependencies import Input, Output
    from torch.utils.data import TensorDataset

    predictions: TensorDataset = torch.load(conf.PREDSPATH)
    ground_truths: TensorDataset = torch.load(conf.VALPATH)

    @app.callback(
        [Output("left-fig", "figure"), Output("right-fig", "children")],
        [Input("dropdown", "value")],
    )
    def update_figure(label_value):
        xidx = 0
        labelidx = 1
        idx = find_index(ground_truths, label=LABELNAMES.index(label_value), label_idx=1)
        gt = ground_truths[idx][xidx]
        pred = LABELNAMES[torch.argmax(predictions[idx][labelidx])]
        ground_truth_fig = create_figure(gt, "Ground Truth")
        return ground_truth_fig, pred

    app.run_server(debug=True)