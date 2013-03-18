# example script
# source(~/Rscripts/hcsvlab_commands.R)
# url = "http://gsw1-hcsvlab-test3-vm.intersect.org.au/documents.json"
# corpus_dir = "my_corpus"
# params = list()
# downloadCorpus(url, corpus_dir, params)

formatStr <- function(s) {
	if (s == "") return("")
	return (paste('"', s, '"', sep=""))
}

addLine <- function(s1, s2, sep=";") {
	return (paste(s1, sep, s2))
}

downloadCorpus <- function(url, corpus_dir, params = list()) {
	python_cmd = "from hcsvlab.query import Query"
	python_cmd = addLine(python_cmd, paste("query = Query('", url, "')", sep=""))
	python_cmd = addLine(python_cmd, "params = {}")
	# construct args
	if (length(params) > 0) {
		for (key in names(params)) {
			python_cmd = addLine(python_cmd, paste("params['", key, "']='", params[[key]], "'", sep=""))
		}
	}
	python_cmd = addLine(python_cmd, "query.query(params)")
	python_cmd = addLine(python_cmd, paste("query.download('", corpus_dir, "')", sep=""))
	print(paste("python -c", formatStr(python_cmd)))

	system(paste("python -c", formatStr(python_cmd)))
}