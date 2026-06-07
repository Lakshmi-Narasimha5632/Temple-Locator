from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Database Connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root123",
    database="temple_locator",
    cursorclass=pymysql.cursors.DictCursor
)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# Search Temples
@app.route('/search')
def search():

    search_term = request.args.get('search')

    cursor = connection.cursor()

    query = """
    SELECT id,
           temple_name,
           city,
           area
    FROM temples3
    WHERE temple_name LIKE %s
       OR city LIKE %s
       OR area LIKE %s
       OR description LIKE %s
    """

    search_pattern = f"%{search_term}%"

    cursor.execute(
        query,
        (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )
    )

    temples = cursor.fetchall()

    return render_template(
        'results.html',
        temples=temples,
        search_term=search_term
    )


# Temple Details Page
@app.route('/temple/<int:id>')
def temple_details(id):

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM temples3
    WHERE id=%s
    """

    cursor.execute(query, (id,))
    temple = cursor.fetchone()

    return render_template(
        'temple_details.html',
        temple=temple
    )


if __name__ == "__main__":
    app.run(debug=True)