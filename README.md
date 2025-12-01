# Remote Control Bot via Telegram

This is an enhanced Python application that allows remote control of a computer through Telegram. The bot provides extensive functionality for system monitoring, file management, and remote operations.

## Instructions / Instrukcje / Инструкции

### English Instructions

#### Installation
1. Clone the repository or download the files
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Edit the `remote_control_bot.py` file and set your:
   - `TELEGRAM_TOKEN` - Your Telegram bot token
   - `ADMIN_ID` - Your Telegram user ID
4. Run the bot:
   ```
   python remote_control_bot.py
   ```

#### Available Commands
- `/start` - Start the bot
- `/help` - Show all available commands
- `/reverse <host> <port>` - Start reverse shell
- `/put <file_path>` - Upload file to bot
- `/get <filename>` - Download file from bot
- `/run <python_code>` - Execute Python code
- `/screenshot` - Take screenshot
- `/keylogger <start/stop>` - Control keylogger
- `/dos <target> <port> <duration>` - DoS attack
- `/schedule <command> <time>` - Schedule task
- `/stop` - Stop the bot
- `/jumpscare [duration]` - Show jumpscare
- `/show <filename>` - Display image/video on screen
- `/grab <path>` - Grab files from computer
- `/steal` - Steal browser passwords
- `/persist` - Add to startup
- `/antivm` - Check for virtual environment
- `/shell <command>` - Execute shell command
- `/browse <path>` - Browse files
- `/sysinfo` - Get system information
- `/processes` - List running processes
- `/kill <pid>` - Kill process by PID
- `/webcam` - Take webcam photo
- `/record_screen <seconds>` - Record screen
- `/lock` - Lock computer
- `/unlock` - Unlock computer
- `/block <url>` - Block website
- `/unblock <url>` - Unblock website
- `/encrypt <file>` - Encrypt file
- `/decrypt <file>` - Decrypt file
- `/message <text>` - Show message on screen
- `/sound <type>` - Play system sound
- `/network` - Scan local network
- `/geolocate` - Get geolocation

### Polish Instrukcje

#### Instalacja
1. Sklonuj repozytorium lub pobierz pliki
2. Zainstaluj wymagane zależności:
   ```
   pip install -r requirements.txt
   ```
3. Edytuj plik `remote_control_bot.py` i ustaw:
   - `TELEGRAM_TOKEN` - Twój token bota Telegram
   - `ADMIN_ID` - Twoje ID użytkownika Telegram
4. Uruchom bota:
   ```
   python remote_control_bot.py
   ```

#### Dostępne komendy
- `/start` - Uruchom bota
- `/help` - Pokaż wszystkie dostępne komendy
- `/reverse <host> <port>` - Odwrotna powłoka
- `/put <ścieżka_pliku>` - Prześlij plik do bota
- `/get <nazwa_pliku>` - Pobierz plik z bota
- `/run <kod_python>` - Wykonaj kod Python
- `/screenshot` - Zrób zrzut ekranu
- `/keylogger <start/stop>` - Sterowanie keyloggerem
- `/dos <cel> <port> <czas_trwania>` - Atak DoS
- `/schedule <komenda> <czas>` - Zaplanuj zadanie
- `/stop` - Zatrzymaj bota
- `/jumpscare [czas_trwania]` - Pokaż jumpscare
- `/show <nazwa_pliku>` - Wyświetl obraz/wideo na ekranie
- `/grab <ścieżka>` - Pobierz pliki z komputera
- `/steal` - Ukradnij hasła z przeglądarki
- `/persist` - Dodaj do autostartu
- `/antivm` - Sprawdź środowisko wirtualne
- `/shell <komenda>` - Wykonaj komendę powłoki
- `/browse <ścieżka>` - Przeglądaj pliki
- `/sysinfo` - Pobierz informacje o systemie
- `/processes` - Lista uruchomionych procesów
- `/kill <pid>` - Zakończ proces po PID
- `/webcam` - Zrób zdjęcie kamerą
- `/record_screen <sekundy>` - Nagrywaj ekran
- `/lock` - Zablokuj komputer
- `/unlock` - Odblokuj komputer
- `/block <url>` - Zablokuj stronę
- `/unblock <url>` - Odblokuj stronę
- `/encrypt <plik>` - Szyfruj plik
- `/decrypt <plik>` - Deszyfruj plik
- `/message <tekst>` - Pokaż wiadomość na ekranie
- `/sound <typ>` - Odtwórz dźwięk systemowy
- `/network` - Skanuj sieć lokalną
- `/geolocate` - Pobierz geolokalizację

### Russian Инструкции

#### Установка
1. Клонируйте репозиторий или скачайте файлы
2. Установите необходимые зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Отредактируйте файл `remote_control_bot.py` и установите:
   - `TELEGRAM_TOKEN` - ваш токен Telegram бота
   - `ADMIN_ID` - ваш ID пользователя Telegram
4. Запустите бота:
   ```
   python remote_control_bot.py
   ```

#### Доступные команды
- `/start` - запустить бота
- `/help` - показать все доступные команды
- `/reverse <хост> <порт>` - обратный шелл
- `/put <путь_к_файлу>` - загрузить файл в бота
- `/get <имя_файла>` - скачать файл из бота
- `/run <python_код>` - выполнить Python код
- `/screenshot` - сделать скриншот
- `/keylogger <start/stop>` - управление keylogger'ом
- `/dos <цель> <порт> <длительность>` - атака DoS
- `/schedule <команда> <время>` - запланировать задачу
- `/stop` - остановить бота
- `/jumpscare [длительность]` - показать jumpscare
- `/show <имя_файла>` - отобразить изображение/видео на экране
- `/grab <путь>` - получить файлы с компьютера
- `/steal` - украсть пароли из браузера
- `/persist` - добавить в автозагрузку
- `/antivm` - проверить виртуальное окружение
- `/shell <команда>` - выполнить команду оболочки
- `/browse <путь>` - просматривать файлы
- `/sysinfo` - получить информацию о системе
- `/processes` - список запущенных процессов
- `/kill <pid>` - убить процесс по PID
- `/webcam` - сделать фото с веб-камеры
- `/record_screen <секунды>` - записать экран
- `/lock` - заблокировать компьютер
- `/unlock` - разблокировать компьютер
- `/block <url>` - заблокировать веб-сайт
- `/unblock <url>` - разблокировать веб-сайт
- `/encrypt <файл>` - зашифровать файл
- `/decrypt <файл>` - расшифровать файл
- `/message <текст>` - показать сообщение на экране
- `/sound <тип>` - воспроизвести системный звук
- `/network` - сканировать локальную сеть
- `/geolocate` - получить геолокацию

## Features

### Core Features
- **Remote Shell**: Execute commands on the target machine
- **File Transfer**: Upload and download files
- **Screenshot**: Capture screen shots
- **Keylogger**: Monitor keystrokes
- **DoS Attack**: Launch denial of service attacks
- **Scheduled Tasks**: Execute commands at specified times
- **File Grabbing**: Extract specific files from the system
- **Password Stealing**: Extract saved passwords from browsers
- **Persistence**: Add bot to system startup
- **Anti-VM Detection**: Check if running in virtual environment

### Enhanced Features (New Innovations)
- **System Information**: Detailed system information including hardware specs
- **Process Management**: List and kill processes
- **Webcam Capture**: Take photos using the webcam
- **Screen Recording**: Record screen activity
- **System Lock**: Lock the target computer
- **URL Blocking**: Block/unblock websites by modifying hosts file
- **File Encryption/Decryption**: Encrypt/decrypt files with Fernet encryption
- **Message Display**: Show custom messages on screen
- **Sound Control**: Play system sounds
- **Network Scanning**: Scan the local network for active hosts
- **Geolocation**: Determine location based on IP address
- **Bluetooth Control**: (Placeholder for future implementation)

### Additional Features
- **Jumpscare**: Display scary message on screen with countdown
- **File Display**: Show images, GIFs, videos on the target screen
- **File Browsing**: Browse files and directories on the system
- **Custom Scripts**: Execute custom Python scripts

## Commands

### Basic Commands
- `/start` - Start the bot and get system notification
- `/help` - Show all available commands
- `/reverse <host> <port>` - Start reverse shell
- `/put <file_path>` - Upload file to Telegram
- `/get <file_name>` - Download file from computer
- `/run <python_code>` - Execute Python code
- `/screenshot` - Take screenshot
- `/keylogger <start/stop>` - Control keylogger
- `/dos <target> <port> <duration>` - Launch DoS attack
- `/schedule <command> <delay>` - Schedule a task
- `/stop` - Stop the bot
- `/grab <path>` - Grab files from the system
- `/steal` - Steal browser passwords
- `/persist` - Add to startup
- `/antivm` - Check for virtual environment
- `/shell <command>` - Execute shell command
- `/browse <path>` - Browse files and folders

### Enhanced Commands
- `/sysinfo` - Get detailed system information
- `/processes` - List running processes
- `/kill <PID>` - Kill a process by PID
- `/webcam` - Capture image from webcam
- `/record_screen <duration>` - Record screen for specified duration
- `/lock` - Lock the computer
- `/unlock` - Unlock the computer
- `/block <url>` - Block a website
- `/unblock <url>` - Unblock a website
- `/encrypt <path>` - Encrypt files in path
- `/decrypt <path>` - Decrypt files in path
- `/message <text>` - Display a message on screen
- `/sound` - Play a system sound
- `/bluetooth` - Bluetooth control (placeholder)
- `/network` - Scan local network
- `/geolocate` - Get geolocation based on IP

### Special Commands
- `/jumpscare [duration]` - Trigger jumpscare with optional duration
- `/show <filename>` - Show an image/video file on screen

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Update the `TELEGRAM_TOKEN` and `ADMIN_ID` in the script with your own values.

3. Run the bot:
```bash
python remote_control_bot.py
```

## Security Notice

⚠️ **IMPORTANT**: This tool is intended for educational purposes and authorized penetration testing only. Use responsibly and only on systems you own or have explicit permission to test. Unauthorized use of this tool may violate local, state, and federal laws.

## Configuration

Edit these values in the script:
- `TELEGRAM_TOKEN`: Your Telegram bot token
- `ADMIN_ID`: Your Telegram user ID for authentication

## Legal Disclaimer

This software is provided for educational and ethical hacking purposes only. The author is not responsible for any misuse of this software. Always obtain proper authorization before using this tool on any system you do not own.