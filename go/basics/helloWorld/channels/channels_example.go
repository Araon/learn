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
		results <- Results{i, "", err}
		return
	}
	defer resp.Body.Close()

	type CatFact struct {
		Fact string `json:"fact"`
	}

	var fact CatFact
	if err := json.NewDecoder(resp.Body).Decode(&fact); err != nil {
		results <- Results{i, "", err}
		return
	}

	results <- Results{i, fact.Fact, nil}
}

func main() {

	var wg sync.WaitGroup

	numGoroutines := 5
	wg.Add(numGoroutines)

	results := make(chan Results, numGoroutines)

	for i := range numGoroutines {
		go test(i, &wg, results)
	}

	wg.Wait()
	close(results)

	ordered := make([]Results, numGoroutines)
	for r := range results {
		ordered[r.Index] = r
	}

	for i := range numGoroutines {
		if ordered[i].Err != nil {
			fmt.Printf("Error %v\n", ordered[i].Err)
			continue
		}
		fmt.Printf("\nCatfact #%d: %s\n", i, ordered[i].Fact)

	}

	fmt.Println("\nMain function is running.")

}
