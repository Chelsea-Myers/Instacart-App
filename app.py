from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'instacart_sample.csv' 
df = pd.read_csv(file_path)

# Set up day of the week as a text feature
dow_to_name = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
}

# Group data to find number of orders per day
avg_orders_per_day = df.groupby('order_dow')['order_id'].nunique().reset_index()
avg_orders_per_day.columns = ['order_dow', 'Average Number of Orders']
avg_orders_per_day['Day of the Week'] = avg_orders_per_day['order_dow'].map(dow_to_name)
avg_orders_per_day.sort_values(by='order_dow', inplace=True)

#Format data for data table
avg_orders_per_day_toprint = avg_orders_per_day[['Day of the Week', 'Average Number of Orders']]

# Group data to find number of orders per hour
avg_orders_per_hour = df.groupby('order_hour_of_day')['order_id'].nunique().reset_index()
avg_orders_per_hour.columns = ['Hour of the Day', 'Average Number of Orders']
avg_orders_per_hour.sort_values(by='Hour of the Day', inplace=True)

#Format data for data table
avg_orders_per_day_toprint = avg_orders_per_day[['Day of the Week', 'Average Number of Orders']]


# Initialize the Dash app
app = Dash(__name__)

server = app.server

# App layout
app.layout = [
    html.H1(children='Instacart Dashboard'),
    dcc.RadioItems(
            id='radio-options',
            options=[
                    {'label': 'Day of the Week', 'value': 'Day of the Week'},
                    {'label': 'Hour of the Day', 'value': 'Hour of the Day'}
            ],
            value='Day of the Week',
            labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='orders-graph')
    ]

@app.callback(
    Output('orders-graph', 'figure'),
    [Input('radio-options', 'value')]
)

def update_graph(selected_option):
    if selected_option == 'Day of the Week':

        fig=px.bar(avg_orders_per_day,
                x="Day of the Week",
                y='Average Number of Orders',
                title='Average Number of Orders Per Day')
    else:

        fig=px.bar(avg_orders_per_hour,
                x="Hour of the Day",
                y='Average Number of Orders',
                title='Average Number of Orders Per Day')
        
    return fig

    
#Run the app
if __name__ == '__main__':
    app.run(debug=True)
