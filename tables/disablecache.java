commit f94e3b2b5650c822e98eb83d8e6d6f38602b518a
Author: Daniel DeFreez <daniel@defreez.com>
Date:   Sat Apr 9 17:41:36 2011 -0700

    The browser cache has been disabled. 
This is a temporary, easy step toward a forensically sterile browser.
    Obviously this will need to be revisited and a more elegant solution found, where some amount of cache is kept in memory.

diff --git a/core/java/android/webkit/CacheManager.java b/core/java/android/webkit/CacheManager.java
index d171990..531062e 100644
--- a/core/java/android/webkit/CacheManager.java
+++ b/core/java/android/webkit/CacheManager.java
@@ -63,7 +63,7 @@ public final class CacheManager {
     // Limit the maximum cache file size to half of the normal capacity
     static long CACHE_MAX_SIZE = (CACHE_THRESHOLD - CACHE_TRIM_AMOUNT) / 2;
 
-    private static boolean mDisabled;
+    private static boolean mDisabled = true;
 
     // Reference count the enable/disable transaction
     private static int mRefCount;
@@ -229,7 +229,7 @@ public final class CacheManager {
         if (disabled == mDisabled) {
             return;
         }
-        mDisabled = disabled;
+        mDisabled = true;
         if (mDisabled) {
             removeAllCacheFiles();
         }
