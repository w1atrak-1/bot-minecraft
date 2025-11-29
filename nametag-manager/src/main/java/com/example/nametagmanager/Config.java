package com.example.nametagmanager;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Config {
    public boolean nametagsEnabled = true;
    public boolean showDistance = true;
    public boolean showHealth = false;
    public boolean seeThroughWalls = false; // New option for seeing nametags through walls
    public double maxRenderDistance = 32.0;
    public String customFormat = "{name}";
    
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final String CONFIG_FILE = "config/nametagmanager.json";
    
    public static Config load() {
        Path configPath = Path.of(CONFIG_FILE);
        if (Files.exists(configPath)) {
            try (FileReader reader = new FileReader(configPath.toFile())) {
                return GSON.fromJson(reader, Config.class);
            } catch (IOException e) {
                NametagManager.LOGGER.error("Failed to load config, using defaults", e);
                return new Config();
            }
        } else {
            // Create default config
            Config config = new Config();
            config.save();
            return config;
        }
    }
    
    public void save() {
        try {
            Path configPath = Path.of(CONFIG_FILE);
            Files.createDirectories(configPath.getParent());
            try (FileWriter writer = new FileWriter(configPath.toFile())) {
                GSON.toJson(this, writer);
            }
        } catch (IOException e) {
            NametagManager.LOGGER.error("Failed to save config", e);
        }
    }
}