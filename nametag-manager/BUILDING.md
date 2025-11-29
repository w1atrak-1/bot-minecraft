# Building the Nametag Manager Mod

## Prerequisites

- Java 17 or higher
- Gradle (for building the mod)

## Building the Mod

1. Make sure you have Gradle installed on your system
2. Navigate to the mod directory:
   ```bash
   cd /workspace/nametag-manager
   ```
3. Build the mod:
   ```bash
   gradle build
   ```
4. The built mod JAR file will be located in `build/libs/`

## Using the Mod

1. Install Minecraft 1.20.1 with Fabric Loader
2. Install Fabric API for 1.20.1
3. Place the built JAR file in your Minecraft `mods` folder
4. Launch the game - the mod will create a config file at `config/nametagmanager.json`
5. Adjust settings in the config file as desired

## Development

The mod uses the Fabric API to hook into Minecraft's rendering system to display custom nametags. The main components are:

- `NametagManager.java` - Main mod entry point
- `NametagRenderer.java` - Handles the rendering of custom nametags
- `Config.java` - Manages configuration settings

The mod renders nametags client-side only, meaning changes are only visible to the local player and don't affect other players' game experience.