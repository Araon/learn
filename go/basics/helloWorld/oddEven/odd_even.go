package main

import "fmt"

/*
Write a program
that prints odd and even numbers using go routines
how would i use channels and go functions here?
*/

func sendNumbers(n int, out chan<- int) {
	for i := 0; i <= n; i++ {
		out <- i
	}
	close(out)
}

func printEven(in <-chan int, done chan<- struct{}) {
	for x := range in {
		if x%2 == 0 {
			fmt.Printf("Even: %d\n", x)
		}
	}
	done <- struct{}{}
}

func printOdd(in <-chan int, done chan<- struct{}) {
	for x := range in {
		if x%2 != 0 {
			fmt.Printf("Odd: %d\n", x)
		}
	}
	done <- struct{}{}
}

func main() {
	nums := make(chan int)
	done := make(chan struct{}, 2)

	go printEven(nums, done)
	go printOdd(nums, done)

	sendNumbers(10, nums)

	<-done
	<-done

}
