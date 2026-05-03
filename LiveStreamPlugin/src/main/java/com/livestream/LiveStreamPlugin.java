package com.livestream;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.event.player.AsyncPlayerChatEvent;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class LiveStreamPlugin extends JavaPlugin implements Listener, CommandExecutor, TabCompleter {

    // Mapa przechowująca streamy: UUID gracza -> dane streama
    private final Map<UUID, StreamData> activeStreams = new ConcurrentHashMap<>();
    
    // Set z permisjami dla rang które mogą ustawiać stream
    private Set<String> allowedPermissions;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        
        // Konfiguracja dozwolonych permisji
        allowedPermissions = new HashSet<>();
        allowedPermissions.add("livestream.creator"); // Ranga Twórca
        allowedPermissions.add("livestream.media");   // Ranga Media
        
        // Rejestracja komend i eventów
        getCommand("live").setExecutor(this);
        getCommand("live").setTabCompleter(this);
        Bukkit.getPluginManager().registerEvents(this, this);
        
        getLogger().info("LiveStreamPlugin został włączony!");
    }

    @Override
    public void onDisable() {
        getLogger().info("LiveStreamPlugin został wyłączony!");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equalsIgnoreCase("live")) {
            if (args.length == 0) {
                // Wyświetlenie wszystkich aktywnych streamów
                showLiveStreams(sender);
                return true;
            } else if (args[0].equalsIgnoreCase("start") && sender instanceof Player) {
                // Ustawienie streama: /live start <platforma> <link>
                if (args.length < 3) {
                    sender.sendMessage(ChatColor.RED + "Użycie: /live start <platforma> <link>");
                    sender.sendMessage(ChatColor.RED + "Przykład: /live start twitch https://twitch.tv/twojnick");
                    return true;
                }
                
                Player player = (Player) sender;
                
                // Sprawdzenie czy gracz ma odpowiednią rangę
                if (!hasAllowedPermission(player)) {
                    player.sendMessage(ChatColor.RED + "Nie masz uprawnień do ustawienia streama!");
                    player.sendMessage(ChatColor.RED + "Tylko rangi Twórca i Media mogą używać tej komendy.");
                    return true;
                }
                
                String platform = args[1];
                String link = args[2];
                
                // Walidacja linku
                if (!isValidUrl(link)) {
                    player.sendMessage(ChatColor.RED + "Nieprawidłowy format linku!");
                    return true;
                }
                
                // Dodanie streama
                StreamData streamData = new StreamData(player.getName(), platform, link);
                activeStreams.put(player.getUniqueId(), streamData);
                
                // Powiadomienie gracza
                player.sendMessage(ChatColor.GREEN + "Rozpoczęto transmisję na " + ChatColor.AQUA + platform);
                
                // Opcjonalne powiadomienie serwera
                if (getConfig().getBoolean("broadcast-stream-start", false)) {
                    broadcastStreamStart(player.getName(), platform, link);
                }
                
                return true;
            } else if (args[0].equalsIgnoreCase("stop") && sender instanceof Player) {
                // Zatrzymanie streama: /live stop
                Player player = (Player) sender;
                
                if (!activeStreams.containsKey(player.getUniqueId())) {
                    player.sendMessage(ChatColor.RED + "Nie prowadzisz obecnie żadnej transmisji!");
                    return true;
                }
                
                activeStreams.remove(player.getUniqueId());
                player.sendMessage(ChatColor.GREEN + "Zakończono transmisję.");
                
                return true;
            } else {
                sender.sendMessage(ChatColor.RED + "Użycie: /live");
                sender.sendMessage(ChatColor.RED + "       /live start <platforma> <link> - rozpocznie transmisję");
                sender.sendMessage(ChatColor.RED + "       /live stop - zakończy transmisję");
                return true;
            }
        }
        return false;
    }

    private void showLiveStreams(CommandSender sender) {
        if (activeStreams.isEmpty()) {
            sender.sendMessage(ChatColor.YELLOW + "Brak aktywnych transmisji na żywo.");
            return;
        }

        sender.sendMessage("");
        sender.sendMessage(ChatColor.GOLD + "" + ChatColor.BOLD + "-------------------------------------------");
        sender.sendMessage("");
        
        for (StreamData stream : activeStreams.values()) {
            sender.sendMessage(ChatColor.WHITE + "Gracz " + ChatColor.AQUA + stream.getPlayerName() + 
                             ChatColor.WHITE + " rozpoczął transmisje na " + 
                             ChatColor.AQUA + stream.getPlatform());
            
            // Klikalny link
            String clickableLink = createClickableLink(stream.getLink());
            sender.sendMessage(clickableLink);
            
            sender.sendMessage("");
        }
        
        sender.sendMessage(ChatColor.GOLD + "" + ChatColor.BOLD + "-------------------------------------------");
    }

    private String createClickableLink(String url) {
        // W Minecraft JSON text components są potrzebne dla klikalnych linków
        // Używamy formatu JSON przez tellraw style
        return ChatColor.BLUE + "" + ChatColor.UNDERLINE + url;
    }

    private void broadcastStreamStart(String playerName, String platform, String link) {
        String message = ChatColor.GOLD + "" + ChatColor.BOLD + "-------------------------------------------";
        String message2 = ChatColor.WHITE + "Gracz " + ChatColor.AQUA + playerName + 
                         ChatColor.WHITE + " rozpoczął transmisje na " + 
                         ChatColor.AQUA + platform;
        String message3 = ChatColor.BLUE + "" + ChatColor.UNDERLINE + link;
        String message4 = ChatColor.GOLD + "" + ChatColor.BOLD + "-------------------------------------------";
        
        Bukkit.broadcastMessage(message);
        Bukkit.broadcastMessage(message2);
        Bukkit.broadcastMessage(message3);
        Bukkit.broadcastMessage(message4);
    }

    private boolean hasAllowedPermission(Player player) {
        for (String permission : allowedPermissions) {
            if (player.hasPermission(permission)) {
                return true;
            }
        }
        return false;
    }

    private boolean isValidUrl(String url) {
        return url.startsWith("http://") || url.startsWith("https://");
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        // Usuń stream gdy gracz opuści serwer
        activeStreams.remove(event.getPlayer().getUniqueId());
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (args.length == 1) {
            return Arrays.asList("start", "stop");
        } else if (args.length == 2 && args[0].equalsIgnoreCase("start")) {
            return Arrays.asList("twitch", "youtube", "tiktok", "facebook", "instagram");
        }
        return null;
    }

    // Klasa wewnętrzna przechowująca dane o streamie
    private static class StreamData {
        private final String playerName;
        private final String platform;
        private final String link;

        public StreamData(String playerName, String platform, String link) {
            this.playerName = playerName;
            this.platform = platform;
            this.link = link;
        }

        public String getPlayerName() {
            return playerName;
        }

        public String getPlatform() {
            return platform;
        }

        public String getLink() {
            return link;
        }
    }
}
