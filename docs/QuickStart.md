# QuickStart

## How to use LibRadar

1. Install dependencies. build-essential, python2, pip, git, redis

   Recommand to use pypy, install pypy and pypy-pip to boost LibRadar

  - Install redis
  ```bash
    $ wget http://download.redis.io/releases/redis-3.2.7.tar.gz
	$ tar xzf redis-3.2.7.tar.gz
	$ cd redis-3.2.7
	$ make
	$ apt-get install tcl
	$ make test
	$ make install
	# If you're using Linux, ignore this 'ln' line below.
	# If you're using Mac OS, link redis-server to make it runnable.
	$ ln src/redis-server /usr/bin/
  ```

1. Install modules
 - python-redis
  ```
    $ pip install redis
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

# Example

```bash
$ python LibRadar/libradar.py /Users/marchon/Downloads/ArticleNews.apk

===== RESULT: ============
----
Package: Landroid/support
Library: Android Support
Standard Package: Landroid/support
Type: Development Aid
Website: https://developer.android.com/reference/android/package-summary.html
Similarity: 2006/5254
----
Package: Landroid/support/v4
Library: Android Support v4
Standard Package: Landroid/support/v4
Type: Development Aid
Website: http://developer.android.com/reference/android/support/v4/app/package-summary.html
Similarity: 578/2529
----
Package: Landroid/support/v7
Library: Android Support v7
Standard Package: Landroid/support/v7
Type: Development Aid
Website: https://developer.android.com/reference/android/support/v7/app/package-summary.html
Similarity: 1389/2686
----
Package: Lcom/facebook
Library: Facebook
Standard Package: Lcom/facebook
Type: Social Network
Website: https://developers.facebook.com
Similarity: 1184/1226
----
Package: Lcom/google/gson
Library: Google Gson
Standard Package: Lcom/google/gson
Type: Development Aid
Website: https://github.com/google/gson
Similarity: 409/409
----
Package: Lcom/ss/squareup/okhttp
Library: OkHttp
Standard Package: Lcom/squareup/okhttp
Type: Development Aid
Website: https://github.com/square/okhttp
Similarity: 357/602
----
Package: Lcom/sina/weibo
Library: Weibo
Standard Package: Lcom/sina/weibo
Type: Social Network
Website: http://weibo.com/
Similarity: 39/806
----
Package: Lcom/slidingmenu
Library: SlidingMenu
Standard Package: Lcom/slidingmenu
Type: GUI Component
Website: https://github.com/jfeinstein10/SlidingMenu
Similarity: 10/210
----
Package: Lcom/tencent/mm
Library: Tencent Wechat
Standard Package: Lcom/tencent/mm
Type: Social Network
Website: https://open.weixin.qq.com/
Similarity: 235/235
----
Package: Lcom/umeng/analytics
Library: Umeng Analytics
Standard Package: Lcom/umeng/analytics
Type: Mobile Analytics
Website: https://www.umeng.com/analytics
Similarity: 325/325
----
Package: Lu/aly
Library: Umeng Analysis
Standard Package: Lu/aly
Type: Mobile Analytics
Website: https://www.umeng.com/
Similarity: 1624/1624
----
Package: Lorg/apache/http
Library: Apache Http
Standard Package: Lorg/apache/http
Type: Development Aid
Website: https://hc.apache.org/
Similarity: 57/57
==========================

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