# Nametag Manager Mod

A Minecraft mod that allows management of player nametags (visually, locally) for Minecraft 1.20+.

## Features

- Customizable player nametags that render visually for the local player only
- Configurable nametag format with placeholders
- Distance and health information display options
- Configurable render distance
- Option to see nametags through walls/obstacles
- Local-only modifications (doesn't affect other players)

## Configuration

The mod creates a configuration file at `config/nametagmanager.json` with the following options:

- `nametagsEnabled`: Whether nametags are displayed (default: true)
- `showDistance`: Show distance to player in nametag (default: true)
- `showHealth`: Show player health in nametag (default: false)
- `seeThroughWalls`: Whether to show nametags even when obstructed by blocks (default: false)
- `maxRenderDistance`: Maximum distance to render nametags (default: 32.0)
- `customFormat`: Format string for nametags with placeholders (default: "{name}")

### Format Placeholders

- `{name}`: Player's name
- `{distance}`: Distance to player (if showDistance is enabled)
- `{health}`: Player's health (if showHealth is enabled)

Example format: `{name}{distance} - {health}HP`

## Installation

1. Install Fabric for Minecraft 1.20+
2. Install Fabric API
3. Place the mod JAR file in your `mods` folder
4. Launch the game to generate the configuration file
5. Modify the configuration file as desired

## Building

To build the mod from source:

```bash
cd nametag-manager
./gradlew build
```

The built mod JAR will be in the `build/libs` directory.