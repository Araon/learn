package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {
	welcomeString := "Ticktokcer is running"
	fmt.Println(welcomeString)

	reader := bufio.NewReader(os.Stdin)
	fmt.Println("Do you want to know the time or date")

	// err ok syntax aka try-catch
	input, err := reader.ReadString('\n') // \n if the ender, how long you want to read
	if err != nil {
		fmt.Println(err)
	}

	userInput := strings.TrimSpace(input)
	dt := time.Now()
	if userInput == "date" {
		fmt.Printf("The current date is %s\n", dt.Format("01-02-2006"))
	} else if userInput == "time" {
		fmt.Printf("The current time is %s\n", dt.Format("15:00:00"))
	} else {
		fmt.Println("Incorrect input")
	}

}
