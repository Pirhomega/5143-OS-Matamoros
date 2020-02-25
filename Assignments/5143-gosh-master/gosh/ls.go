package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"time"
)

func init() {
	// Add this command's function to the command mapping
	ComMap["ls"] = Ls
}

// Ls lists all files and directories in a specified folder. Currently, no
// flags are supported.
func Ls(args []string) {
	argList, flags := ArgSplitter(args)
	var path string = ""

	// ReadDir reads the directory named by dirname and returns a list of
	// directory entries sorted by filename. The entries are a FileInfo
	// object with the following format:
	/*
			type FileInfo interface {
		    	Name() string       // base name of the file
		    	Size() int64        // length in bytes for regular files; system-dependent for others
		    	Mode() FileMode     // file mode bits
		    	ModTime() time.Time // modification time
		    	IsDir() bool        // abbreviation for Mode().IsDir()
				Sys() interface{}   // underlying data source (can return nil)
			}
	*/

	// If no arguments, list all file and folder names only
	if len(argList) == 0 && len(flags) == 0 {
		defaultPrint(".")
	} else if len(argList) > 0 && len(flags) == 0 {
		// Different path than current working directory, no flags passed
		path = BuildPathToDir(argList[0])
		defaultPrint(path)
	} else if len(argList) == 0 && len(flags) > 0 {
		// Long print of current working directory
		// Parse a flag or two
		lFlag, hFlag := parseFlags(flags)

		if lFlag == true && hFlag == false {
			// If long listing, not human readable
			longPrint(".", false)
		} else if lFlag == true && hFlag == true {
			// If long listing, human readable
			longPrint(".", true)
		}
	} else if len(argList) > 0 && len(flags) > 0 {
		// Different path with flags, build path to directory
		path = BuildPathToDir(argList[0])

		// Find which flags are present (returns a boolean for each flag)
		lFlag, hFlag := parseFlags(flags)

		// Long listing, not human readable
		if lFlag == true && hFlag == false {
			longPrint(path, false)
		} else if lFlag == true && hFlag == true {
			// Long listing, human readable
			longPrint(path, true)
		} else {
			// You don't know what you want, you get a long listing
			// and you will like it.
			longPrint(path, false)
		}
	}
}

// parseFlags checks for -l and -h
func parseFlags(flags []string) (bool, bool) {
	lFlag := false
	hFlag := false
	// Loop through flag array
	for _, v := range flags {
		if v == "l" {
			lFlag = true
		}
		if v == "h" {
			hFlag = true
		}
	}
	return lFlag, hFlag
}

// defaultPrint is the vanilla ice cream of prints. It lists files
// and directories.
func defaultPrint(path string) {
	files, err := ioutil.ReadDir(path)
	if err != nil {
		fmt.Println(err)
	}
	for _, file := range files {
		fmt.Printf(file.Name() + " ")
	}
	fmt.Printf("\n")
}

// longPrint prints a long listing. If the second argument is true, a long
// listing is printed with sizes in human-readable format.
func longPrint(path string, human bool) {
	files, _ := ioutil.ReadDir(path)

	// Long listing, not human readable
	if human == false {
		for _, file := range files {
			// Print permissions
			fmt.Printf("%s ", file.Mode())
			// Print owner fields
			// This is not implemented as Windows returns -1 for
			// the group and owner fields
			// Print size
			fmt.Printf("%12d ", file.Size())
			// Print date
			t := file.ModTime()
			fmt.Printf("%v ", t.Format(time.UnixDate))
			// Print file/folder name
			fmt.Printf(file.Name() + " ")
			fmt.Printf("\n")
		}
	} else {
		// Long listing, human readable
		for _, file := range files {
			// Print permissions
			fmt.Printf("%s ", file.Mode())

			// Print owner fields
			// This is not implemented as Windows returns -1 for
			// the group and owner fields

			// Convert file size format
			formatSize := divide(file.Size())
			// Print size
			fmt.Printf("%6s ", formatSize)

			// Print date
			t := file.ModTime()
			fmt.Printf("%v ", t.Format(time.UnixDate))
			// Print file/folder name
			fmt.Printf(file.Name() + " ")
			fmt.Printf("\n")
		}
	}
}

// divide finds the number of divisions needed to get a file size below
// 1024. Example: if a file size in bytes takes 3 divisions to get below 1024,
// the file is 1 or more gigabytes. The returned string is formatted with some
// order of magnitude (ex: 1GB)
func divide(size int64) string {
	count := 0
	for size > 1024 {
		size /= 1024
		count++
	}

	// Convert size to a string
	fSize := strconv.Itoa(int(size))

	switch count {
	case 0:
		fSize += "B"
	case 1:
		fSize += "KB"
	case 2:
		fSize += "MB"
	case 3:
		fSize += "GB"
	case 4:
		fSize += "TB"
	case 5:
		fSize += "PB"
	}

	return fSize
}
