#!/usr/bin/python

import pandas as pd
import datetime
import numpy as np
import scipy as sp
import os
import matplotlib.pyplot as plt
import matplotlib
import ggplot as gg
import scriptine
## self import
import googletrend
import sentiment_algo
os.chdir("/root/Envs/btc-project/btc-price-analysis")

def googletrend_command(delta_t, threshold=0.0, inverse=False):
	"""the command to run google trend algorithm.

	:param delta_t:   the upper bound for original delta_t parameter
    :param threshold: upper bound for the threshold of differentiating two classes
    :param inverse:   whether to inverse the classifier
	"""
	## handle filepath and title based on parameter inverse
	filename = "googletrend"
	titlename = "ROC of google trend classifier"
	if inverse:
		filename += "_inverse"
		titlename += " (inverse version)"
	filepath = "./plots/%s.jpg" % filename
	## generate data first
	data = googletrend.preprocess()
	## store classifier evaluation metrics into dict
	output = {}
	output['tpr'] = []
	output['fpr'] = []
	output['plot'] = []
	for thre in np.arange(0, threshold+0.1, 0.1):
		print "==> threshold: %f, inverse: %s" % (thre, inverse)
		for i in xrange(1, int(delta_t)):
			googletrend.algorithm(data, i, thre, inverse)
			tp_rate, fp_rate = googletrend.evaluate(data)
			# print "delta_t: %d, TPR: %f, FPR: %f" % (i, tp_rate, fp_rate)
			output['tpr'].append(tp_rate)
			output['fpr'].append(fp_rate)
			output['plot'].append('thre_' + str(thre))
	## plot ROC graph
	## add a y=x baseline for comparison
	output['tpr'].extend([0.0, 1.0])
	output['fpr'].extend([0.0, 1.0])
	output['plot'].extend(['baseline', 'baseline'])
	df = pd.DataFrame(output)
	graph = gg.ggplot(df, gg.aes('fpr', 'tpr', color='plot')) + \
			gg.theme_seaborn() + \
			gg.ggtitle(titlename) + \
    		gg.xlab("FPR") + \
    		gg.ylab("TPR") + \
    		gg.xlim(0.0, 1.0) + \
    		gg.ylim(0.0, 1.0) + \
			gg.geom_point() + \
			gg.geom_line()
	gg.ggsave(plot=graph, filename=filepath, width=6, height=6, dpi=100)

def sentiment_command(news_file, mode=0):
	"""the command to run sentiment analysis related stuff.

	:param news_file:    the filename of news data
	:param mode:  
						0 -- run sentiment analysis (TODO)\n
						1 -- run interpolation on news_file (default: False)
	"""
	if mode == 1:
		sentiment_algo.interpolate_news(news_file)

if __name__ == "__main__":
    scriptine.run()