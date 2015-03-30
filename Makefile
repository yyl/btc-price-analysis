all:
	cd stanford-coreNLP; \
	java -cp "*" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -file input.txt;
