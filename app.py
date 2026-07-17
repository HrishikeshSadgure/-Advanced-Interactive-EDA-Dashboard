from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import plotly.express as px
import io
import os

app = Flask(__name__)
df = None  # To store uploaded dataframe globally (basic approach)

@app.route('/', methods=['GET', 'POST'])
def index():
    global df
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            return redirect('/preview')
    return render_template('index.html')

@app.route('/preview')
def preview():
    global df
    if df is not None:
        return render_template('preview.html', tables=[df.head(50).to_html(classes='data')], titles=df.columns.values)
    return redirect('/')

@app.route('/univariate', methods=['GET', 'POST'])
def univariate():
    global df
    plot_div = ""
    column = None

    if df is not None:
        if request.method == 'POST':
            column = request.form['column']
            if pd.api.types.is_numeric_dtype(df[column]):
                fig = px.histogram(df, x=column, nbins=30, marginal='box', title=f"Distribution of {column}")
            else:
                vc = df[column].value_counts().reset_index()
                vc.columns = [column, 'count']
                fig = px.bar(vc, x=column, y='count', title=f"Category Counts for {column}")
            plot_div = fig.to_html(full_html=False)

    return render_template('univariate.html', columns=df.columns if df is not None else [], plot_div=plot_div, selected_col=column)

if __name__ == '__main__':
    app.run(debug=True)
