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

downloadCorpus <- function(url, corpus, params = list()) {
	pythonExec = "~/hcsvlab-python-tools/hcsvlab/query.py"
	args = ""
	# construct params str
	if (length(params) > 0) {
		i = 0
		for (key in names(params)) {
			args = paste(args, key, "=", formatStr(params[[key]]), sep="")
			if (i < length(params) - 1) {
				args = paste(args, ",", sep="")
			}
			i = i + 1
		}
	}
	
	sysCommand = paste("python", pythonExec, formatStr(url), formatStr(corpus), formatStr(args))
	#print(sysCommand)

	system(sysCommand)
}