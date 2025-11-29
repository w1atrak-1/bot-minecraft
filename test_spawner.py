import random
import string
import sys
from io import StringIO
from minecraft_bot_spawner import MinecraftBotSpawner

def test_bot_spawner():
    print("Testing Minecraft Bot Spawner...")
    
    # Create spawner instance
    spawner = MinecraftBotSpawner()
    
    # Test credential generation
    print("\nTesting credential generation:")
    for i in range(5):
        username, password = spawner.generate_credentials()
        print(f"  Bot {i+1}: Username='{username}' Password='{password}'")
        # Verify length constraints
        assert 5 <= len(username) <= 10, f"Username length issue: {len(username)}"
        assert 5 <= len(password) <= 9, f"Password length issue: {len(password)}"
        # Verify no special characters
        assert username.isalnum(), f"Username has special chars: {username}"
        assert password.isalnum(), f"Password has special chars: {password}"
    
    print("\n✓ All credential generation tests passed!")
    
    # Test proxy loading
    print(f"\nLoaded {len(spawner.proxies)} proxies: {spawner.proxies}")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_bot_spawner()