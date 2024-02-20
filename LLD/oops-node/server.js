const express = require('express')
const bodyParser = require('body-parser')

const Book = require('./book')

const app = express();
const port = 3000;

app.use(bodyParser.json());

let books = [
    new Book(1, 'Book 1', 'Author 1'),
    new Book(2, 'Book 2', 'Author 2')
];

//read all books

// Read all books
app.get('/books', (req, res) => {
    res.json(books);
});

// Read a specific book
app.get('/books/:id', (req, res) => {
    const bookId = parseInt(req.params.id);
    const book = books.find(b => b.id === bookId);

    if (book) {
        res.json(book);
    } else {
        res.status(404).json({ error: 'Book not found' });
    }
});
//create book
app.post('/books', (req, res) => {
    const { title, author } = req.body;
    const newBook = new Book(books.length + 1, title, author);
    books.push(newBook);
    res.json(newBook);
});


//update book
app.put('/books/:id', (req, res) => {
    const bookId = parseInt(req.params.id);
    const bookIndex = books.findIndex(b => b.id === bookId);

    if (bookIndex !== -1) {
        const { title, author } = req.body;
        books[bookIndex] = new Book(bookId, title, author);
        res.json(books[bookIndex]);
    } else {
        res.status(404).json({ error: 'Book not found' });
    }
});

//delete a book
app.delete('/books/:id', (req, res) => {
    const bookId = parseInt(req.params.id);
    books = books.filter(b => b.id !== bookId);
    res.json({ message: 'Book deleted successfully' });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});