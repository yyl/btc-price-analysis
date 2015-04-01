all:
	cd stanford-coreNLP; \
	java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,parse,sentiment -file input.txt
	#java -cp "*" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -file input.txt;
