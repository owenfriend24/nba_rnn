# nba_rnn
### Latent play-style mapping of NBA players via RNN

* Unsupervised deep learning approach to defining play styles for current NBA players, identifying league archetypes, and generalizing these archetypes across eras. 

What I find interesting about recurrent neural networks (and deep learning in general) is not that they can use data to predict future observations, because 1) lots of simpler methods can predict future values (e.g., OLS regression) and 2) real-world problems often cannot be precisely predicted by a model no matter how much data you have (e.g., the stock market, the scores of sports games). What *is* interesting about RNNs is their capacity to form underlying representations, which can be interrogated directly after training. In other words, while it is impossible to build a model that tells me definitively how many points each player will score, I can build a model which does its best to predict player performance, and then examine what that model learned and how it is making predictions. By extracting representations of each player from the model's 128-dimensional hidden state (i.e., its 'ball knowledge'), here, I derive data-driven archetypes of different play-styles, group players with similar play-styles (both in the current NBA and across eras!) and examine how those play-styles have evolved through the years. 

nba_rnn.ipynb provides the full project including feature selection, scaling and preprocessing, architecture and training, interrogation of 128D hidden-state representations, dimensionality reduction and clustering, and extension of the model's 'ball knowledge' to previous eras. 

Some highlights include:
* Wemby's play style is embedded almost directly between LeBron and AD in feature space (see below)
* Individual RNN units track things like rebounding prowess and "empty calorie" players who score a lot of points but don't win a lot of games
* Projecting historical players into our derived latent feature space (the model's 'ball knowledge'), SGA is the closest current era player to 90s Jordan. Wemby is closest to Hakeem, Devin Booker to Reggie Miller, Jokic to Larry Bird, and Julius Randle to Charles Barkley.
* The biggest shift in archetypal play-styles from the 90s to today is the explosion of off-ball 3-point specialists


<img width="789" height="810" alt="clusters" src="https://github.com/user-attachments/assets/75414deb-e5aa-4813-9562-bdceae36f2aa" />
