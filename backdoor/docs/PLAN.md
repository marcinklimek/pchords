# Plan Implementacji - Backdoor

## Spis treści

1. [Fazy projektu](#fazy-projektu)
2. [Szczegółowy plan](#szczegółowy-plan)
3. [Priorytety](#priorytety)
4. [Ryzyka](#ryzyka)
5. [Definicja ukończenia](#definicja-ukończenia)

---

## Fazy projektu

```
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 1: Fundament                                              │
│  ─────────────────                                              │
│  • Struktura projektu Go                                        │
│  • Model danych + SQLite                                        │
│  • Podstawowe CRUD                                              │
│  • Testy jednostkowe                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 2: Logika biznesowa                                       │
│  ────────────────────────                                       │
│  • Walidacja wejść                                              │
│  • Obsługa karnetów (wszystkie typy)                            │
│  • Obsługa sekcji                                               │
│  • System logów i audytu                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 3: API REST                                               │
│  ────────────────                                               │
│  • Endpointy dla terminali                                      │
│  • Health check                                                 │
│  • Logowanie z terminali                                        │
│  • Obsługa błędów                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 4: Panel Admin (GUI)                                      │
│  ─────────────────────────                                      │
│  • Okno główne Fyne                                             │
│  • Zarządzanie klientami                                        │
│  • Zarządzanie kartami                                          │
│  • Zarządzanie karnetami                                        │
│  • Sekcje i instruktorzy                                        │
│  • Obsługa czytnika USB na serwerze                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 5: Terminal (Kiosk)                                       │
│  ────────────────────────                                       │
│  • Aplikacja fullscreen Fyne                                    │
│  • Obsługa czytnika USB                                         │
│  • Komunikacja z API                                            │
│  • Dźwięki                                                      │
│  • Obsługa błędów/timeoutów                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 6: Raporty                                                │
│  ───────────────                                                │
│  • Raport dzienny                                               │
│  • Raport miesięczny                                            │
│  • Raport sekcji                                                │
│  • Historia klienta                                             │
│  • Eksport CSV/PDF                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FAZA 7: Testy i wdrożenie                                      │
│  ────────────────────────                                       │
│  • Testy integracyjne                                           │
│  • Testy na sprzęcie docelowym                                  │
│  • Dokumentacja użytkownika                                     │
│  • Skrypty instalacyjne                                         │
│  • Szkolenie                                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Szczegółowy plan

### FAZA 1: Fundament

#### 1.1 Struktura projektu
- [ ] Inicjalizacja `go.mod`
- [ ] Struktura katalogów
- [ ] Konfiguracja (YAML)
- [ ] Makefile

#### 1.2 Baza danych
- [ ] Połączenie SQLite
- [ ] Migracje schematu
- [ ] Modele Go (structs)
- [ ] Podstawowe zapytania

#### 1.3 CRUD operacje
- [ ] Klienci (Create, Read, Update, Delete)
- [ ] Karty (wydanie, blokada, przypisanie)
- [ ] Typy karnetów
- [ ] Instruktorzy
- [ ] Sekcje

#### 1.4 Testy
- [ ] Testy modeli
- [ ] Testy zapytań SQL
- [ ] Dane testowe (fixtures)

---

### FAZA 2: Logika biznesowa

#### 2.1 Walidacja wejść
- [ ] Sprawdzenie karty (aktywna/zablokowana)
- [ ] Sprawdzenie klienta
- [ ] Sprawdzenie karnetu (ważność, typ)
- [ ] Sprawdzenie czy już dziś wchodził
- [ ] Debouncing (ochrona przed wielokrotnym odbiciem)

#### 2.2 Obsługa karnetów
- [ ] Karnet miesięczny (data ważności)
- [ ] Karnet na wejścia (limit + data ważności)
- [ ] Karnet sekcyjny (przypisanie do sekcji, dzień tygodnia)
- [ ] Flaga Multisport

#### 2.3 Obsługa sekcji
- [ ] Przypisanie klienta do sekcji
- [ ] Walidacja dnia tygodnia
- [ ] Statystyki sekcji

#### 2.4 System logów
- [ ] Logger wrapper
- [ ] Zapis do bazy
- [ ] Poziomy logów
- [ ] Automatyczne czyszczenie (2 miesiące)

#### 2.5 Audit log
- [ ] Zapis zmian w encjach
- [ ] Kto, kiedy, co zmienił
- [ ] Powód zmiany

---

### FAZA 3: API REST

#### 3.1 Router i middleware
- [ ] Router (net/http lub chi)
- [ ] CORS (jeśli potrzebne)
- [ ] Logging middleware
- [ ] Recovery (panic handling)

#### 3.2 Endpointy
- [ ] `POST /api/entry/check` - sprawdzenie karty
- [ ] `POST /api/entry/confirm` - rejestracja wejścia
- [ ] `POST /api/log` - log z terminala
- [ ] `GET /api/health` - health check

#### 3.3 Obsługa błędów
- [ ] Standardowe kody HTTP
- [ ] Czytelne komunikaty JSON
- [ ] Logowanie błędów

---

### FAZA 4: Panel Admin (GUI Fyne)

#### 4.1 Okno główne
- [ ] Layout z nawigacją (tabs/menu)
- [ ] Statusbar
- [ ] Konfiguracja okna

#### 4.2 Moduł Klienci
- [ ] Lista klientów (tabela)
- [ ] Wyszukiwanie
- [ ] Formularz dodawania/edycji
- [ ] Szczegóły klienta (historia)

#### 4.3 Moduł Karty
- [ ] Lista kart klienta
- [ ] Wydanie nowej karty
- [ ] Blokada karty (z powodem)
- [ ] Przeniesienie karnetu na nową kartę

#### 4.4 Moduł Karnety
- [ ] Lista aktywnych karnetów
- [ ] Dodawanie karnetu
- [ ] Edycja/anulowanie
- [ ] Historia karnetów

#### 4.5 Moduł Sekcje
- [ ] Lista instruktorów
- [ ] Lista sekcji (grup)
- [ ] Przypisanie uczestników
- [ ] Harmonogram

#### 4.6 Obsługa czytnika
- [ ] Nasłuchiwanie klawiatury (czytnik USB)
- [ ] Szybkie wyszukanie klienta po karcie
- [ ] Rejestracja wejścia ręcznego

---

### FAZA 5: Terminal (Kiosk)

#### 5.1 Aplikacja Fyne
- [ ] Fullscreen mode
- [ ] Duże, czytelne fonty
- [ ] Ekrany stanów (IDLE, SUCCESS, ERROR)
- [ ] Kolory sygnalizacyjne

#### 5.2 Obsługa czytnika USB
- [ ] Nasłuchiwanie klawiatury
- [ ] Parsowanie UID karty
- [ ] Debouncing

#### 5.3 Komunikacja z API
- [ ] HTTP client z timeoutem
- [ ] Retry logic
- [ ] Obsługa błędów sieci

#### 5.4 Dźwięki
- [ ] Odtwarzanie WAV
- [ ] Dźwięk OK
- [ ] Dźwięk ERROR
- [ ] Konfiguracja głośności

#### 5.5 Obsługa błędów
- [ ] Timeout → "Spróbuj ponownie"
- [ ] Brak sieci → "Brak połączenia"
- [ ] Zawsze powrót do IDLE

---

### FAZA 6: Raporty

#### 6.1 Raport dzienny
- [ ] Lista wejść z dnia
- [ ] Podział: komercyjne vs sekcyjne
- [ ] Wejścia ręczne oznaczone

#### 6.2 Raport miesięczny
- [ ] Podsumowanie wejść
- [ ] Statystyki karnetów
- [ ] Wpływy (jeśli zapisywane)

#### 6.3 Raport sekcji
- [ ] Frekwencja per sekcja
- [ ] Frekwencja per instruktor
- [ ] Lista uczestników z obecnościami

#### 6.4 Historia klienta
- [ ] Wszystkie karnety
- [ ] Wszystkie wejścia
- [ ] Wszystkie karty

#### 6.5 Eksport
- [ ] CSV
- [ ] PDF (opcjonalnie)
- [ ] Drukowanie

---

### FAZA 7: Testy i wdrożenie

#### 7.1 Testy
- [ ] Testy jednostkowe (>80% coverage)
- [ ] Testy integracyjne API
- [ ] Testy E2E (symulacja terminala)
- [ ] Testy na RPi

#### 7.2 Dokumentacja
- [ ] Instrukcja obsługi
- [ ] FAQ
- [ ] Troubleshooting

#### 7.3 Deployment
- [ ] Skrypt instalacji serwera
- [ ] Skrypt instalacji terminala
- [ ] Systemd service files
- [ ] Backup script

#### 7.4 Szkolenie
- [ ] Szkolenie obsługi
- [ ] Dokumentacja dla admina

---

## Priorytety

### Must Have (MVP)
1. Walidacja wejść kartą
2. Podstawowe typy karnetów (miesięczny, na wejścia)
3. Panel admin - klienci, karty, karnety
4. Terminal - wyświetlanie wyniku
5. Podstawowe logi

### Should Have
1. Sekcje i instruktorzy
2. Raporty
3. Blokada karty z powodem
4. Wejście ręczne
5. Multisport (komunikat)

### Nice to Have
1. Eksport PDF
2. Statystyki graficzne
3. Logowanie operatorów
4. Kopie zapasowe automatyczne

---

## Ryzyka

| Ryzyko | Prawdopodobieństwo | Wpływ | Mitygacja |
|--------|-------------------|-------|-----------|
| Problemy z czytnikiem USB | Średnie | Wysoki | Testować różne modele czytników |
| Wydajność SQLite przy dużej ilości danych | Niskie | Średni | Indeksy, czyszczenie logów |
| Problemy z Fyne na RPi | Średnie | Wysoki | Testy na sprzęcie docelowym wcześnie |
| Brak sieci LAN między serwerem a terminalem | Niskie | Wysoki | Instrukcja konfiguracji sieci |

---

## Definicja ukończenia

### Faza uznana za ukończoną gdy:

1. **Kod** - wszystkie zadania zaimplementowane
2. **Testy** - pokrycie >80%, wszystkie przechodzą
3. **Dokumentacja** - README zaktualizowane
4. **Review** - kod przejrzany
5. **Demo** - funkcjonalność pokazana i zaakceptowana
