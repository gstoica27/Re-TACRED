# Re-TACRED: Addressing Shortcomings of the TACRED Dataset

## AAAI 2021 Submission ID: 3163

### Work In Progress Until AAAI Publication

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


**SpanBERT**

We perform our SpanBERT experiments using the open-source repository provided by Joshi et al. (2019) [here](https://github.com/facebookresearch/SpanBERT). All our experiments are performed using the SpanBERT case-large model. However, we make a few alterations to the evaluation pipeline. This directory contains the *complete* files that contain all our changes. Simply replacy "run_tacred.py" in the SpanBERT repository with our "run_tacred.py" script, and then add the "scorer.py" and "category_maps.py" files in the same directory. Training and evaluation are performed as in the linked repository, but note that for evaluation on the test split, you must pass "--eval_test" as an additional commandline argument.

