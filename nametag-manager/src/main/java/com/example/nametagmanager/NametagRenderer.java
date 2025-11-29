package com.example.nametagmanager;

import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.font.TextRenderer;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.text.Text;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.RotationAxis;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.RaycastContext;

public class NametagRenderer {
    private static Config config = Config.load();
    
    public static void init() {
        WorldRenderEvents.AFTER_TRANSLUCENT.register(NametagRenderer::onWorldRender);
    }
    
    private static void onWorldRender(WorldRenderContext context) {
        // Reload config in case it changed
        config = Config.load();
        
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.world == null || client.player == null || !config.nametagsEnabled) {
            return;
        }
        
        MatrixStack matrices = context.matrixStack();
        VertexConsumerProvider vertexConsumers = context.consumers();
        
        for (Entity entity : client.world.getEntities()) {
            if (entity instanceof PlayerEntity player && entity != client.player) {
                renderNametag(context, player, matrices, vertexConsumers);
            }
        }
    }
    
    private static void renderNametag(WorldRenderContext context, PlayerEntity player, MatrixStack matrices, VertexConsumerProvider vertexConsumers) {
        // Get player name and position
        String playerName = getModifiedNametag(player);
        Vec3d pos = player.getPos().add(0, player.getHeight() + 0.5, 0); // Position above player's head
        
        // Check if player is visible
        if (!isPlayerVisible(player)) {
            return;
        }
        
        // Additional check for line of sight if seeThroughWalls is disabled
        if (!config.seeThroughWalls && !hasLineOfSight(context, player)) {
            return;
        }
        
        // Save the current matrix state
        matrices.push();
        
        // Move to player position
        matrices.translate(pos.x - context.camera().getPos().x, 
                          pos.y - context.camera().getPos().y, 
                          pos.z - context.camera().getPos().z);
        
        // Rotate to face the camera
        matrices.multiply(RotationAxis.POSITIVE_Y.rotationDegrees(180 - context.camera().getYaw()));
        matrices.multiply(RotationAxis.POSITIVE_X.rotationDegrees(-context.camera().getPitch()));
        
        // Scale the nametag appropriately
        float scale = 0.025f;
        matrices.scale(-scale, -scale, scale);
        
        // Render the text
        MinecraftClient client = MinecraftClient.getInstance();
        TextRenderer textRenderer = client.textRenderer;
        
        int backgroundColor = 0x20000000; // Slightly transparent black background
        int textColor = 0xFFFFFF; // White text
        
        float x = -textRenderer.getWidth(playerName) / 2.0f;
        float y = 0.0f;
        
        textRenderer.draw(playerName, x, y, textColor, false, matrices.peek().getPositionMatrix(), vertexConsumers, 
                         TextRenderer.TextLayerType.NORMAL, backgroundColor, 0xF000F0);
        
        // Restore the matrix state
        matrices.pop();
    }
    
    private static String getModifiedNametag(PlayerEntity player) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null) {
            return player.getName().getString();
        }
        
        // Calculate distance if needed
        String distanceStr = "";
        if (config.showDistance) {
            double distance = client.player.distanceTo(player);
            distanceStr = String.format(" [%.1fm]", distance);
        }
        
        // Get health if needed
        String healthStr = "";
        if (config.showHealth) {
            healthStr = String.format(" %.0fHP", player.getHealth());
        }
        
        // Apply custom format
        String result = config.customFormat;
        result = result.replace("{name}", player.getName().getString());
        if (config.showDistance) {
            result = result.replace("{distance}", distanceStr);
        }
        if (config.showHealth) {
            result = result.replace("{health}", healthStr);
        }
        
        return result;
    }
    
    private static boolean isPlayerVisible(PlayerEntity player) {
        // Simple visibility check - in the future this could be more sophisticated
        // based on distance, settings, etc.
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null) {
            return false;
        }
        
        // Check distance - don't render nametags for very far players
        double distance = client.player.distanceTo(player);
        return distance <= config.maxRenderDistance;
    }
    
    private static boolean hasLineOfSight(WorldRenderContext context, PlayerEntity player) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player == null || client.world == null) {
            return false;
        }
        
        // Get the eye position of the local player and the target player
        Vec3d start = client.player.getEyePos();
        Vec3d end = player.getPos().add(0, player.getHeight() / 2, 0); // Check from the middle of the player body
        
        // Perform a raycast to check if there's a clear line of sight
        // This checks if there are any blocks between the player and the target that would block the view
        BlockHitResult result = client.world.raycast(
            new RaycastContext(
                start,
                end,
                RaycastContext.ShapeType.VISUAL,
                RaycastContext.FluidHandling.NONE,
                client.player
            )
        );
        
        // If the raycast hit something before reaching the target player, there's no line of sight
        return result.getType() == HitResult.Type.MISS;
    }
}