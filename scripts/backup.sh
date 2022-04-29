project=$1

mkdir -p tmp/results/

tar -czvf tmp/results/$project-results.tar.gz results/$project/

rclone copy tmp/results/$project-results.tar.gz OneDrive:/Research/BugsBirth/Backup/RegressionSeeker/Marzo-2022/    