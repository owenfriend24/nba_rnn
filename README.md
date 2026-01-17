# nba_rnn
## Latent play-style mapping of NBA players via RNN
* Unsupervised deep learning approach to deriving data-driven play styles for current NBA players, identifying league archetypes, and generalizing these archetypes across eras. 
---

### Highlights:
* Learned latent representations of NBA player play-styles using unsupervised sequence modeling, precisely predicting next game performance (e.g., within one point)
* Trained recurrent neural networks to encode player behavior into a 128-dimensional latent space (play-style embeddings)
* Discovered data-driven player archetypes via dimensionality reduction and clustering
* Demonstrated cross-era generalization by projecting historical players into a modern latent space
* Interrogated individual hidden units to reveal meaningful differences in play-style (e.g., "empty calorie" players who score a lot of points but don't win a lot of games)

### Methods at a glance:
* Sequential modeling of sports data via recurrent neural network (RNN)
* Unsupervised representation learning via hidden-state embeddings
* Feature scaling and temporal preprocessing
* Dimensionality reduction and clustering
* Model interpretability through hidden-unit analysis
* Out-of-distribution generalization to historical eras

<img width="789" height="810" alt="clusters" src="https://github.com/user-attachments/assets/75414deb-e5aa-4813-9562-bdceae36f2aa" />

---

### Motivation: 
Rather than treating deep learning primarily as a prediction tool, this project focuses on representation learning: using recurrent neural networks to discover structured, interpretable latent embeddings from complex temporal data. While many methods can predict future values, real-world systems like sports performance are noisy and inherently only partially predictable. The core logic behind this project is that it does not matter if sequential predictions are imperfect, because they allow sequence models can learn meaningful internal representations that capture stable behavioral structure. 

Accordingly, this RNN is trained to model player performance over time, after which the 128-dimensional hidden state is extracted as a learned embedding of each player’s play style (the model’s “ball knowledge”). These embeddings are then interrogated directly to cluster players into data-driven archetypes, compare stylistic similarity across players and eras, and even analyze how latent play styles evolve historically.

This setup allows the model to function not as a forecasting engine, but as a tool for discovering and interpreting latent structure in sequential human behavior.

---

### Repo/notebook description: 
[nba_rnn.ipynb](https://github.com/owenfriend24/nba_rnn/blob/main/nba_rnn.ipynb) contains the full, end-to-end pipeline, including:
* Feature selection, scaling, and temporal preprocessing
* RNN architecture design and training
* Extraction of 128D hidden-state embeddings
* Dimensionality reduction and clustering of learned representations
* Projection of historical players into the learned latent space

Some interesting results include:
* Wemby's play style is embedded almost directly between LeBron and AD in latent feature space (see figure)
* Individual RNN units track things like rebounding prowess and high-volume but low impact scoring
* Projecting historical players into our derived latent feature space (the model's 'ball knowledge'), SGA is the closest current era player to 90s Jordan. Wemby is closest to Hakeem, Devin Booker to Reggie Miller, Jokic to Larry Bird, and Julius Randle to Charles Barkley.
* The biggest shift in archetypal play-styles from the 90s to today is unsurprisingly the explosion of off-ball 3-point specialists


