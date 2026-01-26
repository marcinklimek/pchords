# Wycena Projektu - Backdoor

## System Obsługi Wejść i Karnetów

**Data wyceny:** Styczeń 2024
**Wersja:** 1.0

---

## Podsumowanie

| Kategoria | Koszt netto |
|-----------|-------------|
| **Oprogramowanie** | 15 000 - 22 000 PLN |
| **Hardware (1 terminal)** | 800 - 1 500 PLN |
| **Hardware (serwer - jeśli nowy)** | 1 500 - 3 000 PLN |
| **Wdrożenie i szkolenie** | 1 500 - 2 500 PLN |
| | |
| **RAZEM (z 1 terminalem)** | **18 800 - 29 000 PLN** |

---

## Część I: Oprogramowanie

### Zestawienie prac programistycznych

| Moduł | Zakres | Pracochłonność | Koszt |
|-------|--------|----------------|-------|
| **1. Fundament** | Struktura projektu, baza danych SQLite, modele, CRUD | 16-24h | 1 600 - 2 400 PLN |
| **2. Logika biznesowa** | Walidacja wejść, obsługa karnetów (wszystkie typy), sekcje, logi, audyt | 24-32h | 2 400 - 3 200 PLN |
| **3. API REST** | Endpointy dla terminali, obsługa błędów | 8-12h | 800 - 1 200 PLN |
| **4. Panel Admin** | GUI Fyne - klienci, karty, karnety, sekcje, obsługa czytnika | 40-56h | 4 000 - 5 600 PLN |
| **5. Terminal** | Aplikacja kiosk, czytnik USB, dźwięki, obsługa błędów | 16-24h | 1 600 - 2 400 PLN |
| **6. Raporty** | Dzienny, miesięczny, sekcyjny, eksport CSV | 16-24h | 1 600 - 2 400 PLN |
| **7. Testy i wdrożenie** | Testy, dokumentacja, skrypty instalacyjne | 16-24h | 1 600 - 2 400 PLN |
| **8. Poprawki i dopracowanie** | Bufor na nieprzewidziane | 8-16h | 800 - 1 600 PLN |

### Podsumowanie oprogramowania

| | Minimum | Maximum |
|---|---------|---------|
| **Godziny pracy** | 144h | 212h |
| **Stawka godzinowa** | 100 PLN | 100 PLN |
| **Koszt oprogramowania** | **14 400 PLN** | **21 200 PLN** |

*Zaokrąglone: **15 000 - 22 000 PLN***

---

## Część II: Hardware

### Wariant A: Terminal na Raspberry Pi

| Element | Cena jednostkowa | Ilość | Koszt |
|---------|-----------------|-------|-------|
| Raspberry Pi 4 (2GB RAM) | 250 - 350 PLN | 1 | 250 - 350 PLN |
| Zasilacz USB-C 5V/3A | 50 - 80 PLN | 1 | 50 - 80 PLN |
| Karta microSD 32GB | 30 - 50 PLN | 1 | 30 - 50 PLN |
| Obudowa RPi | 30 - 80 PLN | 1 | 30 - 80 PLN |
| Monitor 7-10" HDMI | 200 - 400 PLN | 1 | 200 - 400 PLN |
| Czytnik RFID USB | 80 - 200 PLN | 1 | 80 - 200 PLN |
| Kable (HDMI, USB) | 30 - 50 PLN | 1 | 30 - 50 PLN |
| Głośnik USB/jack (opcja) | 30 - 80 PLN | 1 | 30 - 80 PLN |
| | | | |
| **RAZEM Terminal RPi** | | | **700 - 1 290 PLN** |

### Wariant B: Terminal na starym laptopie/PC

| Element | Cena jednostkowa | Ilość | Koszt |
|---------|-----------------|-------|-------|
| Używany laptop/mini PC | 300 - 800 PLN | 1 | 300 - 800 PLN |
| Czytnik RFID USB | 80 - 200 PLN | 1 | 80 - 200 PLN |
| | | | |
| **RAZEM Terminal laptop** | | | **380 - 1 000 PLN** |

*Uwaga: Jeśli macie stary laptop/PC - koszt tylko czytnik ~100-200 PLN*

### Serwer (PC obsługi)

| Element | Cena | Uwagi |
|---------|------|-------|
| **Jeśli jest istniejący PC** | 0 PLN | Wymagania: Windows/Linux, 4GB RAM, 50GB dysk |
| Czytnik RFID USB | 80 - 200 PLN | Dla serwera (opcjonalnie) |
| | | |
| **Jeśli potrzebny nowy PC** | 1 500 - 3 000 PLN | Mini PC / laptop |

### Karty RFID

| Element | Cena jednostkowa | Ilość | Koszt |
|---------|-----------------|-------|-------|
| Karty RFID 13.56MHz (opakowanie 100szt) | 80 - 150 PLN | 1 | 80 - 150 PLN |
| Breloki RFID (opcja, 50szt) | 100 - 180 PLN | 1 | 100 - 180 PLN |

### Podsumowanie hardware

| Konfiguracja | Koszt |
|--------------|-------|
| **1 terminal RPi + istniejący PC serwer** | 700 - 1 300 PLN |
| **1 terminal RPi + nowy PC serwer** | 2 200 - 4 300 PLN |
| **1 terminal laptop + istniejący PC** | 400 - 1 000 PLN |
| **Każdy dodatkowy terminal** | 400 - 1 300 PLN |
| **Karty RFID (100szt)** | 80 - 150 PLN |

---

## Część III: Wdrożenie i szkolenie

| Usługa | Zakres | Koszt |
|--------|--------|-------|
| **Instalacja serwera** | Konfiguracja PC, instalacja aplikacji, bazy danych | 500 - 800 PLN |
| **Instalacja terminali** | Konfiguracja RPi/laptopów, sieć, testy | 300 - 500 PLN / terminal |
| **Konfiguracja sieci** | Router, statyczne IP, testy połączeń | 200 - 400 PLN |
| **Szkolenie obsługi** | 2-3h szkolenie praktyczne | 300 - 500 PLN |
| **Dokumentacja** | Instrukcja obsługi, FAQ, troubleshooting | Wliczone w software |
| | | |
| **RAZEM wdrożenie** | | **1 300 - 2 200 PLN** |

---

## Warianty cenowe

### Wariant EKONOMICZNY

*Istniejący PC jako serwer, 1 terminal na starym laptopie*

| Pozycja | Koszt |
|---------|-------|
| Oprogramowanie | 15 000 PLN |
| Hardware (czytniki 2szt) | 300 PLN |
| Karty RFID (100szt) | 100 PLN |
| Wdrożenie | 1 300 PLN |
| | |
| **RAZEM** | **16 700 PLN netto** |

### Wariant STANDARDOWY

*Istniejący PC jako serwer, 1 terminal Raspberry Pi*

| Pozycja | Koszt |
|---------|-------|
| Oprogramowanie | 18 000 PLN |
| Terminal RPi (komplet) | 1 000 PLN |
| Czytnik USB dla serwera | 150 PLN |
| Karty RFID (100szt) | 100 PLN |
| Wdrożenie | 1 500 PLN |
| | |
| **RAZEM** | **20 750 PLN netto** |

### Wariant ROZSZERZONY

*Nowy PC jako serwer, 2 terminale Raspberry Pi*

| Pozycja | Koszt |
|---------|-------|
| Oprogramowanie | 22 000 PLN |
| Serwer (mini PC) | 2 500 PLN |
| Terminale RPi 2x | 2 000 PLN |
| Czytnik USB dla serwera | 150 PLN |
| Karty RFID (200szt) | 200 PLN |
| Wdrożenie | 2 500 PLN |
| | |
| **RAZEM** | **29 350 PLN netto** |

---

## Harmonogram płatności (propozycja)

| Etap | % | Kwota* | Kiedy |
|------|---|--------|-------|
| **1. Zaliczka** | 30% | ~6 000 PLN | Przed rozpoczęciem |
| **2. Po fazie 4** | 40% | ~8 000 PLN | Panel Admin gotowy |
| **3. Końcowa** | 30% | ~6 000 PLN | Po wdrożeniu |

*Dla wariantu standardowego ~20 000 PLN*

---

## Gwarancja i wsparcie

### W cenie
- **3 miesiące gwarancji** na naprawę błędów
- **Dokumentacja** techniczna i użytkownika
- **Pomoc zdalna** przy problemach (do 5h)

### Opcjonalnie (płatne)
| Usługa | Koszt |
|--------|-------|
| Przedłużona gwarancja (12 mies.) | 200 PLN/mies. |
| Pakiet wsparcia (5h/mies.) | 400 PLN/mies. |
| Rozwój nowych funkcji | 100 PLN/h |
| Interwencja na miejscu | 150 PLN/h + dojazd |

---

## Co zawiera wycena

### Oprogramowanie
- [x] Aplikacja serwera z panelem admin
- [x] Aplikacja terminala (kiosk)
- [x] Baza danych SQLite
- [x] REST API
- [x] Obsługa wszystkich typów karnetów
- [x] Obsługa sekcji i instruktorów
- [x] Raporty (dzienny, miesięczny, sekcyjny)
- [x] System logów i audytu
- [x] Eksport CSV
- [x] Dokumentacja

### Hardware (do zakupu)
- [ ] Raspberry Pi / laptop na terminal
- [ ] Monitor dla terminala
- [ ] Czytniki RFID USB
- [ ] Karty RFID
- [ ] Okablowanie

### Wdrożenie
- [x] Instalacja na sprzęcie klienta
- [x] Konfiguracja sieci
- [x] Szkolenie obsługi
- [x] Testy produkcyjne

---

## Czego NIE zawiera wycena

- Zakup sprzętu (hardware) - wyceniony oddzielnie
- Integracja z systemami zewnętrznymi
- Aplikacja mobilna
- Integracja z płatnościami online
- Hosting w chmurze (system jest offline)
- Wsparcie po okresie gwarancji (bez umowy)

---

## Uwagi końcowe

1. **Ceny netto** - do doliczenia VAT 23%
2. **Ważność wyceny** - 30 dni od daty sporządzenia
3. **Hardware** - ceny orientacyjne, zależne od dostępności
4. **Czas realizacji** - szacunkowo 4-8 tygodni od podpisania umowy
5. **Wymagania** - dostęp do sieci LAN, miejsce na sprzęt

---

## Kontakt

W razie pytań dotyczących wyceny lub zakresu projektu - zapraszam do kontaktu.

---

*Dokument wygenerowany automatycznie. Wersja 1.0*
