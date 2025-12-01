-- Sample Lua script for Roblox
print("Hello from Roblox Ezecutor!")

-- Example: Create a part in the workspace
local part = Instance.new("Part")
part.Name = "EzecutorPart"
part.Size = Vector3.new(4, 4, 4)
part.Position = Vector3.new(0, 10, 0)
part.Anchored = true
part.BrickColor = BrickColor.new("Really blue")
part.Parent = workspace

-- Example: Create a message in the chat
game:GetService("StarterGui"):SetCore("ChatMakeSystemMessage", {
    Text = "Script executed via Roblox Ezecutor!";
    Color = Color3.new(0, 1, 0);
    Font = Enum.Font.SourceSansBold;
    FontSize = Enum.FontSize.Size24;
})

print("Script executed successfully!")