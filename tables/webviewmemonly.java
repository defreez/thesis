--- a/core/java/android/webkit/WebViewDatabase.java
+++ b/core/java/android/webkit/WebViewDatabase.java
@@ -180,16 +180,7 @@ public class WebViewDatabase {
     public static synchronized WebViewDatabase getInstance(Context context) {
         if (mInstance == null) {
             mInstance = new WebViewDatabase();
-            try {
-                mDatabase = context
-                        .openOrCreateDatabase(DATABASE_FILE, 0, null);
-            } catch (SQLiteException e) {
-                // try again by deleting the old db and create a new one
-                if (context.deleteDatabase(DATABASE_FILE)) {
-                    mDatabase = context.openOrCreateDatabase(DATABASE_FILE, 0,
-                            null);
-                }
-            }
+            mDatabase = SQLiteDatabase.create(null);
 
             // mDatabase should not be null, 
             // the only case is RequestAPI test has problem to create db 
@@ -209,16 +200,7 @@ public class WebViewDatabase {
                 mDatabase.setLockingEnabled(false);
             }
 
-            try {
-                mCacheDatabase = context.openOrCreateDatabase(
-                        CACHE_DATABASE_FILE, 0, null);
-            } catch (SQLiteException e) {
-                // try again by deleting the old db and create a new one
-                if (context.deleteDatabase(CACHE_DATABASE_FILE)) {
-                    mCacheDatabase = context.openOrCreateDatabase(
-                            CACHE_DATABASE_FILE, 0, null);
-                }
-            }
+            mCacheDatabase = SQLiteDatabase.create(null);
