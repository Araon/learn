require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const Book = require('./book');
const InMemoryStorage = require('./InMemoryStorage');
const RedisStorage = require('./RedisStorage');

const app = express();
const port = 3000;

app.use(bodyParser.json());

// use InMemoryStorage Strategy by default
let bookStorage;

if (process.env.NODE_ENV === 'production') {
    bookStorage = new RedisStorage();
} else {
    bookStorage = new InMemoryStorage();
}

// read all books
app.get('/ping', async (req, res) => {
    res.status(200).json({ Ping: 'Pong' });
});

// Read all books
app.get('/books', async (req, res) => {
    try {
        const books = await bookStorage.getAllBooks();
        res.json(books);
    } catch (err) {
        console.error('Error retrieving books:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Read a specific book
app.get('/books/:id', async (req, res) => {
    const bookId = req.params.id;

    try {
        const book = await bookStorage.getBookById(bookId);

        if (book) {
            res.json(book);
        } else {
            res.status(404).json({ error: 'Book not found' });
        }
    } catch (err) {
        console.error('Error retrieving book:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// create book
app.post('/books', async (req, res) => {
    const { title, author } = req.body;
    const newBook = new Book(uuidv4().substring(0, 6), title, author);

    try {
        await bookStorage.addBook(newBook);
        res.json(newBook);
    } catch (err) {
        console.error('Error adding book:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// update book
app.put('/books/:id', async (req, res) => {
    const bookId = req.params.id;
    const { title, author } = req.body;
    const updatedBook = new Book(bookId, title, author);

    try {
        await bookStorage.updateBook(bookId, updatedBook);
        res.json(updatedBook);
    } catch (err) {
        console.error('Error updating book:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// delete a book
app.delete('/books/:id', async (req, res) => {
    const bookId = req.params.id;

    try {
        const result = await bookStorage.deleteBook(bookId);

        if (result) {
            res.json({ message: 'Book deleted successfully' });
        } else {
            res.status(404).json({ error: 'Book not found' });
        }
    } catch (err) {
        console.error('Error deleting book:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
