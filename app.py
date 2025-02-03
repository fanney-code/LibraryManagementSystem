from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['libraryManagementSystem']

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Route to add a book
@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    quantity = int(request.form['quantity'])
    book = {
        'title': title,
        'author': author,
        'quantity': quantity
    }
    db.books.insert_one(book)
    return 'Book added successfully.'

# Route to search for a book
@app.route('/search_book', methods=['GET'])
def search_book():
    search_title = request.args.get('search_title')
    book = db.books.find_one({'title': search_title})
    if book:
        return f"Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}"
    else:
        return "Book not found."

# Route to borrow a book
@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    borrow_title = request.form['borrow_title']
    book = db.books.find_one({'title': borrow_title})
    if book and book['quantity'] > 0:
        db.books.update_one({'title': borrow_title}, {'$inc': {'quantity': -1}})
        return "Book borrowed successfully."
    elif book and book['quantity'] == 0:
        return "Book out of stock."
    else:
        return "Book not found."

# Route to return a book
@app.route('/return_book', methods=['POST'])
def return_book():
    return_title = request.form['return_title']
    book = db.books.find_one({'title': return_title})
    if book:
        db.books.update_one({'title': return_title}, {'$inc': {'quantity': 1}})
        return "Book returned successfully."
    else:
        return "Book not found."

# Route to display all books
@app.route('/display_all_books', methods=['GET'])
def display_all_books():
    books = db.books.find()
    return render_template('all_books.html', books=books)

if __name__ == "__main__":
    app.run(debug=True)
