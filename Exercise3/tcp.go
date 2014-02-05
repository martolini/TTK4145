package main

import (
	"fmt"
	"net"
	"time"
)

func readMessage(conn *net.TCPConn) {
	buff := make([]byte, 1024)
	n, err := conn.Read(buff)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(buff[:n]))
}

func writeMessage(conn *net.TCPConn, message string) {
	message += "\000"

	n, err := conn.Write([]byte(message))
	if err != nil {
		fmt.Println(err, n)
		return
	}
}

func main() {
	addr, _ := net.ResolveTCPAddr("tcp", "129.241.187.161:33546")
	conn, err := net.DialTCP("tcp", nil, addr)
	if err != nil {
		fmt.Println("connect fail")
		return
	}
	defer conn.Close()

	// handle error
	// go func() {
	// 	for {
	// 		ln, err := net.Listen("tcp", ":30000")
	// 		conn, err := ln.Accept()
	// 		if err != nil {
	// 			fmt.Println(err)
	// 			return
	// 		}
	// 		var cmd []byte
	// 		fmt.Fscan(conn, &cmd)
	// 		fmt.Println("Message:", string(cmd))
	// 	}
	// }()
	readMessage(conn)
	time.Sleep(1 * time.Second)
	// writeMessage(conn, "Connect to: 78.91.28.51:30000")
	// time.Sleep(1 * time.Second)
	// writeMessage(conn, "MY MAN")
}
