# -*- coding: utf-8 -*-

import os

import oss2

# 以下代码展示了文件下载的用法，如下载文件、范围下载、断点续传下载等。


# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。
access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAI19YfqOSkHpRW')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'pmxBQkjnHYmnTmoExeG5w7Vdk4laMK')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'lxapk')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')

# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param

# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

key = '91/BreathTest.Chinese/fd74b020422f21b085fb3adf9f1056c9-80189abbe9218bf73fdeea7b86f64cf8c248262f6be6a2d7f5b3a4781be218a5.apk'

filename='bc.apk'

"""
文件下载
"""

def f2(a, b):
    print("F2")
    print a
    print b
# 下载到本地文件
result = bucket.get_object_to_file(key, filename, progress_callback=f2)
print("F1")


"""import urllib
import urllib2

url = 'http://lxapk.oss-cn-beijing.aliyuncs.com/91/BreathTest.Chinese/fd74b020422f21b085fb3adf9f1056c9-80189abbe9218bf73fdeea7b86f64cf8c248262f6be6a2d7f5b3a4781be218a5.apk/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

values = None
headers = {'Authorization': 'LTAI19YfqOSkHpRW:pmxBQkjnHYmnTmoExeG5w7Vdk4laMK'}
data = None
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
"""