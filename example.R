#######
# This simple example demonstrates how you can use the alphabase API (R version).
# 
# You can also divide different functions (downloading, model training, and uploading) into different files.
# 
# For model training and predictions uploading, you should better calculate the accuracy (or logloss, AUC) of your
# predictions first. Based on those metrics, you can choose the best ones to upload. Please do you best to automate
# the whole process.
# 
### alphabase website:
#   https://alphabase.ai/
#


# NEED TO BE CHANGED TO YOUR OWN INFO
# parameters needed for data downloading and predictions uploading
username = "iShares"
password = "ishares"
dest_dir = "/Users/iShares/Desktop/alphabase"


# load functions needed for data downloading and predictions uploading
setwd(dest_dir)
source("alphabaseAPI.R")


# dowload current round datasets
print("downloading datasets ...")
download.dataset(username, password, dest_dir)


# TODO:
# can insert you machine learning models here
# to automate your model training process after data downloading

# model Examples
print("training models ...")
for(i in seq(4)) {
	system(paste0("Rscript logisticRegression.R ", i))
}


# upload predictions after model training
print("uploading predictions ...")
for(i in seq(4)) {
	upload.prediction(username, password, paste0("abai_submission_", i, ".csv"))
}