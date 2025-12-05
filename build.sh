#!/bin/bash

echo "Building Minecraft Attack Distance Injector..."

# Check if Maven is installed
if ! [ -x "$(command -v mvn)" ]; then
  echo "Error: Maven is not installed." >&2
  exit 1
fi

# Build the project
mvn clean package

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "The injector JAR is located at: target/attack-distance-injector-1.0-SNAPSHOT.jar"
    echo ""
    echo "To use the injector with Minecraft 1.8.8, run Minecraft with the following JVM argument:"
    echo "java -javaagent:target/attack-distance-injector-1.0-SNAPSHOT.jar -jar Minecraft.jar"
else
    echo "Build failed!"
    exit 1
fi