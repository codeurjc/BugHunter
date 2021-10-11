VOLUME="example-1"
docker run --rm -v $VOLUME:/data -v $(pwd):/backup busybox tar cvf /backup/$VOLUME-backup-m2.tar /data