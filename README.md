# LibRadar
LibRadar is an automatic tool for Android library detection.

Upload your apk file and LibRadar can detect third-party libraries in Android apps accurately and instantly.

## Features

#### Fast
Lib Radar takes just several seconds to scan an app.
#### Accurate
Lib Radar is trained with more than 1 million apps from Google Play, so this tool can find almost every popular library that the app uses.
#### Anti-Obfuscation
Many Android apps are obfuscated with obfuscator such as ProGuard, which makes it difficult to recognize a library by its package names, class names, method names and variable names.
Lib Radar is an obfuscting-free approach which uses Android APIs for library scanning.

##Usage

Use __detect.py__ under the  main directory.

Input the first parameters as the path of the target apk.

```bash
$ python main/detect.py ~/apks/sample.apk
```
Or modify the code in the main function.

If you want an online trial, just click [http://radar.pkuos.org/](http://radar.pkuos.org/).

##Dev Environment
* JDK Version : Java 1.8.0_25

* IDE : PyCharm 4.0.3

* APKTOOL Version : 2.0.1

## Web Server Environment
* Java : 1.7.0_79

* Node.js : v0.10.37

##Update History
__version 1.1.0 (current version)__

A new version with optimized code, detailed comments and simplified data.

__version 1.0.1__

Uploading bug fixed.

__version 1.0.0__ 

First complete Version with complicated code which can be used with Node.js. 
