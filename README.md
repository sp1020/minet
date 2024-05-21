# Microbial Interaction Network (MINet)

MINet is a Python package for analyzing micribial interactions and visualizaing the resulting interactions as a graph. 

## Conditional occurrence directionality method 

In MINet, microbial interaction is evaluated through co-occurrence and qualitative association among co-occurring microbes, with interaction directionality inferred from conditional occurrence patterns. 

Co-occurrence is assessed using Fisher's exact tests. The quantitative association is evaluated by Pearson's correlation on logarithm-transformed read counts. During the process, only samples where both ASVs have non-zero read counts are considered to reduce signals where the two microbes cannot interact. 

Interaction directionality is inferred from permutation tests by evaluating the likelihood of observing an ASV (ASV<sub>i</sub>) in the presence and absence of another ASV (ASV<sub>j</sub>). When the presence of one ASV (ASV<sub>i</sub>) increases the likelihood of observing the other ASV (ASV<sub>j</sub>), directionality is assigned from the former to the latter (ASV<sub>i</sub> → ASV<sub>j</sub>).


## Installation using conda 

Create `minet` environment using Conda. 

```
conda env create -f environment.yml
```

## Usage: Conditional Occurrence Directionality Analysis  

To execute the analysis, use the following command:

```
minet interaction -i <feature_table file (.tsv)> -o <result interaction (.tsv)> --depth <depth> --prevalence <prevalence>
```

### Input 

* `-i` : Microbial feature table (in .tsv format)
* `--depth` : Per sample sequence read depth cutoff for normalizing reads counts
* `--prevalence` : Prevalence cutoff to remove less represented ASVs 
* `--no-preprocess`: Set if the input data is proprocessed (the read counts will not be altered during the analysis)

###  output
* `-o` : Microbial interaction analysis result (in .tsv format)


## Usage: Create Microbial Interaction Network



```
minet network -i <result interaction (.tsv)> -o <network file (.xml)>
```

### Input

* `-i`: Microbial interaction anlaysis result file (in .tsv format)
* `--fdr-cooccurrence`: False discovery rate for cooccurrence analysis
* `--fdr-quantitative`: False discovery rate for quantitative association analysis
* `--directionality-p-value`: P-value cutoff for directionality inference


### Output

* `-o`: Network file (in .xml format)
