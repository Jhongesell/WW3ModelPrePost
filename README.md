# WatchWave Model Dataset 

<a href="https://colab.research.google.com/github.com/carlosenciso/WW3ModelPrePost/blob/master/NOTEBOOK/WW3_prepost.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory"></a>

<br>

The objective of this repository is to download data from the WWIII model (hindcast + current simulations), for three wave variables and for a specific geographic location. After downloading and post-processing the Grib2 files, the data will be saved in CSV format.

The scripts also webscrapping the ASCII data from another information source for more current periods (2 months behind the current date).

### Installation

#### Requirements

- conda - Install for your operating system from [Anaconda (Python 3)](https://www.anaconda.com/distribution/)
- git

#### Instructions

To use the notebooks locally you will first need to download or clone this repo using the following command in a terminal

```bash
git clone https://github.com/carlosenciso/WW3ModelPrePost.git && cd WW3ModelPrePost
```

If you want to use `git` on Windows, you will need to install git from your [página oficial](https://git-scm.com/downloads) and then run Git Bash from where you can use the `git` command.

When the download is finished, you will find yourself inside the folder that contains the files for this repository. You will need to install the working environment specified in the `environment.yml` file using the` conda` command

```bash
conda env create -f environment.yml
```
