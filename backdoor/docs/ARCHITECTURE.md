# Architektura Systemu Backdoor

## Spis treści

1. [Przegląd](#przegląd)
2. [Architektura Master-Slave](#architektura-master-slave)
3. [Komponenty](#komponenty)
4. [Model danych](#model-danych)
5. [API](#api)
6. [Przepływ danych](#przepływ-danych)
7. [Obsługa błędów](#obsługa-błędów)
8. [System logów](#system-logów)
9. [Bezpieczeństwo](#bezpieczeństwo)

---

## Przegląd

System Backdoor składa się z:
- **Serwera centralnego** (Master) - cała logika, baza danych, panel administracyjny
- **Terminali** (Slave) - proste kioski przy wejściach, tylko wyświetlanie

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         BACKDOOR SYSTEM                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                        ┌──────────────────────┐                         │
│                        │   SERWER (Master)    │                         │
│                        │   PC Obsługi         │                         │
│                        │                      │                         │
│                        │  ┌────────────────┐  │                         │
│                        │  │  SQLite DB     │  │                         │
│                        │  └────────────────┘  │                         │
│                        │  ┌────────────────┐  │                         │
│                        │  │  REST API      │  │                         │
│                        │  │  :8080         │  │                         │
│                        │  └────────────────┘  │                         │
│                        │  ┌────────────────┐  │                         │
│                        │  │  Panel Admin   │  │                         │
│                        │  │  (GUI Fyne)    │  │                         │
│                        │  └────────────────┘  │                         │
│                        │  ┌────────────────┐  │                         │
│                        │  │  System Logów  │  │                         │
│                        │  │  (2 miesiące)  │  │                         │
│                        │  └────────────────┘  │                         │
│                        │         │            │                         │
│                        │    [Czytnik USB]     │                         │
│                        └─────────┬────────────┘                         │
│                                  │                                      │
│                         LAN (HTTP REST)                                 │
│                    ┌─────────────┼─────────────┐                        │
│                    │             │             │                        │
│                    ▼             ▼             ▼                        │
│  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐│
│  │  TERMINAL 1 (Slave) │ │  TERMINAL 2 (Slave) │ │  TERMINAL N (Slave) ││
│  │  Raspberry Pi       │ │  Raspberry Pi       │ │  Stary laptop       ││
│  │                     │ │                     │ │                     ││
│  │  - Fullscreen UI    │ │  - Fullscreen UI    │ │  - Fullscreen UI    ││
│  │  - Tylko wyświetla  │ │  - Tylko wyświetla  │ │  - Tylko wyświetla  ││
│  │  - Czytnik USB      │ │  - Czytnik USB      │ │  - Czytnik USB      ││
│  │  - Dźwięk           │ │  - Dźwięk           │ │  - Dźwięk           ││
│  │  - ZERO LOGIKI      │ │  - ZERO LOGIKI      │ │  - ZERO LOGIKI      ││
│  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Architektura Master-Slave

### Dlaczego Master-Slave?

| Aspekt | Korzyść |
|--------|---------|
| **Prostota** | Terminale nie mają logiki biznesowej |
| **Spójność** | Jedna baza danych, brak synchronizacji |
| **Utrzymanie** | Aktualizacje tylko na serwerze |
| **Debugowanie** | Wszystkie logi w jednym miejscu |
| **Koszt** | Terminale mogą być tanim sprzętem |

### Podział odpowiedzialności

#### Serwer (Master)
- Przechowuje bazę danych SQLite
- Wykonuje całą logikę biznesową
- Udostępnia REST API dla terminali
- Wyświetla panel administracyjny
- Zbiera logi ze wszystkich źródeł
- Obsługuje własny czytnik RFID

#### Terminal (Slave)
- Nasłuchuje czytnika USB (klawiatura)
- Wysyła zapytania do serwera
- Wyświetla odpowiedzi (OK/błąd)
- Odtwarza dźwięki
- Raportuje błędy do serwera
- **NIE MA** lokalnej bazy danych
- **NIE WYKONUJE** żadnej logiki biznesowej

---

## Komponenty

### 1. Serwer

```
internal/server/
├── api/            # REST API
│   ├── router.go       # Routing
│   ├── entry.go        # Endpointy wejść
│   ├── client.go       # Endpointy klientów
│   ├── health.go       # Health check
│   └── log.go          # Endpoint logów
├── admin/          # Panel Admin (Fyne GUI)
│   ├── app.go          # Główne okno
│   ├── clients.go      # Zarządzanie klientami
│   ├── cards.go        # Zarządzanie kartami
│   ├── passes.go       # Zarządzanie karnetami
│   ├── sections.go     # Sekcje i instruktorzy
│   ├── reports.go      # Raporty
│   └── logs.go         # Przeglądarka logów
└── services/       # Logika biznesowa
    ├── entry.go        # Walidacja wejść
    ├── pass.go         # Obsługa karnetów
    ├── client.go       # Obsługa klientów
    └── report.go       # Generowanie raportów
```

### 2. Terminal

```
internal/terminal/
├── app.go          # Główna pętla aplikacji
├── ui.go           # Ekrany (Fyne fullscreen)
├── api_client.go   # Klient HTTP
├── keyboard.go     # Obsługa czytnika USB
└── sound.go        # Odtwarzanie dźwięków
```

### 3. Baza danych

```
internal/database/
├── db.go           # Połączenie SQLite
├── migrations.go   # Migracje schematu
└── queries.go      # Zapytania SQL
```

---

## Model danych

### Schemat ERD

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   clients   │     │    cards    │     │   passes    │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ id          │◄────│ client_id   │     │ id          │
│ first_name  │     │ id          │     │ client_id   │──►│
│ last_name   │     │ uid         │     │ pass_type_id│
│ phone       │     │ is_blocked  │     │ section_id  │
│ notes       │     │ block_reason│     │ valid_from  │
│ created_at  │     │ issued_at   │     │ valid_until │
│ is_active   │     │ blocked_at  │     │ entries_*   │
└─────────────┘     └─────────────┘     │ is_multisport│
       │                                 │ price_paid  │
       │                                 │ is_active   │
       │                                 └─────────────┘
       │                                        │
       │            ┌─────────────┐             │
       │            │   entries   │             │
       │            ├─────────────┤             │
       └───────────►│ client_id   │◄────────────┘
                    │ card_id     │
                    │ pass_id     │
                    │ entry_date  │
                    │ entry_time  │
                    │ entry_type  │  ('card'|'manual')
                    │ is_cancelled│
                    │ cancel_reason│
                    └─────────────┘

┌─────────────┐     ┌─────────────┐
│ instructors │     │  sections   │
├─────────────┤     ├─────────────┤
│ id          │◄────│instructor_id│
│ name        │     │ id          │
│ is_active   │     │ name        │
└─────────────┘     │ day_of_week │
                    │ is_active   │
                    └─────────────┘

┌─────────────┐     ┌─────────────┐
│ pass_types  │     │ system_logs │
├─────────────┤     ├─────────────┤
│ id          │     │ id          │
│ name        │     │ timestamp   │
│ category    │     │ level       │
│ duration_days│    │ source      │
│ entry_limit │     │ category    │
│ price       │     │ message     │
└─────────────┘     │ details     │
                    └─────────────┘

┌─────────────┐
│  audit_log  │
├─────────────┤
│ id          │
│ timestamp   │
│ operator    │
│ action      │
│ entity_type │
│ entity_id   │
│ old_value   │
│ new_value   │
│ reason      │
└─────────────┘
```

### Pełny schemat SQL

```sql
-- Klienci
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Karty RFID
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    client_id INTEGER REFERENCES clients(id),
    is_blocked BOOLEAN DEFAULT FALSE,
    block_reason TEXT,
    issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    blocked_at DATETIME
);

-- Instruktorzy
CREATE TABLE instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Sekcje (grupy)
CREATE TABLE sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_id INTEGER REFERENCES instructors(id),
    name TEXT NOT NULL,
    day_of_week INTEGER,  -- 0=niedziela, 1=pon, 2=wt, ...
    time_start TEXT,      -- "18:00"
    is_active BOOLEAN DEFAULT TRUE
);

-- Typy karnetów
CREATE TABLE pass_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,  -- 'commercial', 'section', 'instructor'
    duration_days INTEGER,   -- NULL dla sekcyjnych
    entry_limit INTEGER,     -- NULL dla miesięcznych
    price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- Karnety klientów
CREATE TABLE passes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    pass_type_id INTEGER NOT NULL REFERENCES pass_types(id),
    section_id INTEGER REFERENCES sections(id),
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    entries_remaining INTEGER,
    entries_total INTEGER,
    is_multisport BOOLEAN DEFAULT FALSE,
    price_paid DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT
);

-- Wejścia
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    card_id INTEGER REFERENCES cards(id),
    pass_id INTEGER REFERENCES passes(id),
    entry_date DATE NOT NULL,
    entry_time DATETIME NOT NULL,
    entry_type TEXT NOT NULL DEFAULT 'card',  -- 'card', 'manual'
    terminal_id TEXT,
    is_cancelled BOOLEAN DEFAULT FALSE,
    cancel_reason TEXT,
    cancelled_by TEXT,
    cancelled_at DATETIME,
    notes TEXT,
    created_by TEXT
);

-- Logi systemowe
CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT NOT NULL,      -- 'DEBUG', 'INFO', 'WARN', 'ERROR'
    source TEXT NOT NULL,     -- 'server', 'terminal-1', etc.
    category TEXT NOT NULL,   -- 'entry', 'api', 'db', 'system'
    message TEXT NOT NULL,
    details TEXT,             -- JSON
    card_uid TEXT,
    client_id INTEGER,
    operator TEXT
);

-- Audit log
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    operator TEXT,
    action TEXT NOT NULL,
    entity_type TEXT,
    entity_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    reason TEXT
);

-- Indeksy
CREATE INDEX idx_cards_uid ON cards(uid);
CREATE INDEX idx_cards_client ON cards(client_id);
CREATE INDEX idx_passes_client ON passes(client_id);
CREATE INDEX idx_passes_valid ON passes(valid_until, is_active);
CREATE INDEX idx_entries_date ON entries(entry_date);
CREATE INDEX idx_entries_client ON entries(client_id);
CREATE INDEX idx_logs_timestamp ON system_logs(timestamp);
CREATE INDEX idx_logs_level ON system_logs(level);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
```

---

## API

### Endpointy

| Metoda | Endpoint | Opis | Używany przez |
|--------|----------|------|---------------|
| POST | `/api/entry/check` | Sprawdź kartę | Terminal |
| POST | `/api/entry/confirm` | Potwierdź wejście | Terminal |
| POST | `/api/log` | Zapisz log | Terminal |
| GET | `/api/health` | Health check | Terminal |

### POST /api/entry/check

Sprawdza czy karta może wejść.

**Request:**
```json
{
    "card_uid": "A1B2C3D4",
    "terminal_id": "terminal-wejscie-1"
}
```

**Response (sukces):**
```json
{
    "allowed": true,
    "client_name": "Jan Kowalski",
    "message": "Karnet miesięczny",
    "valid_until": "31.01.2024",
    "entries_info": null,
    "extra_notice": "Pamiętaj o karcie Multisport",
    "sound": "ok"
}
```

**Response (błąd):**
```json
{
    "allowed": false,
    "client_name": "Anna Nowak",
    "message": "Karnet wygasł",
    "valid_until": "15.01.2024",
    "entries_info": null,
    "extra_notice": null,
    "sound": "error"
}
```

**Response (karnet na wejścia):**
```json
{
    "allowed": true,
    "client_name": "Piotr Wiśniewski",
    "message": "Karnet 10 wejść",
    "valid_until": "28.02.2024",
    "entries_info": "Pozostało: 7/10",
    "extra_notice": null,
    "sound": "ok"
}
```

### POST /api/entry/confirm

Rejestruje wejście w bazie (wywoływane po check jeśli allowed=true).

**Request:**
```json
{
    "card_uid": "A1B2C3D4",
    "terminal_id": "terminal-wejscie-1"
}
```

**Response:**
```json
{
    "success": true,
    "entry_id": 12345
}
```

### POST /api/log

Zapisuje log z terminala.

**Request:**
```json
{
    "level": "ERROR",
    "source": "terminal-wejscie-1",
    "category": "connection",
    "message": "Timeout podczas sprawdzania karty",
    "details": {
        "card_uid": "A1B2C3D4",
        "timeout_ms": 3000
    }
}
```

### GET /api/health

Sprawdza czy serwer działa.

**Response:**
```json
{
    "status": "ok",
    "time": "2024-01-20T14:30:00Z",
    "version": "1.0.0"
}
```

---

## Przepływ danych

### Wejście kartą (flow)

```
Terminal                          Serwer
   │                                 │
   │  [Klient przykłada kartę]       │
   │                                 │
   ├──POST /api/entry/check─────────►│
   │  {card_uid, terminal_id}        │
   │                                 │
   │                          ┌──────┴──────┐
   │                          │ Walidacja:  │
   │                          │ - karta?    │
   │                          │ - zablok.?  │
   │                          │ - karnet?   │
   │                          │ - ważność?  │
   │                          │ - limit?    │
   │                          │ - dziś był? │
   │                          └──────┬──────┘
   │                                 │
   │◄─────────Response───────────────┤
   │  {allowed, client_name, ...}    │
   │                                 │
   ├──[Wyświetl wynik]               │
   ├──[Zagraj dźwięk]                │
   │                                 │
   │  [jeśli allowed=true]           │
   │                                 │
   ├──POST /api/entry/confirm───────►│
   │  {card_uid, terminal_id}        │
   │                                 │
   │                          ┌──────┴──────┐
   │                          │ Zapisz      │
   │                          │ wejście     │
   │                          │ w bazie     │
   │                          └──────┬──────┘
   │                                 │
   │◄─────────Response───────────────┤
   │  {success, entry_id}            │
   │                                 │
   ├──[Powrót do IDLE]               │
   │                                 │
```

### Logika walidacji wejścia

```go
func (s *EntryService) CheckEntry(cardUID, terminalID string) EntryCheckResponse {
    // 1. Znajdź kartę
    card := s.db.FindCardByUID(cardUID)
    if card == nil {
        return EntryCheckResponse{
            Allowed: false,
            Message: "Nieznana karta",
            Sound:   "error",
        }
    }

    // 2. Sprawdź czy zablokowana
    if card.IsBlocked {
        return EntryCheckResponse{
            Allowed: false,
            Message: "Karta zablokowana",
            Sound:   "error",
        }
    }

    // 3. Pobierz klienta
    client := s.db.GetClient(card.ClientID)
    if client == nil || !client.IsActive {
        return EntryCheckResponse{
            Allowed: false,
            Message: "Klient nieaktywny",
            Sound:   "error",
        }
    }

    // 4. Sprawdź czy już dziś wchodził
    todayEntry := s.db.GetTodayEntry(client.ID)
    if todayEntry != nil {
        // Powrót - OK, ale nie rejestruj ponownie
        return EntryCheckResponse{
            Allowed:    true,
            ClientName: client.FullName(),
            Message:    "Powrót",
            Sound:      "ok",
        }
    }

    // 5. Znajdź aktywny karnet
    pass := s.db.GetActivePass(client.ID, time.Now())
    if pass == nil {
        return EntryCheckResponse{
            Allowed:    false,
            ClientName: client.FullName(),
            Message:    "Brak aktywnego karnetu",
            Sound:      "error",
        }
    }

    // 6. Sprawdź datę ważności
    if pass.ValidUntil.Before(time.Now()) {
        return EntryCheckResponse{
            Allowed:    false,
            ClientName: client.FullName(),
            Message:    "Karnet wygasł",
            ValidUntil: pass.ValidUntil.Format("02.01.2006"),
            Sound:      "error",
        }
    }

    // 7. Dla karnetów na wejścia - sprawdź limit
    if pass.EntriesRemaining != nil && *pass.EntriesRemaining <= 0 {
        return EntryCheckResponse{
            Allowed:    false,
            ClientName: client.FullName(),
            Message:    "Wykorzystano wszystkie wejścia",
            Sound:      "error",
        }
    }

    // 8. OK - przygotuj odpowiedź
    response := EntryCheckResponse{
        Allowed:    true,
        ClientName: client.FullName(),
        Message:    pass.TypeName(),
        ValidUntil: pass.ValidUntil.Format("02.01.2006"),
        Sound:      "ok",
    }

    // Info o pozostałych wejściach
    if pass.EntriesRemaining != nil {
        response.EntriesInfo = fmt.Sprintf("Pozostało: %d/%d",
            *pass.EntriesRemaining, *pass.EntriesTotal)
    }

    // Przypomnienie o Multisport
    if pass.IsMultisport {
        response.ExtraNotice = "Pamiętaj o karcie Multisport"
    }

    return response
}
```

---

## Obsługa błędów

### Terminal - zasady

1. **NIGDY nie pokazuj stack trace** - tylko przyjazne komunikaty
2. **NIGDY nie wis** - zawsze timeout i powrót do IDLE
3. **Wszystkie błędy loguj na serwerze**

### Komunikaty dla klienta

| Sytuacja | Komunikat | Kolor |
|----------|-----------|-------|
| Timeout serwera | "Spróbuj ponownie" | żółty |
| Serwer niedostępny | "Brak połączenia" | żółty |
| Błąd odczytu karty | "Przyłóż kartę ponownie" | żółty |
| Nieznana karta | "Nieznana karta - zgłoś się do obsługi" | czerwony |
| Karnet wygasł | "Karnet wygasł - zgłoś się do obsługi" | czerwony |
| Karta zablokowana | "Karta zablokowana - zgłoś się do obsługi" | czerwony |
| Brak karnetu | "Brak karnetu - zgłoś się do obsługi" | czerwony |

### Terminal - maszyna stanów

```
                    ┌─────────────────────────┐
                    │                         │
                    ▼                         │
            ┌───────────────┐                 │
            │    IDLE       │                 │
            │ "PRZYŁÓŻ      │                 │
            │  KARTĘ"       │                 │
            └───────┬───────┘                 │
                    │ [karta]                 │
                    ▼                         │
            ┌───────────────┐                 │
            │   CHECKING    │                 │
            │ "Sprawdzam..."│                 │
            │  (timeout 3s) │                 │
            └───────┬───────┘                 │
        ┌───────────┼───────────┬─────────────┤
        ▼           ▼           ▼             │
  ┌───────────┐ ┌───────────┐ ┌───────────┐   │
  │  SUCCESS  │ │   ERROR   │ │  CONN_ERR │   │
  │   (3s)    │ │   (5s)    │ │   (5s)    │   │
  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘   │
        └─────────────┴─────────────┴─────────┘
```

---

## System logów

### Poziomy logów

| Poziom | Użycie |
|--------|--------|
| DEBUG | Szczegóły techniczne (tylko dev) |
| INFO | Normalne operacje (wejścia, zmiany) |
| WARN | Potencjalne problemy (karnet wygasł, timeout) |
| ERROR | Błędy wymagające uwagi |

### Kategorie

| Kategoria | Przykłady |
|-----------|-----------|
| `entry` | Wejścia, walidacje |
| `api` | Requesty HTTP |
| `db` | Operacje bazodanowe |
| `auth` | Logowania operatorów |
| `system` | Start/stop, konfiguracja |
| `audit` | Zmiany w danych |

### Retencja

- Logi systemowe: **2 miesiące**
- Audit log: **bez limitu** (lub do ręcznego usunięcia)

### Automatyczne czyszczenie

```sql
-- Codziennie o 3:00 w nocy
DELETE FROM system_logs
WHERE timestamp < datetime('now', '-60 days');
```

---

## Bezpieczeństwo

### Sieć

- System działa **tylko w sieci lokalnej (LAN)**
- Brak dostępu z internetu
- Komunikacja HTTP (nie HTTPS) - akceptowalne w LAN

### Dane

- Minimalizacja danych (RODO)
- Brak danych płatniczych
- Brak adresów, dokumentów
- Możliwość usunięcia danych klienta

### Kopie zapasowe

- Regularne backupy bazy SQLite
- Backup = kopia pliku `.db`
- Zalecane: codziennie na zewnętrzny dysk/NAS

### Uprawnienia (opcjonalnie)

W przyszłości można dodać:
- Logowanie operatorów
- Role (admin, obsługa)
- Audyt kto co zmienił
