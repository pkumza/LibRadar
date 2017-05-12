import libradar
import json
import glob

apks = glob.glob("/Volumes/banana/apks/*")

i = -1
total = 10

while i < total:
    try:
        i += 1
        print "Progress %d" % i
        apk_path = apks[i]
        lrd = libradar.LibRadar(apk_path)
        res = lrd.compare()
        print(json.dumps(res, indent=4, sort_keys=True))
        #for item in res:
        #    if item["Library"] != "Unknown" and "Standard Package" in item and "Package" in item and item["Standard Package"] != item["Package"]:
        #        print "NOT_MATCH_PACKAGE_NAME"
        #        print item["Standard Package"]
        #        print item["Package"]
    except Exception, e:
        total += 1
        print Exception,":", e