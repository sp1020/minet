# Template usage guide 

This is a template for Python package development 


## Step 1. Clone the template

Create a directory for the application, clone the Python template package, and remove the template git repository. 

```
mkdir NEW_APP
git clone git@github.com:sp1020/python_app_template.git ./NEW_APP
rm NEW_APP/.git -rf
```

## Step 2. Edit package related information

1. Edit pyproject.toml
    - Replace project.name (NEW_APP)
    - Insert dependencies
    - Replace script commaned (my_package -> NEW_APP)
1. Edit environment.yml
    - Edit the name of the conda environment
1. Rename project name
    - Rename the project directory name from my_package into NEW_APP


## Step 3. Create a conda environment 

```
conda env create -f environment.yml
```

