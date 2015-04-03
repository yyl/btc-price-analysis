all: score clean

score:
	python scripts/parseCSV.py 1
	cd stanford-coreNLP; \
	java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,parse,sentiment -file ../data/nyt_news_only.csv -outputDirectory ../data
	python scripts/parseCSV.py 2

clean:
	rm -f data/nyt_news_only.csv
	rm -f data/nyt_news_only.csv.xml
