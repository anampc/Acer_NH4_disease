[![DOI](https://zenodo.org/badge/255729073.svg)](https://zenodo.org/doi/10.5281/zenodo.10989807)

This repository contains data and analysis scripts for the manuscript:

## Assessing Acropora cervicornis genotype resistance to elevated ammonium and disease
#### **Authors:** Ana M. Palacio Castro, Daniele Kroesche, Ian Enochs, Chris Kelble, Ian Smith, Andrew Baker, Stephanie M. Rosales
#### **Journal:** _Submitted to PlosOne_ [doi:XXX](http://dx.doi.org/XXX)  

-----

### Description:
These repository contains all data and code used to study the impact of elevated ammonium and disease on ten _A. cervicornis_ genotypes

### Contents:

#### 1.Tank_conditions:
* **1.Experimental_conditons.Rmd:** has all the code needed for Figure 1. It sources the data from the **Data** subfolder and saves statistical summaries and plots in the **Outputs** subfolder.

#### 2.Mortality:
* **1.Mortatily_Acer.Rmd:** has all the code needed for Figure 4 and survivorship analysis. It sources te data from the **Data** subfolder and saves statistical summaries and plots in the **Outputs** subfolder.

#### 3.Growth:
* This data and data analysis were not used in the manuscript:**

#### 4.YII:
* **1.IPAM_ImportFunction.R:** R function to imports the csv raw IPAM data. Yo do not have to do anything with this file, but the function is called by this file below.
* **2.MergeYIIandID.R:** Applies **1.IPAM_ImportFunction.R** to the raw data in the **IPAM_Raw**, adds the sample metadata in the **ID_AOI.csv** file and creates a long format file with the YII values that is exported to the file **Data/YII_tall.csv**
* **3.YII_Acer_Nut.Rmd:** has all the code needed for Figure 2 and related statistical analisis. It sources the data from the file **Data/YII_tall.csv** and saves statistical summaries and plots in the **Outputs** subfolder.

#### 5.Symbiodiniaceae:
* **SH_cell_code.Rmd:** has all the code needed for Figure 3. It sources the qPCR data from the **Data** subfolder and the sample metadata from the **Metadata.csv** file. Statistical summaries and plots are saved in the **Outputs** subfolder.
* **Data:** has all the raw data exported from the qPCR machine.

#### 6.Metadata:
* This folder has copies of the metadata files, but are actually not used by any code. 

</br>

#### Notes
* All packages.bib files produce a bibliography of the packages used by each .Rmd
* All .html files produce a webpage with code outputs, plots, etc. based on the .Rmd files

