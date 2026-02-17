package main

import "fmt"

func main() {
	i := 1

	for i <= 3 {
		fmt.Println(i)
		i += 1
	}

	for j := 0; j <= 3; j++ {
		fmt.Println(j)
	}

	for i := range [3]int{} {
		fmt.Println("range: ", i)
	}
}
