# btc-price-analysis

## Motivation

Motivate more: why BTC price prediction is different from regular stock price prediction. As from [bitcoin.org](https://bitcoin.org/en/you-need-to-know):

> The price of a bitcoin can unpredictably increase or decrease over a short period of time due to its young economy, novel nature, and sometimes illiquid markets. Consequently, keeping your savings with Bitcoin is not recommended at this point. 

Our first objective is to see if the common algorithms that work well on regular price prediction still works on BTC price.

## Algorithms

We have attempted to analyze the bitcoin price from several different perspectives with different algorithms.

#### google trend classifier

This is roughly a rule-based classifier based on the search interest index of keyword "bitcoin". The problem is to classify weekly price trend to be either rise or fall. The algorithm is originally proposed in [a paper](http://www.nature.com/srep/2013/130425/srep01684/full/srep01684.html), and we modify it to fit in our problem setup.

Data used: weekly bitcoin price, weekly search interest index of keyword "bitcoin"

The algorithm works as follows:

- compute the average search interest of past _k_ weeks: `s_avg`
- compare search interest of current week `s_t` with `s_avg`
  - if `s_t` > `s_avg` (search interest increases), label next week as `fall`
  - otherwise (search interest decreases), label next week as `rise`

possible extension and parameter tuning:

This only parameter that one can change is the _k_ which decides how many previous weeks it takes to compute the previous average price. We can add one more parameter, which we call `diff`. In the second step, we label next week's price as `fall` iff `s_t` > `s_avg` + `diff`.


## Progress

- download a fixed amount of historic data [done]
- basic financial analysis ([done](http://nbviewer.ipython.org/github/yyl/btc-price-analysis/blob/master/notes/basics.ipynb))
- google trend paper replicate ([in progress](http://nbviewer.ipython.org/github/yyl/btc-price-analysis/blob/master/notes/google_trend.ipynb))
  - similar approach through analyzing news headlines (NYT, Guardian, etc) with sentiment analysis
- bayesian prediction, regression
- performance evaluation

## Resources

- https://www.otexts.org/fpp/4/8
- http://www.kaggle.com/c/informs2010
- [Glossary](https://support.coinbase.com/customer/portal/articles/1833695-bitcoin-glossary)
- A replicate of google trend paper: [link](http://nbviewer.ipython.org/github/twiecki/replicate_google_trends/tree/master/), [discuss](https://www.quantopian.com/posts/google-search-terms-predict-market-movements), [another one](http://nbviewer.ipython.org/gist/shabbychef/5808945)
- bitcoin and google trend: [link](http://www.btcfeed.net/infographics/google-trends-indicate-positive-interest-bitcoin/)
- hacking google trend API: [link](http://techslides.com/hacking-the-google-trends-api)
- critics of google trend paper: [link](http://sellthenews.tumblr.com/post/49271345693/piled-higher-and-deeper)
- https://www.google.com/finance/domestic_trends
