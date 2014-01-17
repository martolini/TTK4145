package main

import (
	. "fmt"
	. "runtime"
	. "time"
)

var i = 0

func adder() {
	for x := 0; x < 100000; x++ {
		i++
	}
}

func decrease() {
	for x := 0; x < 100000; x++ {
		i--
	}
}

func main() {
	GOMAXPROCS(NumCPU()) // I guess this is a hint to what GOMAXPROCS does...
	go adder()           // This spawns adder() as a goroutine
	go decrease()
	// No way to wait for the completion of a goroutine (without additional syncronization)
	// We'll come back to using channels in Exercise 2. For now: Sleep
	Sleep(100 * Millisecond)
	Println("Done:", i)
}
