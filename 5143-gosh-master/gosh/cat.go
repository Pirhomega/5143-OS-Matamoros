package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
)

//these flags will be set off if a > or >> are included in the Cat command
var (
	single, double bool = false, false

	// scanner pointer that will point to a file to be read from
	scanner *bufio.Scanner

	// this string will save the path of the file to which output will be redirected when > or >> are used
	// and ctext will hold strings typed into standard in when 'cat' is called with no arguments
	outputPath, ctext string
)

func init() {
	// Add this command's function to the command mapping
	ComMap["cat"] = Cat
}

// Cat will either concatenate a file and print it to std out or
// intake two or more files and print them as if they were concatenated.
// One could also redirect the output to a file using either '>' or '>>'.
// If Cat was called without any arguments, it will take input from Stdin
// and just output it to Stdout. Currently, you can not execute "cat > outfile"
// Usage:
//			cat
// 			cat file
// 			cat file1 file2 fileN
//			cat file1 file2 fileN (> || >>) outfile
func Cat(args []string) {
	//base case, where there are no arguments to the command
	//read from Stdin and output straight to Stdout until a
	//'q' is typed
	if len(args) == 0 {
		reader := bufio.NewReader(os.Stdin)
		for ctext != "q\r\n" {
			ctext, _ = reader.ReadString('\n')
			fmt.Println(ctext)
		}
		//if cat has arguments, create a temporary file. We will use this to 
		//store contents of the input files.
	} else {
		tempFile, err := os.Create("temp.txt")
		if err != nil {
			log.Fatal(err)
		}
	mainLoop: //this is a label which I use to identify the following for loop
		for element := range args {
			switch args[element] {
			//redirect to a file, erasing file's existing data if any existed
			case ">":
				single = true
				outputPath = args[element+1] //remember the path of the redirected output file
				break mainLoop               //kill the loop, not the switch (which is what it would do if the instruction was just "break")
			//append output to a file
			case ">>":
				double = true
				outputPath = args[element+1]
				break mainLoop
			//otherwise, it's an input file, which we will open and copy it's contents to the temp file
			default:
				file, _ := os.Open(args[element]) //open the file
				scanner = bufio.NewScanner(file)  //create a scanner to run through the file
				scanner.Split(bufio.ScanLines)    //set delimiter to lines, meaning the scanner will read in one line at a time
				for scanner.Scan() {              //run through the file and print each line to the stdout
					tempFile.WriteString(scanner.Text() + "\n") //write to the temp file
				}
				file.Close()
			}
		}
		tempFile.Seek(0, io.SeekStart) //return scanner to the top of tempFile
		scanner = bufio.NewScanner(tempFile)
		scanner.Split(bufio.ScanLines)
		if single == true {
			//opens the read-write file and truncates if successful. Otherwise, it creates the file with read-write permissions
			outfile, _ := os.OpenFile(outputPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0755)
			for scanner.Scan() {
				outfile.WriteString(scanner.Text() + "\n") // transfer contents of tempFile to outfile
			}
			outfile.Close()
		} else if double == true {
			//opens the read-write file for appending. Otherwise, it creates the file with read-write permissions
			outfile, _ := os.OpenFile(outputPath, os.O_RDWR|os.O_CREATE, 0666)
			outfile.Seek(0, io.SeekEnd) //point at the end of outfile so we can start appending properly
			for scanner.Scan() {
				outfile.WriteString("\n" + scanner.Text()) // output contents of tempFile to outfile
			}
			outfile.Close()
			// if no redirection flags were set, print all contents of the tempfile to Stdout
		} else {
			// print the contents of tempFile to stdout
			for scanner.Scan() {
				fmt.Println(scanner.Text())
				if err != nil {
					log.Fatal(err)
				}
			}
		}
		//close and delete the temporary file
		tempFile.Close()
		err = os.Remove("temp.txt")
		if err != nil {
			log.Fatal(err)
		}
	}
}
