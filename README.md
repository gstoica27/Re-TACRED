# Re-TACRED: Addressing Shortcomings of the TACRED Dataset

## AAAI 2021 Paper ID: 3163

### This repository cotains all the necessary code to replicate our submission results. 

We divide it up into four directories. 

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


