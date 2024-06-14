package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"

	// "net/url"
	"net/http"
	"strings"
)

func replaceAtIndex(in string, r rune, i int) string {
	out := []rune(in)
	out[i] = r
	return string(out)
}

func CommandExecute(bash_command string) (string, string, error) {
	var stdout, stderr bytes.Buffer
	cmd := exec.Command("bash", "-c", bash_command)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	return stdout.String(), stderr.String(), err
}

func SendToTelegram(message string, chat_id string, telegram_bot_api string) {

	client := &http.Client{}

	header := fmt.Sprintf("{\"chat_id\": \"%s\", \"text\": \"%s\", \"disable_notification\": true}", chat_id, message)
	var data = strings.NewReader(header)

	req, err := http.NewRequest("POST", telegram_bot_api, data)
	if err != nil {
		log.Fatal(err)
	}

	req.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()

	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s\n", bodyText)
}

func main() {
	var should_send bool = true

	chat_id := "ENTER_YOUR_API"
	bot_api := "ENTER_YOUR_API"
	telegram_bot_api := fmt.Sprintf("https://api.telegram.org/bot%s/sendMessage", bot_api)

	arguments := os.Args[1:]
	command := strings.Join(arguments, " ")

	if len(command) > 0 {
		stdout, stderr, err := CommandExecute(command)

		if err != nil {
			log.Printf("error: %v\n", err)
		}

		var message string
		if len(strings.TrimSpace(stderr)) != 0 {
			message = stderr
		} else {
			message = stdout
		}

		if len(message) == 0 {
			message = "Empty command output"
		}

		if should_send {
			for i := len(message) - 1; i >= 0; i-- {
				if string(message[i]) == "\"" {
					message = replaceAtIndex(message, '\\', i)
				}
			}
			SendToTelegram(message, chat_id, telegram_bot_api)
		} else {
			fmt.Println(message)
		}
	} else {
		log.Printf("Absence of bash command in command-line argument")
	}

}
