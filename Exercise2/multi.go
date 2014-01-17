package main

import (
	. "fmt"
	. "runtime"
)

func increment(c chan int) {
	for x := 0; x < 10; x++ {
		a := <-c
		a++
		c <- a
	}
}

func decrement(c chan int) {
	for x := 0; x < 10; x++ {
		a := <-c
		a--
		c <- a
	}
}

func main() {
	GOMAXPROCS(NumCPU())
	c := make(chan int)
	go increment(c)
	go decrement(c)
	Println(<-c)
}
