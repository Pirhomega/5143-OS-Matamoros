package main

import (
	"fmt"
	"io"
	"os"
)

// PipeLine :
// Special version of the execute function which takes a list of Commands, then
// for each Command, sends it's output to a file and uses that file as the first
// arg of the next command.
func PipeLine(commands []Command) {

	// stdout backup
	stdout := os.Stdout
	// error variable
	var err error
	// Path to the pipe file (invisible files)
	inPipePath := " "
	outPipePath := "  "

	// For each command in the array
	for i, pipe := range commands {

		// If this isn't the last command
		if i < len(commands)-1 {
			// Before processing each command, open the file and redirect stdout
			os.Stdout, err = os.OpenFile(outPipePath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0755)
			if err != nil {
				os.Stdout = stdout
				fmt.Println("Error opening temp file: ", err)
				return
			}
		}

		// If the Command is valid
		if com, valid := ComMap[pipe.key]; valid {
			// If this isn't the first command
			if i > 0 {
				// Add the pipe file to the args (at the front)
				pipe.args = frAddStr(pipe.args, inPipePath)
			}
			// Execute the command with its arguments
			com(pipe.args)
		}

		// After processing each command, if this isn't the last command
		if i < len(commands)-1 {
			// Close the pipe file
			err = os.Stdout.Close()
			if err != nil {
				fmt.Println("Error closing temp file: ", err)
				return
			}
		}
		// After processing each command, restore stdout
		os.Stdout = stdout
		// Copy the output to the input file for the next command
		copyFrom(outPipePath, inPipePath)
	}
	// Remove the temporary files
	Rm([]string{inPipePath})
	Rm([]string{outPipePath})
}

// Add an item to the front of an array of strings
func frAddStr(argList []string, arg string) []string {
	argList = append(argList, "")
	copy(argList[1:], argList)
	argList[0] = arg
	return argList
}

// Copy a file from src to dest
// copy() borrowed from
// https://opensource.com/article/18/6/copying-files-go
func copyFrom(src, dst string) (int64, error) {
	sourceFileStat, err := os.Stat(src)
	if err != nil {
		return 0, err
	}

	if !sourceFileStat.Mode().IsRegular() {
		return 0, fmt.Errorf("%s is not a regular file", src)
	}

	source, err := os.Open(src)
	if err != nil {
		return 0, err
	}
	defer source.Close()

	destination, err := os.Create(dst)
	if err != nil {
		return 0, err
	}
	defer destination.Close()
	nBytes, err := io.Copy(destination, source)
	return nBytes, err
}
