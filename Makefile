all: bitcoin clean

bitcoin:
	python scripts/parseCSV.py 1 nyt_bitcoin.csv
	cd stanford-coreNLP; \
	java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,parse,sentiment -file ../data/news_only_nyt_bitcoin.csv -outputDirectory ../data
	python scripts/parseCSV.py 2 nyt_bitcoin.csv

clean:
	rm -f data/news_only_nyt_bitcoin.csv
	rm -f data/news_only_nyt_bitcoin.csv.xml
