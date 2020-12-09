# Re-TACRED

 ```$xslt
Re-TACRED: Addressing Shortcomings of the TACRED Dataset
George Stoica, Emmanouil Antonios Platanios, and Barnabás Póczos
In Proceedings of the Thirty-fifth AAAI Conference on Artificial Intelligence 2021
```

This repository contains all relevant resources for using Re-TACRED, a new relation extraction dataset. 

For details on this work please check out our:
* AAAI 2021 paper: Camera Ready in Progress
* NeurIPS 2020 KR2ML Workshop: [Paper](https://kr2ml.github.io/2020/papers/KR2ML_12_paper.pdf) & [Poster](https://kr2ml.github.io/2020/papers/KR2ML_12_poster.pdf)

Below we describe the contents of the four repository directories by name.

**Re-TACRED**

This directory contains version 1.0 of our revised TACRED dataset patches for each split. Due to licensing restrictions, we cannot provide the complete dataset. 
However, following Alt, Gabryszak, and Hennig (2020), our patch consists of json files mapping TACRED instances by their id to our revised labels. 
Note that our train/development/test splits are slightly smaller than the complete TACRED dataset. This is due to our removal of non-english TACRED data, 
mentioned in Section 3.5 of our submission. 

The original TACRED dataset is available for download from the LDC [here](https://catalog.ldc.upenn.edu/LDC2018T24). It is free for members, or $25 for non-members.

Applying the patch is simple and only requires replacing each TACRED instance (where applicable) with our revised relation. For convenience, we provide a script 
for this named apply_patch.py in the Re-TACRED directory. In the script, you only need to replace 
```python
tacred_dir = None
save_dir = None
```
With the path to your TACRED dataset save directory, and the directory where you wish to save the patched data to respectively.

**PA-LSTM, C-GCN & SpanBERT**

We base our experiments off of the open-source model repositories of:
* [PA-LSTM](https://github.com/yuhaozhang/tacred-relation.git): Zhang et. al. (2017) 
* [C-GCN](https://github.com/qipeng/gcn-over-pruned-trees.git): Zhang et. al. (2018)
* [SpanBERT](https://github.com/facebookresearch/SpanBERT): Joshi et. al. (2019)

However, it is not possible to simply pass Re-TACRED to each model repository because each is hardcoded for TACRED. Thus, we must modify certain files to make each model Re-TACRED compatible. 
To make it as easy as possible, we provide all our altered files in each named model directory (e.g., the provided PA-LSTM directory). All that needs to be done is to replace the corresponding file in our provided directory with the corresponding file in the original model repository. For instance, you may replace SpanBERT's "run_tacred.py" file with our "run_tacred.py" file.
Running experiments is equivalent to how it is performed in the original model repositories.
