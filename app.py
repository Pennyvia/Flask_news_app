from flask import Flask, render_template
import os
import glob
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "clustered_outputs"

# Helper: Map category keys to actual CSV file paths
def get_categories():
    categories = {}
    for filepath in glob.glob(os.path.join(DATA_FOLDER, "*.csv")):
        filename = os.path.basename(filepath)
        name = os.path.splitext(filename)[0]  # e.g. Sports_cluster_1
        display = name.replace('_', ' ').title()
        categories[name] = {
            "display": display,
            "file": filename
        }
    return categories

@app.route('/')
def welcome():
    user_name = "Pennyvia M Kanengoni"
    reg_number = "R216896T"
    today = datetime.now().strftime("%B %d, %Y")
    return render_template('welcome.html', name=user_name, reg_number=reg_number, current_date=today)

@app.route('/categories')
def categories_page():
    categories = get_categories()
    return render_template('categories.html', categories=categories)

@app.route('/news/<category>')
def show_news(category):
    categories = get_categories()
    if category in categories:
        filename = categories[category]['file']
        file_path = os.path.join(DATA_FOLDER, filename)
        df = pd.read_csv(file_path)

        # Expect CSV to have 'title' and 'url' columns
        if 'title' in df.columns and 'url' in df.columns:
            news_items = df[['title', 'url']].dropna().to_dict('records')
        else:
            # If not structured correctly, fallback to plain list
            news_items = [{"title": row[0], "url": row[1]} for row in df.values if len(row) >= 2]

        return render_template('news.html', category=categories[category]['display'], news=news_items)
    else:
        return "Category not found", 404

if __name__ == '__main__':
    app.run(debug=True)
