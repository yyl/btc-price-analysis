all:
	java -cp "./stanford-coreNLP/*" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -file stanford-coreNLP/input.txt
