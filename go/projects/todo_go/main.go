package main

import (
	"database/sql"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	_ "modernc.org/sqlite"
)

type todo struct {
	ID         string `json:"id"`
	Task       string `json:"task" binding:"required"`
	Status     string `json:"status"`
	Start_date string `json:"start_date"`
	End_date   string `json:"end_date"`
}

var db *sql.DB

func initDB() error {
	var err error
	db, err = sql.Open("sqlite", "./todos.db")

	if err != nil {
		return err
	}

	_, err = db.Exec(`
    CREATE TABLE IF NOT EXISTS todos (
        id TEXT PRIMARY KEY,
        task TEXT NOT NULL,
        status TEXT,
        start_date TEXT,
        end_date TEXT
        )
    `)
	return err
}

var todos = []todo{}

func main() {
	if err := initDB(); err != nil {
		panic(err)
	}

	router := gin.Default()

	router.Use(RequestIDMiddleware())
	router.GET("/todos", getTodos)
	router.POST("/todos", postTodos)

	router.Run("localhost:8080")
}

func getTodos(c *gin.Context) {

	requestID, _ := c.Get("request_id")

	println("Request ID:", requestID.(string))

	rows, err := db.Query("SELECT id, task, status, start_date, end_date FROM todos")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	defer rows.Close()

	var todos []todo
	for rows.Next() {
		var t todo
		if err := rows.Scan(&t.ID, &t.Task, &t.Status, &t.Start_date, &t.End_date); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		todos = append(todos, t)
	}
	c.IndentedJSON(http.StatusOK, todos)
}

func postTodos(c *gin.Context) {
	requestID, _ := c.Get("request_id")

	println("Request ID:", requestID.(string))
	var newTodo todo
	if err := c.BindJSON(&newTodo); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	newTodo.ID = uuid.New().String()
	var start time.Time
	var err error
	if newTodo.Start_date == "" {
		start = time.Now()
	} else {
		start, err = time.Parse("2006-01-02", newTodo.Start_date)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid start_date format (YYYY-MM-DD)"})
			return
		}
	}
	var end time.Time
	if newTodo.End_date == "" {
		end = start.Add(24 * time.Hour)
	} else {
		end, err = time.Parse("2006-01-02", newTodo.End_date)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "end_date cannot be before start_date"})
			return
		}
	}
	newTodo.Start_date = start.Format("2006-01-02")
	newTodo.End_date = end.Format("2006-01-02")
	_, err = db.Exec(
		"INSERT INTO todos (id, task, status, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
		newTodo.ID, newTodo.Task, newTodo.Status, newTodo.Start_date, newTodo.End_date,
	)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusCreated, newTodo)
}

func RequestIDMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {

		requestID := c.GetHeader("X-Request-ID")

		if requestID == "" {
			requestID = uuid.New().String()
		}

		c.Set("request_id", requestID)

		c.Writer.Header().Set("X-Request-ID", requestID)

		c.Next()
	}
}
