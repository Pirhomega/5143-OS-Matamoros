// +build windows

package main

import (
	"fmt"
	"os"
	"syscall"
)

func init(){
    // Add this command's function to the command mapping
    ComMap["mkdir"] = Mkdir
}

// Mkdir makes a new directory. Currently, the only supported functionality
// includes making a folder in the current directory with a folder name
// supplied by the user as the first argument.
// Example: % mkdir test
// Result: This command would make a new folder called test in the current
// working directory.
func Mkdir(args []string) {
	// Get the current working directory
	path, err := os.Getwd()

	if err != nil {
		fmt.Println("Failed to get current working directory.")
	}

	// Check for a folder name
	if len(args) == 0 {
		fmt.Println("Error: No folder name included.")
	} else {
		// The folder name should be argument 0
		folderName := args[0]
		// Construct absolute path
		totalPath := path + "\\" + folderName

		// Print path for testing
		fmt.Println(totalPath)

		// Convert string totalPath to a *uint16
		totalPathPtr := syscall.StringToUTF16Ptr(totalPath)
		// Make the directory using the Windows CreateDirectory system call
		errPath := syscall.CreateDirectory(totalPathPtr, nil)

		if errPath == syscall.ERROR_ALREADY_EXISTS {
			fmt.Println("Directory already exists.")
		} else if errPath == syscall.ERROR_PATH_NOT_FOUND {
			fmt.Println("Failed to create directory. One or more intermediate directories do not exist.")
		}
	}
}
