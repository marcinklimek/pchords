# Backdoor - Makefile
# ====================

.PHONY: all server terminal-arm terminal-amd64 clean test run-server run-terminal deps lint

# Wersja
VERSION := 1.0.0
BUILD_TIME := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
LDFLAGS := -ldflags "-X main.Version=$(VERSION) -X main.BuildTime=$(BUILD_TIME)"

# Katalogi
BIN_DIR := bin
DATA_DIR := data

# Domyślny cel
all: server terminal-arm terminal-amd64

# === BUILD ===

# Serwer (Linux x64)
server:
	@echo "Building server (linux/amd64)..."
	@mkdir -p $(BIN_DIR)
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/backdoor-server ./cmd/server

# Serwer (Windows)
server-windows:
	@echo "Building server (windows/amd64)..."
	@mkdir -p $(BIN_DIR)
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/backdoor-server.exe ./cmd/server

# Terminal (Raspberry Pi ARM64)
terminal-arm:
	@echo "Building terminal (linux/arm64)..."
	@mkdir -p $(BIN_DIR)
	GOOS=linux GOARCH=arm64 go build $(LDFLAGS) -o $(BIN_DIR)/backdoor-terminal-arm64 ./cmd/terminal

# Terminal (Raspberry Pi ARM32)
terminal-arm32:
	@echo "Building terminal (linux/arm)..."
	@mkdir -p $(BIN_DIR)
	GOOS=linux GOARCH=arm GOARM=7 go build $(LDFLAGS) -o $(BIN_DIR)/backdoor-terminal-arm32 ./cmd/terminal

# Terminal (Linux x64 - stary laptop)
terminal-amd64:
	@echo "Building terminal (linux/amd64)..."
	@mkdir -p $(BIN_DIR)
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/backdoor-terminal-amd64 ./cmd/terminal

# Terminal (Windows)
terminal-windows:
	@echo "Building terminal (windows/amd64)..."
	@mkdir -p $(BIN_DIR)
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/backdoor-terminal.exe ./cmd/terminal

# === RUN ===

# Uruchom serwer lokalnie
run-server:
	@mkdir -p $(DATA_DIR)
	go run ./cmd/server --config configs/server.yaml

# Uruchom terminal lokalnie
run-terminal:
	go run ./cmd/terminal --config configs/terminal.yaml

# === TEST ===

# Uruchom testy
test:
	go test -v ./...

# Testy z coverage
test-coverage:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report: coverage.html"

# Benchmark
bench:
	go test -bench=. ./...

# === TOOLS ===

# Pobierz zależności
deps:
	go mod download
	go mod tidy

# Lint
lint:
	@which golangci-lint > /dev/null || (echo "Installing golangci-lint..." && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest)
	golangci-lint run ./...

# Format kodu
fmt:
	go fmt ./...

# === CLEAN ===

# Wyczyść build
clean:
	rm -rf $(BIN_DIR)
	rm -f coverage.out coverage.html

# === INSTALL ===

# Zainstaluj na serwerze (wymaga sudo)
install-server:
	@echo "Installing server..."
	@mkdir -p /opt/backdoor
	@cp $(BIN_DIR)/backdoor-server /opt/backdoor/
	@cp -r configs /opt/backdoor/
	@cp -r assets /opt/backdoor/
	@mkdir -p /opt/backdoor/data
	@echo "Server installed to /opt/backdoor"

# Zainstaluj terminal (wymaga sudo)
install-terminal:
	@echo "Installing terminal..."
	@mkdir -p /opt/backdoor-terminal
	@cp $(BIN_DIR)/backdoor-terminal-* /opt/backdoor-terminal/ 2>/dev/null || true
	@cp configs/terminal.yaml /opt/backdoor-terminal/
	@cp -r assets /opt/backdoor-terminal/
	@echo "Terminal installed to /opt/backdoor-terminal"

# === RELEASE ===

# Zbuduj wszystkie wersje do release
release: clean
	@echo "Building release..."
	@mkdir -p $(BIN_DIR)/release

	# Serwer
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/release/backdoor-server-linux-amd64 ./cmd/server
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/release/backdoor-server-windows-amd64.exe ./cmd/server

	# Terminal
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/release/backdoor-terminal-linux-amd64 ./cmd/terminal
	GOOS=linux GOARCH=arm64 go build $(LDFLAGS) -o $(BIN_DIR)/release/backdoor-terminal-linux-arm64 ./cmd/terminal
	GOOS=linux GOARCH=arm GOARM=7 go build $(LDFLAGS) -o $(BIN_DIR)/release/backdoor-terminal-linux-arm32 ./cmd/terminal
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o $(BIN_DIR)/release/backdoor-terminal-windows-amd64.exe ./cmd/terminal

	@echo "Release builds in $(BIN_DIR)/release/"

# === HELP ===

help:
	@echo "Backdoor - System Obsługi Wejść"
	@echo ""
	@echo "Użycie: make [cel]"
	@echo ""
	@echo "Build:"
	@echo "  all              - Zbuduj serwer i terminale (domyślny)"
	@echo "  server           - Zbuduj serwer (linux/amd64)"
	@echo "  server-windows   - Zbuduj serwer (windows)"
	@echo "  terminal-arm     - Zbuduj terminal (RPi ARM64)"
	@echo "  terminal-arm32   - Zbuduj terminal (RPi ARM32)"
	@echo "  terminal-amd64   - Zbuduj terminal (linux/amd64)"
	@echo "  terminal-windows - Zbuduj terminal (windows)"
	@echo "  release          - Zbuduj wszystkie wersje"
	@echo ""
	@echo "Run:"
	@echo "  run-server       - Uruchom serwer lokalnie"
	@echo "  run-terminal     - Uruchom terminal lokalnie"
	@echo ""
	@echo "Test:"
	@echo "  test             - Uruchom testy"
	@echo "  test-coverage    - Testy z raportem coverage"
	@echo "  lint             - Sprawdź kod linterem"
	@echo ""
	@echo "Other:"
	@echo "  deps             - Pobierz zależności"
	@echo "  fmt              - Formatuj kod"
	@echo "  clean            - Wyczyść build"
	@echo "  help             - Pokaż tę pomoc"
