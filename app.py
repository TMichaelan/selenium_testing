from flask import Flask, render_template
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

def fetch_data():
    conn = sqlite3.connect('logs.db')
    query = "SELECT * FROM logs"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route('/')
def home():
    df = fetch_data()
    figs = {}
    for event in df['event'].unique():
        event_df = df[df['event'] == event]
        fig = px.line(event_df, x="date", y="loading_time", title=f"Loading time for {event}")
        figs[event] = pio.to_html(fig, full_html=False)
    return render_template('index.html', figures=figs)

if __name__ == "__main__":
    app.run(debug=True)