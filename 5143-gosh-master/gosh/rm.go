package main

import (
	"fmt"
	"os"
)

func init(){
    // Add this command's function to the command mapping
    ComMap["rm"] = Rm
}

// Rm removes a folder or file
func Rm(args []string) {
	if len(args) != 0 {
		rmMe := args[0]
		err := os.Remove(rmMe)
		if err != nil {
			fmt.Printf("%v\n", err)
		}
	}
}
