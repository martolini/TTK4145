package main

import (
	. "fmt"
	. "runtime"
	. "sync"
)

func increment(c chan int, wg *WaitGroup) {
	for x := 0; x < 10; x++ {
		a := <-c
		a++
		c <- a
	}
	defer wg.Done()
}

func decrement(c chan int, wg *WaitGroup) {
	for x := 0; x < 11; x++ {
		a := <-c
		a--
		c <- a
	}
	defer wg.Done()
}

func main() {
	var wg WaitGroup
	GOMAXPROCS(NumCPU())
	c := make(chan int, 2)
	c <- 0
	wg.Add(1)
	go increment(c, &wg)
	wg.Add(1)
	go decrement(c, &wg)
	wg.Wait()
	Println(<-c)
}
