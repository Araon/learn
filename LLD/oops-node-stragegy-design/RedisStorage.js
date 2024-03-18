const redis = require('redis');
const { promisify } = require('util');
const client = redis.createClient({
    host: 'localhost', // Docker container's IP or hostname
    port: 6379,
});

const hgetallAsync = promisify(client.hgetall).bind(client);
const hgetAsync = promisify(client.hget).bind(client);
const hsetAsync = promisify(client.hset).bind(client);
const hdelAsync = promisify(client.hdel).bind(client);
const quitAsync = promisify(client.quit).bind(client);

class RedisStorage {

    constructor() {
        this.connected = false;
        console.log('Using redis Storage');
        client.on('ready', () => {
            this.connected = true;
            console.log(`Connected to Redis on port ${client.options.port}.`);
        });

        client.on('error', (err) => {
            this.connected = false;
            console.error('Error connecting to Redis:', err);
        });

    }

    async getAllBooks() {
        try {
            const data = await hgetallAsync('books');

            if (data === null) {
                console.error('No data found for books.');
                return [];
            } else {
                const books = Object.values(data).map(JSON.parse);
                return books;
            }
        } catch (err) {
            throw err;
        }
    }

    async getBookById(id) {
        try {
            const data = await hgetAsync('books', id);
            const book = data ? JSON.parse(data) : null;
            return book;
        } catch (err) {
            throw err;
        }
    }

    async addBook(book) {
        try {
            await hsetAsync('books', book.id, JSON.stringify(book));
        } catch (err) {
            throw err;
        }
    }

    async updateBook(id, updatedBook) {
        try {
            await hsetAsync('books', id, JSON.stringify(updatedBook));
        } catch (err) {
            throw err;
        }
    }

    async deleteBook(id) {
        try {
            const result = await hdelAsync('books', id);
            return result === 1; // Return true if the book was deleted, false otherwise
        } catch (err) {
            throw err;
        }
    }

    async close() {
        try {
            await quitAsync();
            console.log('Redis client closed successfully.');
        } catch (err) {
            console.error('Error closing Redis client:', err);
        }
    }
}

module.exports = RedisStorage;
