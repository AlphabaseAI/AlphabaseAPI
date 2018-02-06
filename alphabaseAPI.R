#######
# Functions for data downloading
# and predictions uploading
#
require(httr)

download.dataset <- function(username, password, path=".") {
	r <- POST('https://alphabase.ai/download_API.php', body=list(username=username, password=password))
	bin <- content(r, "raw")
	writeBin(bin, file.path(path, ".abai_temp"))
	unzip(file.path(path, ".abai_temp"), exdir=file.path(path, "alphabase_dataset/"))
	file.remove(file.path(path, ".abai_temp"))
}

upload.prediction <- function(username, password, submission_path) {
	require(httr)
	r <- POST('https://alphabase.ai/upload_API.php', body=list(username=username,password=password,fileToUpload=upload_file(submission_path)))
	bin <- content(r, "text", encoding = "UTF-8")
	return(bin)
}