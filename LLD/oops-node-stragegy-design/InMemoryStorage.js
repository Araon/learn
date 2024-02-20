class InMemeoryStorage {
    constructor() {
        this.books = []
        console.log('Using InMemeory Storage')
    }

    getAllBooks() {
        return this.books;
    }

    getBookById(id) {
        return this.books.find(book => book.id === id);
    }

    addBook(book) {
        this.books.push(book);
        return book;
    }

    updateBook(id, updatedBook) {
        const index = this.books.findIndex(book => book.id === id);
        if (index !== -1) {
            this.book[index] = updatedBook;
            return updatedBook;
        }
        return null;
    }

    deleteBook(id) {
        this.books = this.books.filter(book => book.id !== id);
    }
}

module.exports = InMemeoryStorage;