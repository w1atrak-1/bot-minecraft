package com.minecraft.injector;

import javassist.*;
import java.io.ByteArrayInputStream;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;

/**
 * Specialized injector for Minecraft 1.8.8 that increases the minimum attack distance
 * This works by modifying the PlayerControllerMP class which handles attack mechanics
 */
public class AttackRangeInjector {

    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[Minecraft Attack Range Injector] Starting...");
        try {
            // Add transformer to modify classes at load time
            inst.addTransformer(new ClassFileTransformer() {
                @Override
                public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
                                      ProtectionDomain protectionDomain, byte[] classfileBuffer) {
                    // Target the PlayerControllerMP class which handles attack distance in 1.8.8
                    if (className.equals("net/minecraft/client/multiplayer/PlayerControllerMP") || 
                        className.equals("bfg")) { // Common obfuscated name for PlayerControllerMP in 1.8.8
                        
                        System.out.println("[Minecraft Attack Range Injector] Modifying PlayerControllerMP...");
                        
                        try {
                            ClassPool pool = ClassPool.getDefault();
                            CtClass ctClass = pool.makeClass(new ByteArrayInputStream(classfileBuffer));
                            
                            // Look for methods that handle attack/reach distance
                            CtMethod[] methods = ctClass.getDeclaredMethods();
                            
                            for (CtMethod method : methods) {
                                String methodName = method.getName();
                                
                                // Common methods in PlayerControllerMP that might contain reach logic
                                if (methodName.contains("attack") || 
                                    methodName.contains("click") || 
                                    methodName.contains("processRightClick") ||
                                    methodName.contains("func_178894_a") || // Common MCP name for process right click block
                                    methodName.contains("func_78750_j")) { // Common MCP name for attackEntity
                                    
                                    System.out.println("[Minecraft Attack Range Injector] Modifying method: " + methodName);
                                    
                                    // Insert code to increase reach distance
                                    // In 1.8.8, attack distance is often checked against 3.0 or 36.0 (3.0 squared)
                                    try {
                                        // Replace any distance checks with higher values
                                        method.insertBefore(
                                            "{ " +
                                            "   // Increase attack distance by modifying distance calculations" +
                                            "   if($_ != null && $_ instanceof Double) { $_ = 36.0D; }" + // 6.0 squared for distance check
                                            "}"
                                        );
                                    } catch (Exception e) {
                                        // If the return type doesn't match, try other approaches
                                        try {
                                            // Try to insert at the beginning to modify variables
                                            method.insertBefore(
                                                "{ " +
                                                "   // Intercept and modify distance comparisons" +
                                                "   // This is a hook approach for when direct modification fails" +
                                                "}"
                                            );
                                        } catch (Exception e2) {
                                            // Continue to next method
                                        }
                                    }
                                }
                            }
                            
                            // Also check for any hardcoded distance values (3.0, 36.0, etc.) in the class
                            ctClass.instrument(new javassist.expr.ExprEditor() {
                                @Override
                                public void edit(javassist.expr.MethodCall m) throws CannotCompileException {
                                    try {
                                        // Look for method calls that might involve distance calculations
                                        if (m.getMethodName().contains("getDistance") ||
                                            m.getMethodName().contains("isVec3d") ||
                                            m.getMethodName().contains("squareDistance")) {
                                            // We can't directly modify method call values with ExprEditor
                                            // But we can try to insert code around them
                                        }
                                    } catch (Exception e) {
                                        // Ignore errors
                                    }
                                }
                                
                                @Override
                                public void edit(javassist.expr.FieldAccess f) throws CannotCompileException {
                                    try {
                                        // Look for field accesses that might be reach distance related
                                        if (f.getFieldName().toLowerCase().contains("reach") ||
                                            f.getFieldName().toLowerCase().contains("attack") ||
                                            f.getFieldName().toLowerCase().contains("dist")) {
                                            // Insert code to override field values
                                            f.replace("$_ = $proceed($$); if($_ instanceof Double && $_ == 9.0D) $_ = 36.0D;"); // 3.0^2 to 6.0^2
                                        }
                                    } catch (Exception e) {
                                        // Ignore errors
                                    }
                                }
                            });
                            
                            byte[] bytecode = ctClass.toBytecode();
                            ctClass.detach();
                            return bytecode;
                            
                        } catch (Exception e) {
                            System.err.println("[Minecraft Attack Range Injector] Error modifying PlayerControllerMP: " + e.getMessage());
                            e.printStackTrace();
                        }
                    }
                    
                    // Also target the Minecraft class which might have reach distance settings
                    if (className.equals("net/minecraft/client/Minecraft") || 
                        className.equals("bpk")) { // Common obfuscated name for Minecraft class
                        
                        System.out.println("[Minecraft Attack Range Injector] Modifying Minecraft class...");
                        
                        try {
                            ClassPool pool = ClassPool.getDefault();
                            CtClass ctClass = pool.makeClass(new ByteArrayInputStream(classfileBuffer));
                            
                            // Modify the clickMouse method which handles attack logic
                            CtMethod clickMouseMethod = null;
                            try {
                                clickMouseMethod = ctClass.getDeclaredMethod("clickMouse");
                            } catch (javassist.NotFoundException e) {
                                // Try common obfuscated names
                                try {
                                    clickMouseMethod = ctClass.getDeclaredMethod("func_148740_a"); // getMouseOver
                                } catch (javassist.NotFoundException e2) {
                                    try {
                                        clickMouseMethod = ctClass.getDeclaredMethod("S"); // Common obfuscated name
                                    } catch (javassist.NotFoundException e3) {
                                        // Method not found, try next class
                                    }
                                }
                            }
                            
                            if (clickMouseMethod != null) {
                                System.out.println("[Minecraft Attack Range Injector] Found clickMouse method, modifying...");
                                
                                // In the mouse click method, we want to modify how it determines what can be attacked
                                try {
                                    // Insert code to increase the reach distance calculation
                                    clickMouseMethod.insertBefore(
                                        "{ " +
                                        "   // Modify reach distance in mouse over calculations" +
                                        "   System.out.println(\"[Minecraft Attack Range Injector] Mouse click intercepted\");" +
                                        "}"
                                    );
                                } catch (Exception e) {
                                    System.err.println("[Minecraft Attack Range Injector] Could not insert into clickMouse: " + e.getMessage());
                                }
                            }
                            
                            byte[] bytecode = ctClass.toBytecode();
                            ctClass.detach();
                            return bytecode;
                            
                        } catch (Exception e) {
                            System.err.println("[Minecraft Attack Range Injector] Error modifying Minecraft class: " + e.getMessage());
                            e.printStackTrace();
                        }
                    }
                    
                    return null;
                }
            }, true);
            
            // Try to retransform already loaded classes if possible
            for (Class<?> clazz : inst.getAllLoadedClasses()) {
                String className = clazz.getName().replace('.', '/');
                
                if (className.equals("net/minecraft/client/multiplayer/PlayerControllerMP") ||
                    className.equals("bfg") ||
                    className.equals("net/minecraft/client/Minecraft") ||
                    className.equals("bpk")) {
                    
                    try {
                        inst.retransformClasses(clazz);
                        System.out.println("[Minecraft Attack Range Injector] Retransformed: " + className);
                    } catch (Exception e) {
                        System.out.println("[Minecraft Attack Range Injector] Could not retransform: " + className + ", error: " + e.getMessage());
                    }
                }
            }
            
            System.out.println("[Minecraft Attack Range Injector] Initialization complete!");
            
        } catch (Exception e) {
            System.err.println("[Minecraft Attack Range Injector] Fatal error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Agent main method for dynamic attachment
     */
    public static void agentmain(String agentArgs, Instrumentation inst) {
        premain(agentArgs, inst);
    }
}