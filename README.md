# Data preparation in the LDA topic modelling workflow

The LDA topic modelling workflow includes several steps:
1. Creating a list of govuk links for the experiment
2. Looking up these urls on govuk api to return url, text file in csv format
3. Performing LDA on AWS EC instance (local url, text data upload and download)
4. (optional - if hierarchy) Splitting output to multiple url, text csvs based on which is the most probable topic in the url
5. (optional -if hierarchy) LDA on each split url, text csv
6. Cleaning LDA tagged output (removing parentheses etc)
7. LDA performance evaluation compared to user research-derived taxons

This repo includes scripts to perform steps 4 (split_tier_to_urltext_for_lda.py) and 6 (clean_LDAoutput_forR.py)

## Getting Started

### Prerequisites

These scripts were written and tested in a Python 2.7 environment.

### Installing

To include packages required:
```
pip install -r requirements.txt
```

To perform step 4 using the example data provided call the script from your console as follows:
```
python split_tier_to_urltext_for_lda.py --out_path ../DATA/output --preLDA_fpath example_preLDA_input.csv --tagged_fpath example_tag_input.csv
```

To perform step 6 using the example data provided
```
python clean_lda_out.py --out_path ../DATA/education/clean_lda_output/clean_tier1_educ.csv --taxonfile ../DATA/education/educ_link_taxonpath.csv --raw_lda ../DATA/education/raw_lda_tag_output/example_tag_input.csv
```

## Running the tests

pytest will be used to run tests once they've been written!

### Break down into end to end tests

These tests will be unit tests of each function and tests of the output format



## Authors

* **Ellie King** - *Initial work* - [ellieking17](https://github.com/ellieking17)
* **Nicky Zachariou** - *debugging* -[myst3ria](https://github.com/myst3ria)


## License



## Acknowledgments

* **Matt Upson** - *helpful suggestions for debugging and git muddles*
* **Andrea Grandi** -*suggestions for filtering dfs*
* **David Read** -*looping help* 