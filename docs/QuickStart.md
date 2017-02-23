# QuickStart

## How to use LibRadar

1. Install dependencies. build-essential, python2, pip, git, redis

   Recommend to use pypy, install pypy and pypy-pip to boost LibRadar

  - Install redis>=3.2
  ```bash
    $ wget http://download.redis.io/releases/redis-3.2.7.tar.gz
	$ tar xzf redis-3.2.7.tar.gz
	$ cd redis-3.2.7
	$ make
	$ apt-get install tcl
	$ make test
	$ make install
  ```

1. Install modules

  ```
    $ pip install requirements.txt
  ```

1. Download code

 * Github Release (Recommanded)
 <br/>
 Click [https://github.com/pkumza/LibRadar/releases](https://github.com/pkumza/LibRadar/releases)
 <br/>
 Download zip or tar.gz, then extract code from it.

 - Github
   ```bash
   $ git clone https://github.com/pkumza/LibRadar
   ```

 - Pypi

   Download tar.gz code from https://pypi.python.org/pypi/LibRadar/ and extract the file into your work directory.
   Do not use pip install because I didn't include data file into the code, as libradar will get error that it could not
   find data file.

1. Download LibRadarData.rdb and run redis-server
  https://raw.githubusercontent.com/pkumza/LibRadar/LR_DataSet_1/Data/IntermediateData/LibRadarData.rdb

  ```bash
  $ wget https://raw.githubusercontent.com/pkumza/LibRadar/LR_DataSet_1/Data/IntermediateData/LibRadarData.rdb
  $ cd LibRadar
  $ vi tool/redis.conf.
  (find "dir /Users/marchon/Projects/Databases" and change it into your LibRadarData.rdb path.)

  $ redis-server tool/redis.conf &
  ```
1. Use LibRadar to detect libraries.

  ```bash
  $ python LibRadar/libradar.py someapp.apk
  ```

# Example (Version 2.1.1)

```bash
$ python LibRadar/libradar.py /Users/marchon/Downloads/ArticleNews.apk
[
    {
        "Library": "Android Support",
        "Package": "Landroid/support",
        "Permission": [
            "android.permission.BACKUP",
            "android.permission.BLUETOOTH_ADMIN",
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET",
            "android.permission.WAKE_LOCK"
        ],
        "Popularity": "18",
        "Match Ratio": "4/3260",
        "Standard Package": "Landroid/support",
        "Type": "Development Aid",
        "Website": "https://developer.android.com/reference/android/package-summary.html"
    },
    {
        "Library": "Android Support v4",
        "Package": "Landroid/support/v4",
        "Permission": [
            "android.permission.BACKUP",
            "android.permission.BLUETOOTH_ADMIN",
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET",
            "android.permission.WAKE_LOCK"
        ],
        "Popularity": "18",
        "Match Ratio": "4/2700",
        "Standard Package": "Landroid/support/v4",
        "Type": "Development Aid",
        "Website": "http://developer.android.com/reference/android/support/v4/app/package-summary.html"
    },
    {
        "Library": "Google Mobile Services",
        "Package": "Lcom/google/android/gms",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL"
        ],
        "Popularity": "15",
        "Match Ratio": "17/227",
        "Standard Package": "Lcom/google/android/gms",
        "Type": "Development Aid",
        "Website": "https://developers.google.com/android/reference/com/google/android/gms/package-summary"
    },
    {
        "Library": "ZXing ('Zebra Crossing')",
        "Package": "Lcom/google/zxing",
        "Permission": [],
        "Popularity": 3,
        "Match Ratio": "3/3",
        "Standard Package": "Lcom/google/zxing",
        "Type": "Development Aid",
        "Website": "https://github.com/zxing/zxing"
    },
    {
        "Library": "Tencent Login",
        "Package": "Lcom/tencent/tauth",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL"
        ],
        "Popularity": 2,
        "Match Ratio": "20/20",
        "Standard Package": "Lcom/tencent/tauth",
        "Type": "Social Network",
        "Website": "http://wiki.open.qq.com/wiki/mobile/Android_SDK"
    },
    {
        "Library": "Tencent Login",
        "Package": "Lcom/tencent/tauth",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL"
        ],
        "Popularity": "2",
        "Match Ratio": "20/20",
        "Standard Package": "Lcom/tencent/t",
        "Type": "Social Network",
        "Website": "http://t.qq.com"
    },
    {
        "Library": "Tencent Login",
        "Package": "Lcom/tencent/connect",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL"
        ],
        "Popularity": 1,
        "Match Ratio": "53/53",
        "Standard Package": "Lcom/tencent/connect",
        "Type": "Social Network",
        "Website": "https://connect.qq.com"
    },
    {
        "Library": "Tencent Login",
        "Package": "Lcom/tencent/open",
        "Permission": [
            "android.permission.DUMP"
        ],
        "Popularity": "6",
        "Match Ratio": "4/100",
        "Standard Package": "Lcom/tencent/open",
        "Type": "Social Network",
        "Website": "http://wiki.open.qq.com/wiki/mobile/Android_SDK"
    },
    {
        "Library": "Weibo",
        "Package": "Lcom/sina/weibo",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET"
        ],
        "Popularity": "1",
        "Match Ratio": "25/323",
        "Standard Package": "Lcom/sina/weibo",
        "Type": "Social Network",
        "Website": "http://weibo.com/"
    }
]

```

## How to develop LibRadar

#### For Professional use

1. Install LibRadar from [pypi](https://pypi.python.org/pypi/LibRadar) or download the code from [Github](http://github.com/pkumza/LibRadar).

2. Get some dependency.
 - Install Java Runtime Environment. If you already installed jre, ignore this.
 - Install JAD.
 - Install Redis.

3. Get android.jar from Android SDK and place them into $Project_HOME$/Data/RawData, Run APIDict.py

4. Change the apk folder name and run job_dispatching.py

PS: Change variables in _settings.py if you need.