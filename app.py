from flask import Flask, render_template, request, redirect
import asyncpg

app = Flask(__name__)


#HOME 

@app.route('/')
def home():
    return render_template('home.html')


# SIGNUP 

@app.route('/signup', methods=['GET', 'POST'])
async def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = await asyncpg.connect(
            user='postgres',
            password='1234',
            database='library_db',
            host='localhost'
        )
        await conn.execute(
            '''
            INSERT INTO users(name,email,password)
            VALUES($1,$2,$3)
            ''',

            name,
            email,
            password
        )
        await conn.close()
        return redirect('/login')

    return render_template('signup.html')


# LOGIn

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = await asyncpg.connect(
            user='postgres',
            password='1234',
            database='library_db',
            host='localhost'
        )

        user = await conn.fetchrow(
            '''
            SELECT * FROM users
            WHERE email=$1 AND password=$2
            ''',
            email,
            password
        )

        await conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid Email or Password"
    return render_template('login.html')


#DASHBOARD 

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ADD BOOk

@app.route('/add_book', methods=['GET', 'POST'])
async def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        conn = await asyncpg.connect(
            user='postgres',
            password='1234',
            database='library_db',
            host='localhost'
        )

        await conn.execute(
            '''
            INSERT INTO books(title,author,category,quantity)
            VALUES($1,$2,$3,$4)
            ''',
            title,
            author,
            category,
            quantity
        )

        await conn.close()
        return "Book Added Successfully"

    return render_template('add_book.html')


#VIEW BOOKS

@app.route('/view_books')
async def view_books():
    conn = await asyncpg.connect(
        user='postgres',
        password='1234',
        database='library_db',
        host='localhost'
    )
    books = await conn.fetch(
        '''
        SELECT * FROM books
        '''
    )
    await conn.close()

    return render_template("view_books.html", books=books)

# ISSUE BOOK 

@app.route('/issue_book', methods=['GET', 'POST'])
async def issue_book():
    if request.method == 'POST':
        student_name = request.form['student_name']
        book_title = request.form['book_title']
        issue_date = request.form['issue_date']

        conn = await asyncpg.connect(
            user='postgres',
            password='1234',
            database='library_db',
            host='localhost'
        )
        await conn.execute(
            '''
            INSERT INTO issued_books(student_name,book_title,issue_date)
            VALUES($1,$2,$3)
            ''',
            student_name,
            book_title,
            issue_date
        )
        await conn.close()
        return "Book Issued Successfully"

    return render_template('issue_book.html')

# RETURN BOOK 

@app.route('/return_book', methods=['GET', 'POST'])
async def return_book():
    if request.method == 'POST':
        student_name = request.form['student_name']
        book_title = request.form['book_title']

        conn = await asyncpg.connect(
            user='postgres',
            password='1234',
            database='library_db',
            host='localhost'
        )

        await conn.execute(
            '''
            DELETE FROM issued_books
            WHERE student_name=$1
            AND book_title=$2
            ''',
            student_name,
            book_title
        )
        await conn.close()
        return "Book Returned Successfully"

    return render_template('return_book.html')


if __name__ == '__main__':
    app.run(debug=True)