// Backdoor Terminal - Aplikacja kiosk dla wejść
// ==============================================
//
// Prosta aplikacja wyświetlająca:
// - Ekran "PRZYŁÓŻ KARTĘ"
// - Wynik sprawdzenia (OK/BŁĄD)
// - Komunikaty dla klienta
//
// Cała logika znajduje się na serwerze.

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
	configPath := flag.String("config", "configs/terminal.yaml", "Ścieżka do pliku konfiguracyjnego")
	showVersion := flag.Bool("version", false, "Pokaż wersję")
	flag.Parse()

	if *showVersion {
		fmt.Printf("Backdoor Terminal v%s (built: %s)\n", Version, BuildTime)
		os.Exit(0)
	}

	fmt.Printf("Backdoor Terminal v%s\n", Version)
	fmt.Printf("Config: %s\n", *configPath)
	fmt.Println("")
	fmt.Println("TODO: Implementacja terminala")
	fmt.Println("- [ ] Załaduj konfigurację")
	fmt.Println("- [ ] Uruchom GUI fullscreen (Fyne)")
	fmt.Println("- [ ] Nasłuchuj czytnika USB (klawiatura)")
	fmt.Println("- [ ] Komunikuj się z serwerem API")
}
