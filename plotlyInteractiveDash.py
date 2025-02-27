#installs

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launchsites = spacex_df['Launch Site'].unique().tolist()
sites = []
sites.append({'label': 'All Launch Sites', 'value': 'All Launch Sites'})
for i in launchsites:
 sites.append({'label': i, 'value': i})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='sitedropdown',options=sites,placeholder='Select a Launch Site', searchable = True , value = 'All Launch Sites',              
                                             style={'width':'80%','padding':'3px', 'font-size':'20px','text-align-last':'center'}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payloadslider', min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                marks=dict([(i,str(i)) for i in range(int(min_payload),int(max_payload),1000)]),
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])



#TASK 2:
#Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
      Output(component_id='success-pie-chart',component_property='figure'),
      [Input(component_id='sitedropdown',component_property='value')]
)
def update_graph(sitedropdown):
    if sitedropdown != "All Launch Sites":
        pie_data=spacex_df.loc[spacex_df["Launch Site"]==sitedropdown]
        pie_fig=px.pie(pie_data, names="class",title='Total Success Launches for the site '+sitedropdown)
    else: 
        pie_data= spacex_df.loc[spacex_df["class"]==1]
        pie_fig=px.pie(pie_data, names="Launch Site",title='Total Success Launches by Site')
    return pie_fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
      Output(component_id='success-payload-scatter-chart',component_property='figure'),
      [Input(component_id='sitedropdown',component_property='value'),Input(component_id="payloadslider", component_property="value")]
)
def get_scatter(sitedropdown,payloadslider):
    minPayload,maxPayload=payloadslider
    payloadRange = (spacex_df['Payload Mass (kg)'] >= minPayload) & (spacex_df['Payload Mass (kg)'] <= maxPayload)
    payload_data=spacex_df[payloadRange]
    if sitedropdown != "All Launch Sites":
        scatter_data=payload_data[payload_data["Launch Site"]==sitedropdown]
        scatter_fig = px.scatter(scatter_data, x="Payload Mass (kg)", y="class",color="Booster Version Category")
    else:
        scatter_fig = px.scatter(payload_data, x="Payload Mass (kg)", y="class",color="Booster Version Category")
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server()