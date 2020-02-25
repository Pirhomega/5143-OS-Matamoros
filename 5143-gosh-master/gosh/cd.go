package main

import (
	"fmt"
	"os"
)

func init() {
	// Add this command's function to the command mapping
	ComMap["cd"] = Cd
}

// Cd changes directories
func Cd(args []string) {
	// There should only be one argument
	if len(args) == 1 {
		// Try to change directory
		err := os.Chdir(args[0])
		if err != nil {
			fmt.Printf("%v\n", err)
		}
	}
}
