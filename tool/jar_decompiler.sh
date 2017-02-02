# use this shell script to decompile android.jar
# thanks to http://stackoverflow.com/questions/647116/how-to-decompile-a-whole-jar-file
# you have to put `jad` into your PATH environment.
#     zachary created at 2016-12
JAR=$1
unzip -d $JAR.dir $JAR
pushd $JAR.dir
for f in `find . -name '*.class'`; do
    jad -d $(dirname $f) -s java -lnc $f
done
popd
