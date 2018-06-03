# QuickStart

## How to use LibRadar

### Lite Version Online! (The lite version can meet most needs)

1. Download Code from lite version repo.
 - Github
   ```bash
   $ git clone https://github.com/pkumza/LiteRadar
   ```

2. Download Feature File

  Download lite_datasetfile, then move it into LiteRadar/LiteRadar/Data directory.

  [Mirror 1 Github](https://github.com/pkumza/Data_for_LibRadar/blob/master/lite_dataset_10.csv)

  [Mirror 2 Aliyun CN](http://lxwiki.oss-cn-beijing.aliyuncs.com/lite_dataset_10.csv)

3. Use LibRadar to detect libraries.

  ```bash
  $ python literadar.py someapp.apk
  ```

### Ordinary Version

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

2. Install modules

  ```
    $ pip install requirements.txt
  ```

3. Download code

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

4. Download LibRadarData.rdb and run redis-server

  - [~Dropbox Link old~](https://www.dropbox.com/s/w31gig6msdo3cdy/dump-20170515-shrink.rdb.tar.gz?dl=0)
  - [Dropbox Link](https://www.dropbox.com/s/ljtzw74twt8xgy6/d.tar.gz?dl=0)

  ```bash
  $ vi LibRadar/tool/redis.conf.
  (
    find "dir /Users/marchon/Projects/Databases" and change it into your rdb path.
    find "dbfilename" and change it into your rdb filename.
  )

  $ redis-server tool/redis.conf
  ```

5. Use LibRadar to detect libraries.

  ```bash
  $ python libradar.py someapp.apk
  ```

# Example (Version 2.1.1)

```bash
$ python LibRadar/LibRadar/libradar.py happy.apk
[
    {
        "Library": "Android Support v4",
        "Match Ratio": "6777/6777",
        "Package": "Landroid/support/v4",
        "Permission": [
            "android.permission.BACKUP",
            "android.permission.BLUETOOTH_ADMIN",
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET",
            "android.permission.WAKE_LOCK",
            "android.permission.WRITE_SECURE_SETTINGS"
        ],
        "Popularity": 1610,
        "Standard Package": "Landroid/support/v4",
        "Type": "Development Aid",
        "Website": "http://developer.android.com/reference/android/support/v4/app/package-summary.html"
    },
    {
        "Library": "Android Support v7",
        "Match Ratio": "3111/3111",
        "Package": "Landroid/support/v7",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET",
            "android.permission.MANAGE_APP_TOKENS"
        ],
        "Popularity": 2,
        "Standard Package": "Landroid/support/v7",
        "Type": "Development Aid",
        "Website": "https://developer.android.com/reference/android/support/v7/app/package-summary.html"
    },
    {
        "Library": "Bolts Base Library",
        "Match Ratio": "325/325",
        "Package": "Lbolts",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET"
        ],
        "Popularity": 3378,
        "Standard Package": "Lbolts",
        "Type": "Development Aid",
        "Website": "https://github.com/BoltsFramework/Bolts-Android"
    },
    {
        "Library": "Amazon AWS",
        "Match Ratio": "3673/3673",
        "Package": "Lcom/amazonaws",
        "Permission": [
            "android.permission.DUMP"
        ],
        "Popularity": 3,
        "Standard Package": "Lcom/amazonaws",
        "Type": "Development Aid",
        "Website": "http://mvnrepository.com/artifact/com.amazonaws"
    },
    {
        "Library": "Google Mobile Services",
        "Match Ratio": "26342/26344",
        "Package": "Lcom/google/android/gms",
        "Permission": [
            "android.permission.BACKUP",
            "android.permission.BLUETOOTH_ADMIN",
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET",
            "android.permission.WAKE_LOCK",
            "android.permission.WRITE_SECURE_SETTINGS"
        ],
        "Popularity": "8619",
        "Standard Package": "Lcom/google/android/gms",
        "Type": "Development Aid",
        "Website": "https://developers.google.com/android/reference/com/google/android/gms/package-summary"
    },
    {
        "Library": "Google Gson",
        "Match Ratio": "390/390",
        "Package": "Lcom/google/gson",
        "Permission": [],
        "Popularity": 7366,
        "Standard Package": "Lcom/google/gson",
        "Type": "Development Aid",
        "Website": "https://github.com/google/gson"
    },
    {
        "Library": "Google Ads",
        "Match Ratio": "47/47",
        "Package": "Lcom/google/ads",
        "Permission": [
            "android.permission.DUMP"
        ],
        "Popularity": 23586,
        "Standard Package": "Lcom/google/ads",
        "Type": "Advertisement",
        "Website": "https://www.google.com/ads/"
    },
    {
        "Library": "Firebase",
        "Match Ratio": "554/554",
        "Package": "Lcom/google/firebase",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.WRITE_SECURE_SETTINGS"
        ],
        "Popularity": 14,
        "Standard Package": "Lcom/google/firebase",
        "Type": "Development Aid",
        "Website": "http://firebase.com"
    },
    {
        "Library": "Facebook",
        "Match Ratio": "3758/3758",
        "Package": "Lcom/facebook",
        "Permission": [
            "android.permission.DUMP",
            "android.permission.INTERACT_ACROSS_USERS",
            "android.permission.INTERACT_ACROSS_USERS_FULL",
            "android.permission.INTERNET"
        ],
        "Popularity": 54,
        "Standard Package": "Lcom/facebook",
        "Type": "Social Network",
        "Website": "https://developers.facebook.com"
    },
    {
        "Library": "Google Play",
        "Match Ratio": "119/119",
        "Package": "Lcom/android/vending",
        "Permission": [
            "android.permission.DUMP"
        ],
        "Popularity": 44625,
        "Standard Package": "Lcom/android/vending",
        "Type": "App Market",
        "Website": "https://play.google.com"
    },
    {
        "Library": "Unknown",
        "Package": "Landroid/support/graphics",
        "Popularity": 1525,
        "Standard Package": "Landroid/support/graphics",
        "Weight": 299
    },
    {
        "Library": "Unknown",
        "Package": "Landroid/support/customtabs",
        "Popularity": 1805,
        "Standard Package": "Landroid/support/customtabs",
        "Weight": 221
    },
    {
        "Library": "Unknown",
        "Package": "Lcom/adcolony",
        "Popularity": 221,
        "Standard Package": "Lcom/adcolony",
        "Weight": 3602
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
