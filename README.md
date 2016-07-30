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
$ python main/main.py _YOUR\_APK\_FILE_
```
Or modify the code in the main function.

If you want an online trial, just click [http://radar.pkuos.org/](http://radar.pkuos.org/).

## Description for output

[LibRadar](https://github.com/pkumza/LibRadar) put a json format result to stdout.
That's a list braced by [] and every item stands for a library that LibRadar found.

There should be two situation for a library detected:

If the library is tagged in my database, the output may have these items as follows:

|Symbol|Stands for|Description|
|---|---|---|
|dn|Repetitions|The number of the library (of just the **same version**!)|
|ch|Link| Link for the official SDK developer guide website. I forget why I used 'ch' at the very beginning.|
|bh|B\_Hash|The hash value of the package.|
|btc|B\_Total\_Count|The total count of API.|
|btn|B\_Total\_Number|The total types of API.|
|lib|Library|Library Name|
|cpn|Current Package Name|The package name from **your given APK** that seems match this library. 'Current' means what you just uploaded.|
|csp|Current Specified Package Name|The sub-package (a part of the whole package) from your given APK that finally, exactly matched with what in the database.|
|pn|Package Name|The package name from the database that seems matched.|
|sp|Specified Package Name|The sub-package(a part of the whole package) that exactly matched with that in your APK.|
|tp|Type|The type that the library belongs to.|
|p|Permission|The permissions that the library used. It is specified by the API it used.|

If the library is not popular enough that I didn't tagged, the output will have only four items:
dn, p, pn, cpn. The meaning of them is just the same. The library is not tagged, so I cannot give you its name, but you can guess by yourself via the package name, which is not gonna be difficult if the package name is not obfuscated.

I used a A\_HASH before and it failed, so I use B\_HASH to replace that one.
cpn, csp, pn, sp can be difficult to understand. If you are confused, just use pn for the package name.
I divided the libraries into ten types:

```python
library_type = {
    "da": "Development Aid",
    "sn": "Social Network",
    "ad": "Advertisement",
    "am": "App Market",
    "ma": "Mobile Analytics",
    "pa": "Payment",
    "ui": "UI Component",
    "ge": "Game Engine",
    "ut": "Utility",
    "mp": "Map"
}
```

## Dev Environment
* JDK Version : Java 1.8.0_25

* IDE : PyCharm 4.0.3

* APKTOOL Version : 2.0.1

## Web Server Environment
* Java : 1.7.0_79

* Node.js : v0.10.37

##Update History
__version 1.3.0 (current version)__

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
