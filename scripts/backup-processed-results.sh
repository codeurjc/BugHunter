project=$1

mkdir -p tmp/processed-results/

tar -czvf tmp/processed-results/procesed-results.tar.gz analysis/results/

rclone copy tmp/processed-results/procesed-results.tar.gz OneDrive:/Research/BugsBirth/Backup/RegressionSeeker/    