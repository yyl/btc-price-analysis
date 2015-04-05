# btc-price-analysis

## 0. Motivation

Motivate more: why BTC price prediction is different from regular stock price prediction. As from [bitcoin.org](https://bitcoin.org/en/you-need-to-know):

> The price of a bitcoin can unpredictably increase or decrease over a short period of time due to its young economy, novel nature, and sometimes illiquid markets. Consequently, keeping your savings with Bitcoin is not recommended at this point. 

Our first objective is to see if the common algorithms that work well on regular price prediction still works on BTC price.

## Progress

- download a fixed amount of historic data [done]
- basic financial analysis ([done](http://nbviewer.ipython.org/github/yyl/btc-price-analysis/blob/master/notes/basics.ipynb))
- google trend paper replicate ([in progress](http://nbviewer.ipython.org/github/yyl/btc-price-analysis/blob/master/notes/google_trend.ipynb))
  - similar approach through analyzing news headlines (NYT, Guardian, etc) with sentiment analysis
- bayesian prediction, regression
- performance evaluation

## Note

Should probably have the first complete set of mining process done. 

- prepare dataset
  - BTC price data: daily or weekly
  - news headline data with sentiment score, daily or weekly
  - merge them together, and then split into training and testing set (TODO: validation for time-series data?)
- train the classifier
  - write up explicitly the model
- evaluation
  - TODO: what is the metric to evaluate?

It should include data preprocessing, training and testing/validation. Let's do first e.g. dual-average algorithm, which is essentially a decision tree model. Then, we move on to google trend algorithm, which is also a decision tree. In both cases, the problem renders to a classification problem. That is, given historic price, label say tomorrow's price to be rise or fall.

The original trading problem is different from a data mining problem, therefore it is necessary to model it into a regular mining problem.

## Resources

- https://www.otexts.org/fpp/4/8
- http://www.kaggle.com/c/informs2010
- [Glossary](https://support.coinbase.com/customer/portal/articles/1833695-bitcoin-glossary)
- A replicate of google trend paper: [link](http://nbviewer.ipython.org/github/twiecki/replicate_google_trends/tree/master/), [discuss](https://www.quantopian.com/posts/google-search-terms-predict-market-movements), [another one](http://nbviewer.ipython.org/gist/shabbychef/5808945)
- bitcoin and google trend: [link](http://www.btcfeed.net/infographics/google-trends-indicate-positive-interest-bitcoin/)
- hacking google trend API: [link](http://techslides.com/hacking-the-google-trends-api)
- critics of google trend paper: [link](http://sellthenews.tumblr.com/post/49271345693/piled-higher-and-deeper)
- https://www.google.com/finance/domestic_trends
