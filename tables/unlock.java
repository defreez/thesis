private void verifyPasswordAndUnlock() {
	String entry = mPasswordEntry.getText().toString();
	if (mLockPatternUtils.checkPassword(entry)) {
