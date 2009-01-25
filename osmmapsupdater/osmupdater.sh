#!/bin/sh

osm="/home/root/Maps/OSM/"


cd $osm

echo "searching files for update"

list=`find ./ | grep png`


count=`find ./ | grep png | wc -l`

echo "found: "$count" files to chk"


rm /tmp/osm.png

update=0
fileTest=0
for i in $list
do

    val=`cat /tmp/OSMupdate_state | grep OSMupdate`
    if [ $val == "OSMupdate" ]
    then
	c=0
    else
	echo "no command to run"
	exit
    fi

    fileTest=`expr $fileTest + 1`
    
    i=${i:1}
    i=${i:1}
    
    hdFilemd5=`md5sum $i | awk '{print $1}'`
    #echo "URL: http://a.tile.openstreetmap.org/"$i" -O osm.png"
    rm /tmp/osm.png 2> /dev/null
    wget -O /tmp/osm.png "http://c.tile.openstreetmap.org/"$i > /dev/null 2> /dev/null
    
    tmpFilemd5=`md5sum /tmp/osm.png | awk '{print $1}'`

    fileTest2=$fileTest"00"
    percent=`expr $fileTest2 / $count`
    
    if [ $hdFilemd5 == $tmpFilemd5 ]
    then
	update=`expr $update + 1`
	cp /tmp/osm.png $i
    else
	c=0
    fi
    
    uPercent=$update"00"
    uPercent=`expr $uPercent / $fileTest`
    
    echo "file name: "$i"<br>files chk: "$fileTest" / "$count"<br>done: "$percent" %<br>upgradet files: "$update"<br>upgradet: "$uPercent" %"
    

done

echo "DONE"