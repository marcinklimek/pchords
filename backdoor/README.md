# Backdoor - System Obsługi Wejść i Karnetów

System do zarządzania wejściami na obiekt (ścianka wspinaczkowa) z obsługą kart RFID, karnetów i sekcji.

## Cechy systemu

- **Offline** - działa bez internetu, w sieci lokalnej
- **Master-Slave** - serwer centralny + terminale przy wejściach
- **RFID** - identyfikacja klientów kartami RFID (czytniki USB HID)
- **Karnety** - miesięczne, sekcyjne, na ilość wejść
- **Sekcje** - obsługa grup wspinaczkowych z instruktorami
- **Raporty** - dzienne, miesięczne, sekcyjne, audyt
- **RODO** - minimalizacja danych, praca offline

## Architektura

```
┌─────────────────────┐
│   SERWER (Master)   │
│   PC Obsługi        │
│                     │
│  - Panel Admin GUI  │
│  - REST API         │
│  - SQLite DB        │
│  - Logi centralne   │
│  - Czytnik USB      │
└──────────┬──────────┘
           │ LAN
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────┐
│TERMINAL │  │TERMINAL │
│ (Slave) │  │ (Slave) │
│   RPi   │  │ Laptop  │
└─────────┘  └─────────┘
```

## Technologia

- **Język**: Go 1.21+
- **GUI**: Fyne v2
- **Baza danych**: SQLite 3
- **API**: REST (net/http)
- **Hardware**: Raspberry Pi 4 / stary laptop

## Struktura projektu

```
backdoor/
├── cmd/
│   ├── server/         # Serwer + Panel Admin
│   └── terminal/       # Terminal (kiosk)
├── internal/
│   ├── server/         # Logika serwera
│   ├── terminal/       # Logika terminala
│   ├── database/       # SQLite
│   ├── models/         # Struktury danych
│   └── common/         # Wspólne utilities
├── assets/             # Dźwięki, fonty
├── configs/            # Pliki konfiguracyjne
├── scripts/            # Skrypty instalacyjne
└── docs/               # Dokumentacja
```

## Quick Start

```bash
# Build serwera
make server

# Build terminala (ARM dla RPi)
make terminal-arm

# Build terminala (x64 dla laptopa)
make terminal-amd64

# Uruchom serwer
./bin/backdoor-server --config configs/server.yaml

# Uruchom terminal
./bin/backdoor-terminal --config configs/terminal.yaml
```

## Dokumentacja

- [Architektura](docs/ARCHITECTURE.md)
- [Plan implementacji](docs/PLAN.md)
- [Wycena projektu](docs/WYCENA.md)
- [API Reference](docs/API.md)

## Status

🟡 W fazie planowania
