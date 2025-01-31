# Provider Fairness Framework

This repository contains the code for the Provider Fairness Framework. It is a framework for evaluating and improving fairness in recommender systems.

We include 3 mitigations for the provider fairness problem:

- Confibre
- PFair
- MOReGIn

Links to the scientific papers can be found here:

- [Confibre](https://arxiv.org/abs/2305.18298)
- [PFair](https://arxiv.org/abs/2305.18298)
- [MOReGIn](https://arxiv.org/abs/2305.18298)

# AMBAR

- user_info.csv. This file contains specific users’ information depicted by the attributes user_id (i.e., the dataset index),
country, continent and gender.
- tracks_info.csv. This file contains information on the music items (i.e., tracks or songs). The attributes in this file are
track_id, artist_id, duration, styles (i.e., the style of music), and category_styles (i.e., music style categories).
- artists_info.csv. This file contains artists’ information. The attributes in this file are artist_id, gender, country, continent, styles (i.e., the style of music), and category_styles (i.e., music style categories).
- ratings.csv. This file contains the users’ music preferences represented by a rating. In particular, the attributes in each tuple are user_id, track_id, and rating.

The full dataset is found in data/AMBAR

## How to reproduce the experiments

These notebooks were tested using Python 3.8. A virtual environment is highly recommended.

```shell
python -m venv venv
source ./venv/bin/activate
```

The required packages are:

- tqdm: used for showing progress in some loops.
- numpy: used for data manipulation.
- pandas: used for data manipulation.
- cornac: used for obtaining the recommendations.

These can be installed (alongside some extra packages) using the requirements.txt provided.

```shell
python -m pip install --upgrade pip
python -m pip install -r ./requirements.txt
```

For running the notebooks, Jupyter is required and needs to be installed in the virtual environment (not included in
requirements.txt).

## Cornac

For running cornac on the data provided, use the notebook Cornac.ipynb where the process is explained. Some variables
were provided so it can be adapted to other use cases. The data used for this script is found in data/AMBAR.

More cornac documenttation can be found [here](https://cornac.readthedocs.io/en/stable/user/index.html)

## PyCPFair

For running PyCPFair on the data provided, use the notebook PyCPFair.ipynb. The main process is found in the process
section.
The data for this script is separated and based on the full set. This data may be found in data/PyCPFair.

## PFair

For running PFair on the data provided, use the notebook PFair_multiclass.ipynb. The main process is found in the process
section.
The data for this script is separated and based on the full set. This data may be found in data/PFair.

