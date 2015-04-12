#!/usr/bin/python

import pandas as pd
import datetime
import numpy as np
import scipy as sp
import os
import matplotlib.pyplot as plt
import matplotlib
import scriptine
## self import
import classifiers
os.chdir("/root/Envs/btc-project/btc-price-analysis")

def googletrend_classifier_command(delta_t, threshold=0, inverse=False):
	"""the command to run google trend algorithm.

	:param delta_t: the upper bound for delta_t parameter
    :param threshold: value to differentiate two classes
    :param inverse: whether to inverse the classifier or not
	"""
	data = classifiers.googletrend_preprocess()
	print "threshold: %d, inverse: %s" % (threshold, inverse)
	for i in xrange(1, int(delta_t)):
		classifiers.googletrend(data, i, threshold, inverse)
		tp_rate, fp_rate = classifiers.googletrend_evaluate(data)
		print "delta_t: %d, TPR: %f, FPR: %f" % (i, tp_rate, fp_rate)

if __name__ == "__main__":
    scriptine.run()