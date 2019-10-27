import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import dash_core_components as dcc


db_connection_str = 'mysql+pymysql://root:"password"@localhost/craigslist'
db_connection = create_engine(db_connection_str)

df = pd.read_sql('SELECT * FROM books_mags', con=db_connection).drop(['id'], axis=1)
df[' index'] = range(1, len(df) + 1)

app = dash.Dash(__name__)
server = app.server
PAGE_SIZE = 5
app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-filtering-fe',
        columns=[
            {"name": i, "id": i, "deletable": True} for i in df.columns
        ],
        style_cell_conditional=[
        {'if': {'column_id': 'titles'},
         'width': '30%'}],
        data=df.to_dict('records'),
        filter_action="native",
        page_size=PAGE_SIZE
    ),
    html.Div(id='datatable-filter-container')
])


@app.callback(
    Output('datatable-filter-container', "children"),
    [Input('datatable-filtering-fe', "data")])
def update_graph(rows):
    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)

    return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)

    

#References 
#https://dash.plot.ly/datatable/callbacks
#https://dash.plot.ly/datatable/filtering
