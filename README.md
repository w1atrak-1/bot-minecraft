# Minecraft 1.8.8 Attack Distance Injector

This is a Java agent that injects into Minecraft 1.8.8 to increase the minimum attack distance. The default attack distance in Minecraft 1.8.8 is 3 blocks, but this injector increases it to 6 blocks.

## How it Works

The injector uses Java instrumentation to modify Minecraft classes at runtime. It specifically targets:

- `PlayerControllerMP` - Handles attack mechanics and reach distance checks
- `Minecraft` - Main Minecraft client class that might contain reach distance settings
- Various other classes that might affect attack/reach distance

The injection is done through bytecode manipulation using Javassist library, which allows for modification of class behavior without having to decompile and recompile Minecraft itself.

## Usage

To use this injector with Minecraft 1.8.8:

```bash
java -javaagent:target/attack-distance-injector-1.0-SNAPSHOT.jar -jar Minecraft.jar
```

Or if you're using a launcher, add the following JVM argument:

```
-javaagent:target/attack-distance-injector-1.0-SNAPSHOT.jar
```

## Technical Details

The injector works by:

1. Identifying Minecraft classes that handle attack distance logic
2. Modifying distance checks to use larger values (3.0 -> 6.0 blocks)
3. Hooking into the attack/reach distance calculation methods
4. Intercepting and modifying distance comparison operations

The agent uses the Java Instrumentation API to transform classes at load time or runtime, allowing it to modify the behavior of Minecraft without changing the original jar file.

## Files

- `AttackRangeInjector.java` - Main injector class that performs bytecode manipulation
- `MinecraftInjector.java` - Alternative approach using reflection
- `ReachDistanceModifier.java` - Additional class for reach distance modification
- `MANIFEST.MF` - Contains agent configuration
- `pom.xml` - Maven build configuration

## Note

This is designed specifically for Minecraft 1.8.8 and may not work with other versions due to differences in class names and structure. Minecraft uses obfuscated class names in the release version, so the injector includes support for both deobfuscated and obfuscated names.