##### 
#
# Quantifying Trading Behavior in Financial Markets Using Google Trends 
# 
# Copyright (C) 2013 Tobias Preis and Helen Susannah Moat
# http://www.tobiaspreis.de
# http://www.suzymoat.co.uk
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 
# 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public 
# License along with this program; if not, see 
# http://www.gnu.org/licenses/. 
# 
# Related publication: 
# 
# Tobias Preis,	 Helen Susannah Moat, and H. Eugene Stanley,
# Scientific Reports 3, 1684 (2013) 
# doi:10.1038/srep01684 
# 
#

# Read data file
read.csv(sep=" ","PreisMoatStanley_ScientificReports_3_1684_2013.dat")->dat

# Parameters
deltat<-3 # number of previous weeks of search volume to compare to
keyword<-"debt"

# Init trading account
r<-rep(1,nrow(dat))

# Analysis
for(i in 1:nrow(dat)) {
  if(i>1) { # Not on first date (no previous search volume)
    r[i]<-r[i-1] # Copy previous return, in case no trading
  }
  if(i>deltat) { # Wait for first window to pass, 
                 # so we can calc past search volume
    if(i<nrow(dat)) { # Not on last date (no future Dow Jones value)

      now<-dat[[keyword]][i] # Google Trends search volume for keyword 
                             # (e.g. "debt") for this week
      previous<-0
      
      # Calculate average search volume of last deltat weeks
      for(t in 1:deltat) {
        previous<-previous+dat[[keyword]][i-t]
      }
      previous<-(previous/deltat)

      # Change in search volume
      value<-(now-previous)

      # DJIA closing price on the first trading day of the coming week
      # *To check this, REFER TO FILE LAYOUT, which also includes dates 
      #  for DJIA values*
      index_now<-dat$DJIA.Closing.Price[i]

      # DJIA closing price on the first trading day of the week 
      # after the coming week
      index_next<-dat$DJIA.Closing.Price[i+1]

      # Relative price change of the DJIA
      index_r<-(index_next/index_now)

      # Trading algorithm
      if(value>0) { # search volume has gone up
        # Short position
        r[i]<-(r[i-1]/(index_r))
      }
      if(value<0) { # search volume has gone down
        # Long position
        r[i]<-(r[i-1]*(index_r))
      }
    }
  }
}

# Print result
print(100*(r[nrow(dat)]-1))

# Plot result
plot(100*(r-1),type="l",col="blue",
     xlab="Time, t [Weeks]", ylab="Profit and Loss [%]")