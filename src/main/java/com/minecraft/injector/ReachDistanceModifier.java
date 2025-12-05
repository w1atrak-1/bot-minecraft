package com.minecraft.injector;

import javassist.*;

import java.io.IOException;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;

/**
 * A class transformer that modifies Minecraft's reach distance in version 1.8.8
 */
public class ReachDistanceModifier implements ClassFileTransformer {

    private static final float NEW_REACH_DISTANCE = 6.0f; // New reach distance
    private static final float ORIGINAL_REACH_DISTANCE = 3.0f; // Original reach distance in 1.8.8

    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[Minecraft Reach Modifier] Loading...");
        inst.addTransformer(new ReachDistanceModifier(), true);
        
        try {
            // Try to transform the classes immediately if they're already loaded
            for (Class<?> clazz : inst.getAllLoadedClasses()) {
                String className = clazz.getName();
                
                // Check for classes related to attack/reach mechanics
                if (className.contains("Minecraft") || 
                    className.contains("PlayerController") || 
                    className.contains("EntityPlayerSP")) {
                    
                    try {
                        inst.retransformClasses(clazz);
                        System.out.println("[Minecraft Reach Modifier] Transformed class: " + className);
                    } catch (Exception e) {
                        System.out.println("[Minecraft Reach Modifier] Could not transform class: " + className + ", error: " + e.getMessage());
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("[Minecraft Reach Modifier] Error during transformation: " + e.getMessage());
            e.printStackTrace();
        }
    }

    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
                           ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
        
        try {
            // Only modify classes we care about
            if (shouldModifyClass(className)) {
                System.out.println("[Minecraft Reach Modifier] Attempting to modify: " + className);
                
                ClassPool pool = ClassPool.getDefault();
                CtClass ctClass = pool.makeClass(new java.io.ByteArrayInputStream(classfileBuffer));
                
                // Look for methods that might handle reach distance
                CtMethod[] methods = ctClass.getDeclaredMethods();
                
                for (CtMethod method : methods) {
                    // Modify methods that might contain reach distance logic
                    if (methodContainsReachLogic(method)) {
                        System.out.println("[Minecraft Reach Modifier] Found method with reach logic: " + method.getName());
                        
                        // Insert code at the beginning of the method to modify reach distance
                        String src = "{ $_ = " + NEW_REACH_DISTANCE + "F; }";
                        
                        // Try to insert code at various points
                        try {
                            method.insertBefore("if(true) { $_ = " + NEW_REACH_DISTANCE + "F; }");
                        } catch (Exception e) {
                            try {
                                method.insertAfter("if($_ instanceof Float || $_ instanceof Double) { $_ = " + NEW_REACH_DISTANCE + "F; }");
                            } catch (Exception e2) {
                                // Continue to next method if insertion fails
                            }
                        }
                    }
                }
                
                // Also look for fields related to reach distance
                CtField[] fields = ctClass.getDeclaredFields();
                for (CtField field : fields) {
                    if (isReachDistanceField(field)) {
                        System.out.println("[Minecraft Reach Modifier] Found reach distance field: " + field.getName());
                        // We can't directly modify field values using Javassist in this context
                        // Instead, we'll focus on modifying the methods that use these fields
                    }
                }
                
                byte[] transformedBytecode = ctClass.toBytecode();
                ctClass.detach();
                return transformedBytecode;
            }
        } catch (Exception e) {
            System.err.println("[Minecraft Reach Modifier] Error transforming class " + className + ": " + e.getMessage());
        }
        
        return null; // Return null to indicate no transformation occurred
    }

    /**
     * Determines if a class should be modified
     */
    private boolean shouldModifyClass(String className) {
        // These are common class names in Minecraft 1.8.8 that might contain reach distance logic
        String[] targetClasses = {
            "net.minecraft.client.Minecraft",
            "net.minecraft.client.multiplayer.PlayerControllerMP",
            "net.minecraft.entity.player.EntityPlayer",
            "net.minecraft.client.entity.EntityPlayerSP",
            "net.minecraft.client.network.NetHandlerPlayClient",
            "bpk",  // Obfuscated Minecraft class
            "bfg",  // Obfuscated PlayerControllerMP
            "yz",   // Obfuscated EntityPlayer
            "vg"    // Obfuscated EntityPlayerSP
        };
        
        for (String targetClass : targetClasses) {
            if (className.equals(targetClass.replace('.', '/'))) {
                return true;
            }
        }
        
        // Also include any class that seems to be related to attacking/hitting
        return className.toLowerCase().contains("minecraft") || 
               className.toLowerCase().contains("player") || 
               className.toLowerCase().contains("controller") ||
               className.toLowerCase().contains("attack") ||
               className.toLowerCase().contains("hit");
    }

    /**
     * Checks if a method likely contains reach distance logic
     */
    private boolean methodContainsReachLogic(CtMethod method) {
        try {
            String methodSource = method.getMethodInfo().toString();
            
            // Look for keywords that suggest reach distance logic
            return method.getName().toLowerCase().contains("attack") ||
                   method.getName().toLowerCase().contains("reach") ||
                   method.getName().toLowerCase().contains("interact") ||
                   method.getName().toLowerCase().contains("hit") ||
                   method.getName().toLowerCase().contains("cansee") ||
                   method.getName().toLowerCase().contains("distance") ||
                   methodSource.toLowerCase().contains("3.0") ||  // Default reach distance
                   methodSource.toLowerCase().contains("reach") ||
                   methodSource.toLowerCase().contains("attack");
        } catch (Exception e) {
            // If we can't read the method info, assume it might contain reach logic
            return true;
        }
    }

    /**
     * Checks if a field is likely the reach distance field
     */
    private boolean isReachDistanceField(CtField field) {
        try {
            String fieldName = field.getName().toLowerCase();
            String fieldType = field.getFieldInfo2().getDescriptor();
            
            // Check if it's a float/double field with reach-related name
            return (fieldType.contains("F") || fieldType.contains("D")) && // F=float, D=double
                   (fieldName.contains("reach") || 
                    fieldName.contains("attack") || 
                    fieldName.contains("dist") ||
                    fieldName.contains("range"));
        } catch (Exception e) {
            return false;
        }
    }
}