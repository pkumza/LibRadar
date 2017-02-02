# LibRadar
LibRadar is an automatic tool for Android library detection.

Upload your apk file and LibRadar can detect third-party libraries in Android apps accurately and instantly.

## Features

#### Fast
LibRadar takes just several seconds to scan an app and report the list of third-party libraries used in it.
#### Accurate
LibRadar is trained with more than 1 million apps from Google Play, so it can identify virtually all popular libraries in any given Android app.
#### Anti-Obfuscation
Many Android apps are obfuscated with tools such as ProGuard, which makes it difficult to recognize a library by its package names or class names.
LibRadar is obfuscation-resilient since we use features that cannot be obfuscated, such as statistics on Android APIs.

## Usage

Use __detect.py__ under the  main directory.

Input the first parameters as the path of the target apk.

```bash
$ python LibRadar/libradar.py someapp.apk
```

~~If you want an online trial, just click http://radar.pkuos.org/~~. (Still version 1 temporarily)

## Description for output

Sorry, Docs not finished.

## Dev Environment

* PyPy Version:
```
Python 2.7.12 (aff251e54385, Nov 09 2016, 17:25:49)
[PyPy 5.6.0 with GCC 4.2.1 Compatible Apple LLVM 5.1 (clang-503.0.40)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

* Python Version (optional):
```
Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 26 2016, 12:10:39)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

* JDK Version :
```
java version "1.8.0_65"
Java(TM) SE Runtime Environment (build 1.8.0_65-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.65-b01, mixed mode)
```

* IDE :
```
PyCharm 2016.3.2
Build #PY-163.10154.50, built on December 29, 2016
Licensed to Ziang Ma
Subscription is active until September 15, 2017
For educational use only.
JRE: 1.8.0_112-release-408-b6 x86_64
JVM: OpenJDK 64-Bit Server VM by JetBrains s.r.o
```

##Update History

__version 2.0.2dev1 (current version)__

1. Lots of changes! ^_^

__version 1.3.0__

1. Ajax support.

__version 1.2.5__

1. Assert 3 parts.
2. Repair the problem "three ';' in 'tgst5.dat'".
3. Update repetition counting.
4. Merge the results of marked libs and unmarked libs.
5. Fix '/' bug.
6. Sort the result.

__version 1.2.3__

1. Add 'LData' Branch for Jingyue's research.
2. Add var RM_STATUS for smali code deleting control.
3. Modify path in function *all_over* so that there's no need to input the full path of this python script any more.
4. Replace chinese description with web address.

__version 1.2.1__

Remove lib code in smali files and zip them into a new file.

__version 1.2.0__

Modularity

__version 1.1.9__

1. Update Output Format.
2. Add library type.
3. Update library fingerprint data for better recognition.

__version 1.1.7__

1. Update library fingerprint data for better recognition.
2. Put plenty data into final output.
 -        "dn": 311 -                          Repetitions
 -        "lib": "pollfish" -                  Library
 -         "sp": "com/pollfish/f/a" -          Simplified Path
 -          "bh": 32370 -                      B_Hash
 -           "btc": 40 -                       B_Total_Call
 -            "btn": 12 -                      B_Total_Number
 -             "pn": "com/pollfish" -          Package Name
3. Permission detection of Libraries.

__version 1.1.5__

Add Permission Detection of packages.

__version 1.1.3__

1. Modified Tagged Library Data and Sorted it.
1. Remove print('*' * 60) and print('Task: '+self.tag+' Starts.')
1. Remove 'minutes' tag because it is useless.
1. Add specific time consuming tag.
 1. time_decode     = TimeRecord('Target App Decoding')
 - time_load       = TimeRecord('Lib Data Loading')
 - time_extract    = TimeRecord('Feature Extracting')
 - time_compare    = TimeRecord('Library Searching')
1. New algorithm.
 1. Sort library data.
 1. Use binary search to find the library.

__version 1.1.2__

Update and modify library data set.

__version 1.1.1__

Replace 320,000 apps data with 1,000,000 apps data.

__version 1.1.0__

A new version with optimized code, detailed comments and simplified data.

__version 1.0.1__

Uploading bug fixed.

__version 1.0.0__ 

First complete Version with complicated code which can be used with Node.js. 