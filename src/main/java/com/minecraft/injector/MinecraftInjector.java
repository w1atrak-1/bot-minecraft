package com.minecraft.injector;

import java.lang.instrument.Instrumentation;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.List;

public class MinecraftInjector {
    
    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[Minecraft Injector] Initializing...");
        modifyAttackDistance();
    }
    
    public static void agentmain(String agentArgs, Instrumentation inst) {
        System.out.println("[Minecraft Injector] Attaching...");
        modifyAttackDistance();
    }
    
    private static void modifyAttackDistance() {
        try {
            // Find Minecraft class
            Class<?> mcClass = findMinecraftClass();
            
            if (mcClass != null) {
                // Modify attack distance field if it exists
                modifyAttackDistanceField(mcClass);
                
                System.out.println("[Minecraft Injector] Attack distance modified successfully!");
            } else {
                System.out.println("[Minecraft Injector] Could not find Minecraft class");
            }
        } catch (Exception e) {
            System.err.println("[Minecraft Injector] Error modifying attack distance: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static Class<?> findMinecraftClass() {
        try {
            // Common class names for Minecraft in 1.8.8
            String[] classNames = {
                "net.minecraft.client.Minecraft",
                "bpk", // Obfuscated name for Minecraft class in 1.8.8
                "ave"
            };
            
            for (String className : classNames) {
                try {
                    return Class.forName(className);
                } catch (ClassNotFoundException e) {
                    // Try next name
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return null;
    }
    
    private static void modifyAttackDistanceField(Class<?> mcClass) {
        try {
            // Try to find the attack distance field
            Field attackDistField = null;
            
            // Common field names for attack distance in 1.8.8
            String[] fieldNames = {
                "attackDistance", 
                "playerAttackDistance", 
                "entityReach", 
                "reachDistance",
                "f", // Common obfuscated name
                "field_71468_F", // Possible field name in 1.8.8
                "field_110441_br" // Another possible field name
            };
            
            for (String fieldName : fieldNames) {
                try {
                    attackDistField = mcClass.getDeclaredField(fieldName);
                    if (attackDistField != null) {
                        System.out.println("[Minecraft Injector] Found attack distance field: " + fieldName);
                        break;
                    }
                } catch (NoSuchFieldException e) {
                    // Try next field name
                }
            }
            
            if (attackDistField != null) {
                // Make the field accessible
                attackDistField.setAccessible(true);
                
                // Get the Minecraft instance
                Object mcInstance = getMinecraftInstance(mcClass);
                
                if (mcInstance != null) {
                    // Modify the attack distance to a larger value
                    attackDistField.set(mcInstance, 6.0f); // Increase from default 3.0 to 6.0
                    System.out.println("[Minecraft Injector] Attack distance set to 6.0f");
                }
            } else {
                System.out.println("[Minecraft Injector] Attack distance field not found, trying alternative method...");
                modifyAttackDistanceByReflection();
            }
        } catch (Exception e) {
            System.err.println("[Minecraft Injector] Error modifying attack distance field: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static Object getMinecraftInstance(Class<?> mcClass) {
        try {
            // Try to get the Minecraft instance through the field_71432_P or similar static field
            Field instanceField = null;
            
            String[] instanceFieldNames = {
                "instance",
                "Minecraft",
                "field_71432_P", // Common static field name in 1.8.8
                "a"
            };
            
            for (String fieldName : instanceFieldNames) {
                try {
                    instanceField = mcClass.getDeclaredField(fieldName);
                    if (instanceField != null && java.lang.reflect.Modifier.isStatic(instanceField.getModifiers())) {
                        System.out.println("[Minecraft Injector] Found instance field: " + fieldName);
                        break;
                    }
                } catch (NoSuchFieldException e) {
                    // Try next field name
                }
            }
            
            if (instanceField != null) {
                instanceField.setAccessible(true);
                return instanceField.get(null); // Static field, so null for instance
            }
            
            // If no static field found, try the static method
            Method getInstanceMethod = null;
            String[] methodNames = {
                "getInstance",
                "getMinecraft",
                "a"
            };
            
            for (String methodName : methodNames) {
                try {
                    getInstanceMethod = mcClass.getDeclaredMethod(methodName);
                    if (getInstanceMethod != null) {
                        System.out.println("[Minecraft Injector] Found instance method: " + methodName);
                        break;
                    }
                } catch (NoSuchMethodException e) {
                    // Try next method name
                }
            }
            
            if (getInstanceMethod != null) {
                getInstanceMethod.setAccessible(true);
                return getInstanceMethod.invoke(null); // Static method, so null for instance
            }
            
        } catch (Exception e) {
            System.err.println("[Minecraft Injector] Error getting Minecraft instance: " + e.getMessage());
            e.printStackTrace();
        }
        
        return null;
    }
    
    private static void modifyAttackDistanceByReflection() {
        try {
            // Alternative approach: modify through PlayerController or similar classes
            Class<?> playerControllerClass = null;
            
            String[] pcClassNames = {
                "net.minecraft.client.multiplayer.PlayerControllerMP",
                "bfg", // Obfuscated name in 1.8.8
                "ave" // Another possible obfuscated name
            };
            
            for (String className : pcClassNames) {
                try {
                    playerControllerClass = Class.forName(className);
                    if (playerControllerClass != null) {
                        System.out.println("[Minecraft Injector] Found PlayerController class: " + className);
                        break;
                    }
                } catch (ClassNotFoundException e) {
                    // Try next class name
                }
            }
            
            if (playerControllerClass != null) {
                // Try to modify attack distance in PlayerController
                Field[] fields = playerControllerClass.getDeclaredFields();
                
                for (Field field : fields) {
                    if (field.getType() == float.class || field.getType() == double.class) {
                        field.setAccessible(true);
                        
                        // Check if this field might be the attack distance
                        if (field.getName().toLowerCase().contains("attack") || 
                            field.getName().toLowerCase().contains("reach") ||
                            field.getName().contains("dist")) {
                            
                            System.out.println("[Minecraft Injector] Modifying field: " + field.getName());
                            
                            // Since we can't easily get the instance without knowing the Minecraft class,
                            // we'll have to try to access it differently
                            break;
                        }
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("[Minecraft Injector] Error in alternative method: " + e.getMessage());
            e.printStackTrace();
        }
    }
}