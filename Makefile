all:
	python scripts/parseCSV.py 1
	cd stanford-coreNLP; \
	java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,parse,sentiment -file ../data/nyt_news.csv -outputDirectory ../data
	python scripts/parseCSV.py 2

clean:
	rm data/nyt_news.csv
	rm data/nyt_news.csv.xml
