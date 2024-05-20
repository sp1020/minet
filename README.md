# Microbial Interaction Network (MINet)

MINet is a Python package for analyzing micribial interactions and visualizaing the resulting interactions as a graph. 


## Installation using conda 

Create `minet` environment using Conda. 

```
conda env create -f environment.yml
```

## Usage 

To execute the analysis, use the following command:

```
minet interaction -i <feature_table file (.tsv)> -o <result interaction (.tsv)>
```

### Input 

* `<feature table>`: Microbial feature table (in .tsv format)

###  output
* `<result interaction>`: Microbial interaction analysis result (in .tsv format)


## Conditional Occurrence Directionality 


## Create network 


```
minet network -i <result interaction (.tsv)> -o <network file (.xml)>
```


