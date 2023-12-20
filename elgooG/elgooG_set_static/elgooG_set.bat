netsh interface ip set dns name="Local Area Connection" static 127.0.0.1
netsh interface ip add dns name="Local Area Connection" 8.8.8.8 index=2