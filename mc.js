/**
 * Skrypt bota do Minecrafta z obsługą wielu instancji, limitowaniem użycia PROXY.
 * POPRAWKA: Zmieniono sposób przekazywania hosta do SocksProxyAgent, aby naprawić błąd "No host defined!".
 * * * * * * * * Aby uruchomić:
 * 1. Upewnij się, że masz zainstalowane Node.js.
 * 2. W folderze projektu uruchom: npm install mineflayer socks-proxy-agent
 * 3. UZUPEŁNIJ PLIK 'active_proxies.txt' swoimi danymi (TYLKO PROXY SOCKS5!)
 * 4. Uruchom skrypt: node mc.js
 */

const fs = require('fs'); // Moduł do obsługi plików
const mineflayer = require('mineflayer');
const { SocksProxyAgent } = require('socks-proxy-agent'); 
const readline = require('readline'); // MODUŁ DO ODBIORU DANYCH Z TERMINALA

// ===================================================================
// 1. DYNAMICZNE WCZYTYWANIE PROXY Z PLIKU
// ===================================================================

const PROXY_FILE = 'active_proxies.txt'; // Nazwa pliku z listą proxy
const MAX_BOTS_PER_PROXY = 5;            

/**
 * Funkcja wczytująca i parsująca konfiguracje proxy z pliku tekstowego.
 * @returns {Array} Lista obiektów konfiguracyjnych proxy.
 */
function loadProxyConfigsFromFile() {
    try {
        console.log(`\nPróba odczytu pliku proxy: ${PROXY_FILE}`);
        const data = fs.readFileSync(PROXY_FILE, 'utf8');
        // Filtrujemy puste linie i te zaczynające się od '#' (komentarze)
        const lines = data.split('\n').filter(line => line.trim() !== '' && !line.trim().startsWith('#'));
        
        const configs = lines.map(line => {
            const trimmedLine = line.trim();
            let match;

            // 1. Próba dopasowania do pełnego formatu: socks[45]://[user:pass@]host:port
            match = trimmedLine.match(/(socks[45]):\/\/(([^:@]+):([^@]+)@)?([^:]+):(\d+)/i);
            
            if (match) {
                const type = match[1];
                const username = match[3] || '';
                const password = match[4] || '';
                const host = match[5];
                const port = parseInt(match[6]);

                return {
                    host,
                    port,
                    type,
                    auth: { username, password }
                };
            }

            // 2. Próba dopasowania do prostego formatu: host:port
            match = trimmedLine.match(/^([^:]+):(\d+)$/);

            if (match) {
                const host = match[1];
                const port = parseInt(match[2]);

                return {
                    host,
                    port,
                    type: 'socks5', // DOMYŚLNE ZAAŁOŻENIE DLA PROSTEGO FORMATU
                    auth: { username: '', password: '' }
                };
            }

            console.warn(`[PARSER WARNING] Nie udało się poprawnie sparsować linii: ${trimmedLine}. Oczekiwany format: socks5://[user:pass@]host:port LUB host:port`);
            return null;

        }).filter(config => config !== null);

        if (configs.length === 0) {
            console.error(`Nie znaleziono żadnych poprawnych konfiguracji proxy w pliku ${PROXY_FILE}.`);
        } else {
            console.log(`Wczytano ${configs.length} konfiguracji proxy z pliku ${PROXY_FILE}.`);
        }
        return configs;

    } catch (err) {
        if (err.code === 'ENOENT') {
            console.error(`BŁĄD KRYTYCZNY: Nie znaleziono pliku ${PROXY_FILE}. Utwórz ten plik i umieść w nim konfiguracje proxy.`);
        } else {
            console.error(`BŁĄD KRYTYCZNY: Wystąpił błąd podczas odczytu pliku ${PROXY_FILE}:`, err.message);
        }
        process.exit(1); // Zakończenie skryptu, jeśli plik nie został wczytany
    }
}

// Globalna lista konfiguracji proxy (wczytana z pliku)
const PROXY_CONFIGS = loadProxyConfigsFromFile(); 

// Mapa do śledzenia użycia każdego proxy: { index_w_PROXY_CONFIGS: liczba_botów }
const PROXY_USAGE = {}; 

/**
 * Funkcja zwraca dostępną konfigurację proxy (obiekt z PROXY_CONFIGS) 
 * lub null, jeśli wszystkie proxy osiągnęły limit użycia.
 */
function getAvailableProxy() {
    for (let i = 0; i < PROXY_CONFIGS.length; i++) {
        // Inicjalizacja licznika, jeśli jeszcze go nie ma
        if (PROXY_USAGE[i] === undefined) {
            PROXY_USAGE[i] = 0;
        }

        // Sprawdzanie, czy dany proxy nie osiągnął limitu
        if (PROXY_USAGE[i] < MAX_BOTS_PER_PROXY) {
            PROXY_USAGE[i]++;
            console.log(`[PROXY ASSIGN] Przydzielono botowi proxy nr ${i}. Użycie: ${PROXY_USAGE[i]}/${MAX_BOTS_PER_PROXY}`);
            return PROXY_CONFIGS[i];
        }
    }
    return null; // Brak dostępnego proxy
}


// ===================================================================
// 2. GENERATOR NICKÓW
// ===================================================================

/**
 * Generuje losowy, unikalny nick bota (np. Gh43fsf).
 * Używa małych i dużych liter oraz cyfr. Długość od 6 do 12 znaków.
 * @returns {string} Wygenerowany nick
 */
function generateRandomUsername() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    // Długość nicka od 6 do 12 znaków
    const length = Math.floor(Math.random() * (12 - 6 + 1)) + 6; 
    let result = '';
    
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    
    // Upewniamy się, że pierwszy znak nie jest cyfrą
    if ('0123456789'.includes(result.charAt(0))) {
        return generateRandomUsername(); // Rekurencyjne wywołanie, jeśli zaczyna się od cyfry
    }

    return result;
}

// ===================================================================
// 3. KONFIGURACJA SERWERA
// ===================================================================

// Host zmieniony na JBWM.pl na podstawie logów
const BOT_HOST = 'JBWM.pl'; 
const BOT_PORT = 25565;
const BOT_VERSION = '1.20.1';
const BOT_PASSWORD = 'super_secret_password_123'; // Używane do /register i /login

// WAŻNE: JEŚLI BOTY OTRZYMUJĄ BŁĄD "You are not white-listed on this server!", 
// MUSISZ USTAWIĆ W PLIKU server.properties: white-list=false (lub dodać nazwy botów do białej listy).

const BOT_CONFIGS = []; // Ta lista zostanie dynamicznie wypełniona


/**
 * Funkcja tworząca i uruchamiająca pojedynczego bota.
 * @param {object} botOptions Konfiguracja bota (host, username, etc.)
 */
function createBot(botOptions) {
    const proxy = getAvailableProxy();

    if (!proxy) {
        console.error(`NIE ZNALEZIONO DOSTĘPNEGO PROXY dla bota ${botOptions.username}. Bot nie zostanie uruchomiony.`);
        return;
    }

    let finalBotOptions = { ...botOptions }; 

    // --- Konfiguracja Proxy ---
    const authPart = proxy.auth.username && proxy.auth.password 
        ? `${proxy.auth.username}:${proxy.auth.password}@` 
        : '';
    
    const proxyUrl = `${proxy.type}://${authPart}${proxy.host}:${proxy.port}`;
    
    console.log(`[${botOptions.username}] Próba połączenia z proxy: ${proxyUrl}`);
    
    try {
        const agent = new SocksProxyAgent(proxyUrl);
        
        // Zastępujemy domyślną funkcję połączenia, aby użyć proxy
        // Poprawiony kod - zamiast client.options.username używamy botOptions.username
        finalBotOptions.connect = (client) => {
            console.log(`[${botOptions.username}] Łączenie przez proxy z serwerem docelowym: ${BOT_HOST}:${BOT_PORT}`);
            agent.connect({
                host: BOT_HOST, // POPRAWKA: Użycie stałej BOT_HOST
                port: BOT_PORT // POPRAWKA: Użycie stałej BOT_PORT
            }, (err, stream) => {
                if (err) {
                    // W przypadku błędu (np. nieprawidłowe proxy SOCKS/HTTP), wypisujemy go
                    console.error(`[${botOptions.username}] BŁĄD PROXY: ${err.message}`);
                    client.emit('error', new Error(`Błąd połączenia przez proxy: ${err.message}`));
                    client.emit('end', 'Proxy connection error');
                    return;
                }
                // Jeśli sukces, przekazujemy strumień do klienta
                client.setSocket(stream);
                client.emit('connect');
            });
        };

    } catch (error) {
        console.error(`[${botOptions.username}] BŁĄD: Nie udało się utworzyć agenta proxy lub funkcji connect.`, error);
        return; 
    }
    
    console.log(`[${botOptions.username}] Próba połączenia z serwerem ${finalBotOptions.host} (przez proxy)...`);
    const bot = mineflayer.createBot(finalBotOptions);

    // --- Obsługa zdarzeń ---

    bot.on('spawn', () => {
        console.log(`[${bot.username}] POŁĄCZONO! Bot się pojawił.`);
        // Po udanym spawn, bot czeka na komunikat autoryzacyjny
    });

    bot.on('message', (message) => {
        const msgText = message.toString();
        console.log(`[${bot.username} | CZAT] ${msgText}`); 
        
        // --- LOGIKA REJESTRACJI/LOGOWANIA ---
        
        const lowerMsg = msgText.toLowerCase();

        // 1. Natychmiastowe logowanie po udanej rejestracji
        if (lowerMsg.includes('zarejestrowany') && lowerMsg.includes('pomyslnie')) {
             console.log(`[${bot.username} | AUTH] Udana rejestracja! Natychmiast próbuję zalogować...`);
             // Krok kluczowy, aby zapobiec rozłączeniu przez serwer
             bot.chat(`/login ${BOT_PASSWORD}`);
             return; 
        }
        
        // 2. Wykrywanie prośby o rejestrację
        if (lowerMsg.includes('/register') && !lowerMsg.includes('zalogowano')) {
             console.log(`[${bot.username} | AUTH] Wykryto potrzebę rejestracji. Wysyłam /register...`);
             // Rejestracja: /register <haslo> <haslo>
             bot.chat(`/register ${BOT_PASSWORD} ${BOT_PASSWORD}`);
        } 
        // 3. Wykrywanie prośby o logowanie
        else if (lowerMsg.includes('/login') && !lowerMsg.includes('zalogowano')) {
             console.log(`[${bot.username} | AUTH] Wykryto potrzebę logowania. Wysyłam /login...`);
             // Logowanie: /login <haslo>
             bot.chat(`/login ${BOT_PASSWORD}`);
        }
        
        // 4. Wiadomość potwierdzająca pomyślne logowanie
        if (lowerMsg.includes('zalogowano') || lowerMsg.includes('mozesz sie poruszac')) {
             console.log(`[${bot.username} | AUTH] Bot zalogowany! Wysyłam wiadomość powitalną.`);
             bot.chat(`Cześć! Jestem botem ${bot.username} i używam proxy!`);
        }

        // --- Inne komendy (po zalogowaniu) ---

        // Przykładowa reakcja na komendę
        if (msgText.startsWith('!status') && message.getText().split('>')[0].trim() !== bot.username) {
            bot.chat(`Mój ping to: ${bot.player.ping} ms. Używam wersji ${bot.version}.`);
        }
    });

    bot.on('end', (reason) => {
        console.log(`[${bot.username}] ROZŁĄCZONO. Powód: ${reason}`);
    });

    bot.on('error', (err) => {
        console.error(`[${bot.username}] WYSTĄPIŁ BŁĄD:`, err);
        if (err.code !== 'EAUTH') {
            console.error(`[${bot.username}] Błąd niekrytyczny.`);
        } else {
             console.error(`[${bot.username}] BŁĄD EAUTH: Serwer jest w trybie ONLINE. Zmień go na tryb OFFLINE/Cracked.`);
        }
    });
}

// ===================================================================
// 4. INTERAKTYWNE URUCHAMIANIE
// ===================================================================

/**
 * Główna funkcja uruchamiająca proces bota.
 * @param {number} botCount Liczba botów do uruchomienia.
 * @param {number} delaySeconds Opóźnienie między botami w sekundach.
 */
function launchAllBots(botCount, delaySeconds) {
    if (PROXY_CONFIGS.length === 0) {
        console.error("Nie można uruchomić botów: nie wczytano żadnych poprawnych konfiguracji proxy.");
        return;
    }
    
    // Dynamiczne generowanie BOT_CONFIGS na podstawie botCount
    for (let i = 0; i < botCount; i++) {
        // Generujemy nick z przedrostkiem "Bot" dla lepszej identyfikacji
        const randomUsername = "Bot_" + generateRandomUsername();
        
        BOT_CONFIGS.push({
            host: BOT_HOST,
            port: BOT_PORT,
            username: randomUsername,
            version: BOT_VERSION
        });
    }

    const maxBots = PROXY_CONFIGS.length * MAX_BOTS_PER_PROXY;
    
    let finalBotCount = BOT_CONFIGS.length;

    if (maxBots < botCount) {
        console.error("!!! BŁĄD KONFIGURACJI !!!");
        console.error(`Zdefiniowałeś ${botCount} botów, ale masz tylko ${PROXY_CONFIGS.length} proxy.`);
        console.error(`Maksymalna liczba obsługiwanych botów to: ${maxBots}.`);
        console.error("Uruchamiam maksymalną możliwą liczbę botów.");
        // Ograniczamy listę do maksymalnej możliwej liczby
        BOT_CONFIGS.splice(maxBots); 
        finalBotCount = maxBots;
    }
    

    console.log(`\nSTARTUJĘ ${finalBotCount} BOTÓW Z OGRANICZENIEM ${MAX_BOTS_PER_PROXY} BÓTÓW NA PROXY.`);
    console.log(`OPÓŹNIENIE MIĘDZY BOTAMI: ${delaySeconds} sekund.\n`);
    
    // Uruchamianie botów z opóźnieniem
    const delayMs = delaySeconds * 1000;
    
    BOT_CONFIGS.forEach((botConfig, index) => {
        // Uruchamiamy każdego bota z opóźnieniem zależnym od jego indeksu i żądanego czasu
        setTimeout(() => createBot(botConfig), index * delayMs);
    });
}


/**
 * Funkcja interaktywnie pyta użytkownika o liczbę botów, a następnie o opóźnienie.
 */
function promptUserForBotCount() {
    const maxBots = PROXY_CONFIGS.length * MAX_BOTS_PER_PROXY;
    
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    console.log(`\n--- Uruchamianie Floty Botów ---`);
    console.log(`Dostępne proxy: ${PROXY_CONFIGS.length} (${MAX_BOTS_PER_PROXY} boty na proxy).`);
    console.log(`Maksymalna liczba botów, jaką możesz uruchomić: ${maxBots}.\n`);

    rl.question('Ile botów chcesz uruchomić? (Wpisz liczbę, np. 50): ', (countAnswer) => {
        const botCount = parseInt(countAnswer.trim(), 10);
        
        if (isNaN(botCount) || botCount <= 0) {
            rl.close();
            console.error("Nieprawidłowa wartość. Proszę podać poprawną liczbę naturalną. Uruchom skrypt ponownie.");
            return;
        }

        rl.question('Jakie opóźnienie (w sekundach) ma być między kolejnymi botami? (Wpisz liczbę, np. 1): ', (delayAnswer) => {
            rl.close();
            const delaySeconds = parseFloat(delayAnswer.trim());

            if (isNaN(delaySeconds) || delaySeconds < 0) {
                console.error("Nieprawidłowa wartość opóźnienia. Proszę podać poprawną liczbę. Uruchom skrypt ponownie.");
                return;
            }

            launchAllBots(botCount, delaySeconds);
        });
    });
}

// Rozpoczęcie od zapytania użytkownika
promptUserForBotCount();