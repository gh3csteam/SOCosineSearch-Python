# SOCosineSearch - Beta v.0.1.2
> SOCosineSearch is a sentence transformers all-MiniLM-L6-v2 based search and parsing tool for StackOverflow in Python
>
> See full version history in [CHANGELOG](./CHANGELOG.md).


## Built With

- **Python** - Core pipeline, data collection, parsing
- **Numpy** - For vectors and converting to float32
- **DuckDb** - local storage of questions and their embeddings
- **Faiss** - Cosine search, vector normalization in RAM 
- **Conda** - Conda environment for Faiss
- **Stack Exchange Api** - used to collect questions into local db and also parse answers
- **[all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)** - sentence transformer used to encode sentences into vectors 

## How it works 
> Using **[Stack Exchange Api](https://api.stackexchange.com/)** it collects questions (normally around 10k) in local DuckDB database, then transforms to vectors. When program starts it loads db in RAM, normalizes vectors for faster search, waits for input, transforms your input, finds most similar question with given answers from database and prints answer & link to similar question form StackOverflow

## Known Issues and Upcoming Features
> You need to use Stack Exchange api key for data_dump due to daily limits, сonsider performance optimizations for more than ~10k objects