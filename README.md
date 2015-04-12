# btc-price-analysis

## Motivation

Motivate more: why BTC price prediction is different from regular stock price prediction. As from [bitcoin.org](https://bitcoin.org/en/you-need-to-know):

> The price of a bitcoin can unpredictably increase or decrease over a short period of time due to its young economy, novel nature, and sometimes illiquid markets. Consequently, keeping your savings with Bitcoin is not recommended at this point. 

Our first objective is to see if the common algorithms that work well on regular price prediction still works on BTC price.

## Algorithms

We have attempted to analyze the bitcoin price from several different perspectives with different algorithms.

### google trend classifier
***

This is roughly a rule-based classifier based on the search interest index of keyword "bitcoin". The problem is to classify weekly price trend to be either rise or fall. The algorithm is originally proposed in [a paper](http://www.nature.com/srep/2013/130425/srep01684/full/srep01684.html), and we modify it to fit in our problem setup.

Data used: weekly bitcoin price, weekly search interest index of keyword "bitcoin"

The algorithm works as follows:

- compute the average search interest of past _k_ weeks: `s_avg`
- compare search interest of current week `s_t` with `s_avg`
  - if `s_t` > `s_avg` (search interest increases), label next week as `fall`
  - otherwise (search interest decreases), label next week as `rise`

possible extension and parameter tuning:

This only parameter that one can change is the _k_ which decides how many previous weeks it takes to compute the previous average price. We can add one more parameter, which we call `diff`. In the second step, we label next week's price as `fall` iff `s_t` > `s_avg` + `diff`.

#### Results

The first graph contains the ROC of the google trend classifier given different threshold `diff`. For each threshold, we computed different TPR/FPR by plugging different values for parameter `delta_t`. 

![google trend classifier](https://github.com/yyl/btc-price-analysis/blob/master/plots/googletrend.jpg)

The red line in the graph is the baseline "random-guess". It turns out the algorithm works worse than the baseline. We realize if we flip the algorithm logic, that is predict price rise if search interest increases, and falls otherwise, we get a better result. The updated ROC is showing below.

![google trend classifier (inversed)](https://github.com/yyl/btc-price-analysis/blob/master/plots/googletrend_inverse.jpg)

[TODO] add reasoning

#### Bayesian Curve Fitting

Bayesian curve fitting is a statistical technique to learn the pattern of previous datasets and make prediction for future values based on the model learned.

Input: daily bit-coin price;
Output: bit-coin price next day;

The algorithm works as follows:
- given the training data X and T, along with a new test point x, the goal is to predict the value of t. That is to evaluate the predictive distribution `p(t|x,X,T)`;
- given the value of x, the corresponding value of t has a Gaussian distribution;
  - `m(t) = beta*transpose(phi(x))*S*sum(phi(x_n)*t_n)`
  - `S_inverse = alpha*I + beta*sum(phi(x_n)*transpose(phi(x)))`
  - `phi(x) = [x^i...], i = 0, 1, ...M`
  - where `alpha = 0.005`, `beta = 11.1`, `I` is the unit matrix;
- the mean value is the predicted price for the next day.

#### Moving Average Trend Classifier

The moving average algorithm is to calculate the average value within a window size and then move to the next time period for the fixed size. Combining the moving average and any short-term price predition algorithm, we are able to classify Bit-coin price trend weekly and monthly, which works as follows:
- sample the historical data weekly, which means the `sample rate` is 7;
- predict each day's price for next week;
- calculate moving average this week go back N `ave_now` and next week go back N `ave_future`;
- if `ave_now > ave_future`, predict `0: decrease`, otherwise `1: increase`;
- from results of each day next week, `vote` for the trend next week;
- similarly `vote` for monthly trend with `weight` [0.6;0.25;0.1;0.05].

## Evaluation

We are using the `absolute mean error` and `relative error rate` to evalute our algorithms, and the two parameters are defined as follows:
- `absolute_mean_error = sum(abs(predict_price-price))/size(price)`
- `average_relative_error = sum(abs(predict_price/price - 1))/size(price)`

## Progress

- download a fixed amount of historic data [done]
- basic financial analysis ([done](http://nbviewer.ipython.org/github/yyl/btc-price-analysis/blob/master/notes/basics.ipynb))
- google trend paper replicate ([in progress](http://nbviewer.ipython.org/github/yyl/btc-price-analysis/blob/master/notes/google_trend.ipynb))
  - similar approach through analyzing news headlines (NYT, Guardian, etc) with sentiment analysis
- bayesian prediction, regression
- performance evaluation

## To-do Next

- use WEKA to get some visualized results for regression;
- try SVM for price prediction;

## Resources

- https://www.otexts.org/fpp/4/8
- http://www.kaggle.com/c/informs2010
- [Glossary](https://support.coinbase.com/customer/portal/articles/1833695-bitcoin-glossary)
- A replicate of google trend paper: [link](http://nbviewer.ipython.org/github/twiecki/replicate_google_trends/tree/master/), [discuss](https://www.quantopian.com/posts/google-search-terms-predict-market-movements), [another one](http://nbviewer.ipython.org/gist/shabbychef/5808945)
- bitcoin and google trend: [link](http://www.btcfeed.net/infographics/google-trends-indicate-positive-interest-bitcoin/)
- hacking google trend API: [link](http://techslides.com/hacking-the-google-trends-api)
- critics of google trend paper: [link](http://sellthenews.tumblr.com/post/49271345693/piled-higher-and-deeper)
- https://www.google.com/finance/domestic_trends
