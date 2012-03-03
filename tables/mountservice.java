} else if (action.equals(Intent.ACTION_SCREEN_OFF)) {
	String state = SystemProperties.get("ro.crypto.state");
	if (state.equals("encrypted"))  {
		Slog.d(TAG, "Received screen off broadcast, and encrypted, time to wipe keys.");
		ActivityManager mAm; 
		mAm = (ActivityManager) mContext.getSystemService(Context.ACTIVITY_SERVICE);
		mConnector.doCommand("cryptfs clearmaster");
		// This isn't terribly useful - use callout to logic for what apps to secure
		mConnector.doCommand("cryptfs clearboundary 10036");
		mAm.forceStopPackage("com.socialnmobile.dictapps.notepad.color.note");
	}    
}    

