package main

import (
	"bufio"
	"fmt"
	"os"
	"runtime"
	"strings"
)

var (
	// list that will hold all commands typed in the terminal
	commandList []string

	// tmpfile will hold a command queried by the "!" character.
	// oldStdin will remember the traditional Stdin when it is
	// switched to tmpfile (see 'exclamation.go').
	// Checker is a flag that will "activate" code in 'getInput()'
	// to run if "!" is used.
	tmpfile  *os.File
	oldStdin *os.File = os.Stdin
	checker  bool     = false

	// saves the position in commandHistory list where this session's
	// commands start. That way, when the shell closes, we only copy this
	// session's commands to the history file.
	whereLeftOff int

	// ComMap with be used to create a map of strings (command keys) to Commands (the functions)
	ComMap = make(map[string]CommandFunc)
)

type (
	// CommandFunc will be used to treat functions of the given format as a type "Command"
	CommandFunc func(args []string)

	// Command : A command grouped with arguments for calling it
	Command struct {
		key  string
		args []string
	}
)

func main() {
	// loads the command history file contents from gosh_history.tmp into RAM
	loadHistory()
	// Main loop
	for {
		// Print prompt
		// The double percent sign must be used to print a literal percent sign
		fmt.Printf("%% ")
		// Get the user's input
		input := getInput()
		// loads a command into commandList array
		commandList = append(commandList, input)
		// Split the input by instances of && (multiple commands to run)
		commandLines := strings.Split(input, "&&")
		// Run each command line
		for _, line := range commandLines {
			// Split each line of input by pipes if necessary
			piping := strings.Split(line, "|")
			// If there is any piping, we'll need to make a Command list
			if len(piping) > 1 {
				var pipe []Command
				for _, command := range piping {
					pipe = append(pipe, parseCommand(command))
				}
				PipeLine(pipe)
			} else {
				// If there is no piping, we just need to run the command
				// Get the command from the line of text
				command := parseCommand(line)
				// Standardize command
				command.key = strings.ToLower(command.key)
				// Execute the command in the standard way
				execute(command)
			}
		}
	}
}

// loads the contents of gosh_history.tmp into the commandList array
func loadHistory() {
	// open the gosh_history file for reading
	historyFile, _ := os.OpenFile("gosh_history.tmp", os.O_RDONLY | os.O_CREATE | os.O_APPEND, 0755)
	scanner := bufio.NewScanner(historyFile)
	for scanner.Scan() {
		// append the command from the gosh_history.tmp and remove the
		// \n
		commandList = append(commandList, strings.TrimRight(scanner.Text(), "\n"))
	}
	historyFile.Close()
	// remember where the commands for this current session begin
	whereLeftOff = len(commandList)
}

func getInput() string {
	var (
		// line will hold the command
		// e will hold any error messages for us to ignore
		line string
		e    error
	)
	// If checker is true, it means the exclamation command was run, so we need
	// to run the command it saved to its temporary file. Therefore,
	// temporarily change Stdin to the temporary file created in exclamation.go,
	// read in its contents, and execute the result
	if checker {
		checker = false
		//switch to the new Stdin - the temporary file
		os.Stdin = tmpfile
	}
	// Create a keyboard reader, which will either read from the keyboard
	// or from the temporary file created in the exclamation.go
	keyboard := bufio.NewReader(os.Stdin)
	// Read a line of input from Stdin until carriage return
	line, e = keyboard.ReadString('\n')
	// if Stdin was changed, switch back to the original Stdin
	// if it wasn't changed, oh well. Doing it this way makes for a cleaner
	//code
	os.Stdin = oldStdin
	// Print out any errors
	if e != nil {
		fmt.Println("ooga")
		fmt.Fprintln(os.Stderr, e)
	}

	// Trim \r\n for Windows
	if runtime.GOOS == "windows" {
		line = strings.TrimRight(line, "\r\n")
	} else {
		line = strings.TrimRight(line, "\n")
	}

	return line
}

func parseCommand(line string) Command {
	// Trim any leading and trailing spaces resulting from '&&' or '|' splits
	// This has to be done to process multiple commands. It just does.
	line = strings.TrimLeft(line, " ")
	line = strings.TrimRight(line, " ")
	// Separate the arguments
	symbols := strings.Split(line, " ")
	command := symbols[0]
	args := symbols[1:]
	// Return command and arguments
	return Command{command, args}
}

func execute(command Command) {
	// Route the command to call the proper function
	if com, valid := ComMap[command.key]; valid {
		com(command.args)
	} else if string(command.key[0]) == "!" {
		Exclamation(command.key[1:])
	} else if command.key == "exit" {
		saveHistory()
		os.Exit(0)
	} else if command.key == "test_pipe" {
		// Make a list of command lines just for testing
		comms := []Command{
			Command{
				"cat",
				[]string{"README.md"}},
			Command{
				"head",
				[]string{}},
			Command{
				"wc",
				[]string{}}}
		// Run those commands in a pipe
		PipeLine(comms)
	} else {
		fmt.Println("Command not found.")
	}
}

// when the shell is about to be closed, saved all this session's commands to the
// gosh_history file.
func saveHistory() {
	// limit is one minus the length of commandList so to not include
	// any exit commands
	limit := len(commandList) - 1
	historyFile, _ := os.OpenFile("gosh_history.tmp", os.O_WRONLY|os.O_APPEND, 0)
	// add only the commands executed during this session to the
	// gosh history file by starting from the point we saved in
	// whereLeftOff
	for i := whereLeftOff; i < limit; i++ {
		historyFile.WriteString(commandList[i] + "\n")
	}
	historyFile.Close()
}
