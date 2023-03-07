package main

import (
	"errors"
	"fmt"
	"net/http"
	"os"
)

func getRoot(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("got %s request\n", r.URL.Path)

	p := "." + r.URL.Path
	if p == "./" {
		p = "./static/page/index.html"
	}

	http.ServeFile(w, r, p)
}

func main() {
	http.HandleFunc("/", getRoot)

	fmt.Printf("Started server on http://localhost:%d", 3333)
	err := http.ListenAndServe(":3333", nil)

	if errors.Is(err, http.ErrServerClosed) {
		fmt.Printf("server closed\n")
	} else if err != nil {
		fmt.Printf("error starting server: %s\n", err)
		os.Exit(1)
	}
}
