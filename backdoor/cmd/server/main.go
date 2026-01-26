// Backdoor Server - Panel Administracyjny + API REST
// ===================================================
//
// Główna aplikacja serwera zawierająca:
// - Panel administracyjny (GUI Fyne)
// - REST API dla terminali
// - Bazę danych SQLite
// - System logów

package main

import (
	"flag"
	"fmt"
	"os"
)

var (
	Version   = "dev"
	BuildTime = "unknown"
)

func main() {
	configPath := flag.String("config", "configs/server.yaml", "Ścieżka do pliku konfiguracyjnego")
	showVersion := flag.Bool("version", false, "Pokaż wersję")
	flag.Parse()

	if *showVersion {
		fmt.Printf("Backdoor Server v%s (built: %s)\n", Version, BuildTime)
		os.Exit(0)
	}

	fmt.Printf("Backdoor Server v%s\n", Version)
	fmt.Printf("Config: %s\n", *configPath)
	fmt.Println("")
	fmt.Println("TODO: Implementacja serwera")
	fmt.Println("- [ ] Załaduj konfigurację")
	fmt.Println("- [ ] Połącz z bazą SQLite")
	fmt.Println("- [ ] Uruchom API REST")
	fmt.Println("- [ ] Uruchom Panel Admin (Fyne)")
}
