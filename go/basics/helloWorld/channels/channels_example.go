package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

type Results struct {
	Index int
	Fact  string
	Err   error
}

func test(i int, wg *sync.WaitGroup, results chan<- Results) {
	defer wg.Done()
	resp, err := http.Get("https://catfact.ninja/fact")
	if err != nil {
		// fmt.Printf("Goroutine #%d: error: %v\n", i, err)
		results <- Results{i, "", err}
		return
	}
	defer resp.Body.Close()

	type CatFact struct {
		Fact string `json:"fact"`
	}

	var fact CatFact
	if err := json.NewDecoder(resp.Body).Decode(&fact); err != nil {
		// fmt.Printf("Goroutine #%d: error decoding response: %v\n", i, err)
		results <- Results{i, "", err}
		return
	}

	// fmt.Printf("CatFact #%d: %s\n", i, fact.Fact)
	results <- Results{i, fact.Fact, nil}
}

func main() {

	var wg sync.WaitGroup

	numGoroutines := 5
	wg.Add(numGoroutines)

	results := make(chan Results, numGoroutines)

	for i := 0; i < numGoroutines; i++ {
		go test(i, &wg, results)

	}

	wg.Wait()
	close(results)

	ordered := make([]Results, numGoroutines)
	for r := range results {
		ordered[r.Index] = r
	}

	for i := 0; i < numGoroutines; i++ {
		if ordered[i].Err != nil {
			fmt.Printf("Error %v\n", ordered[i].Err)
			continue
		}
		fmt.Printf("Catfact #%d: %s\n", i, ordered[i].Fact)
	}

	fmt.Println("Main function is running.")

}
