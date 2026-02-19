package main

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type todo struct {
	ID         string `json:"id"`
	Task       string `json:"task" binding:"required"`
	Status     string `json:"status"`
	Start_date string `json:"start_date"`
	End_date   string `json:"end_date"`
}

var todos = []todo{}

func main() {
	router := gin.Default()

	router.Use(RequestIDMiddleware())
	router.GET("/todos", getTodos)
	router.POST("/todos", postTodos)

	router.Run("localhost:8080")
}

func getTodos(c *gin.Context) {

	requestID, _ := c.Get("request_id")

	println("Request ID:", requestID.(string))
	c.IndentedJSON(http.StatusOK, todos)
}

func postTodos(c *gin.Context) {
	var newTodo todo

	if err := c.BindJSON(&newTodo); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	requestID, _ := c.Get("request_id")

	println("Request ID:", requestID.(string))

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

	// adding the todo to memory
	todos = append(todos, newTodo)
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
