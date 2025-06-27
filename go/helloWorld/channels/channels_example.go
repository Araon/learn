package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

func test(i int, wg *sync.WaitGroup) {
	defer wg.Done()
	resp, err := http.Get("https://catfact.ninja/fact")
	if err != nil {
		fmt.Printf("Goroutine #%d: error: %v\n", i, err)
		return
	}
	defer resp.Body.Close()
	type CatFact struct {
		Fact   string `json:"fact"`
		Length int    `json:"length"`
	}

	var fact CatFact
	if err := json.NewDecoder(resp.Body).Decode(&fact); err != nil {
		fmt.Printf("Goroutine #%d: error decoding response: %v\n", i, err)
		return
	}

	fmt.Printf("CatFact #%d: %s\n", i, fact.Fact)
}

func main() {

	var wg sync.WaitGroup

	numGoroutines := 5

	wg.Add(numGoroutines)
	for i := 0; i < numGoroutines; i++ {
		go test(i, &wg)

	}

	wg.Wait()

	fmt.Println("Main function is running.")

}
