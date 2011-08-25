#!/bin/bash
BACKUPDIR=(/var/log/learningregistry/* /mnt/couchdb/1.0.2/*)
BACKROOT=s3://lr.backups/$1/$2
for d in ${BACKUPDIR[@]}
do
    for f in $d
    do
        s3cmd put $f $BACKROOT$f
    done
done
