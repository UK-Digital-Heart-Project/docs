# UKBB 40616

Summary of the data stored in **cardiac$:\\UKBB_40616**.




## Phenotypes

The downloaded phenotypic data for access ID 40616 are stored in **./Phenotypes** pre-processed by `ukbtools`. The `ukbb_phenotype_file.R` script does basic subsetting by ICD code and is in the [UKBB_filter repo](https://github.com/UK-Digital-Heart-Project/UKBB_filter).

A copy of the Bayer project is in **./Project proposal**

The bridging file between applications 18545 and 40616 is `./Bridging file/Bridge40616_18545.csv`




## Image data

The NIfTI images for the first 10,000 participants from Wenjia are in **./10k_UKBB_NIFTI**.



### 4DSegment image file nomenclature (in ED but identical in ES)
`lvsa_ED.nii.gz` - original 2D / low resolution greyscale image (from scanner)
`LVSA_seg_ED.nii.gz` - automated 2D segmentation (using Wenjia's UK BB network)
`lvsa_SR_ED.nii.gz` - synthetic 3D / high resolution (created using 4DSegment)
`seg_lvsa_SR_ED.nii.gz` - 3D / high resolution segmentation (using 4Dsegment) 



### 4DSegment data file nomenclature (in ED but identical in ES; in LV but identical in RV)
`lv_myoed_wallthickness.txt` - wall thickness in the LV
`lv_myoed_signeddistances.txt` - comparison of mesh size vs atlas
`lv_myoed_curvature.txt` - computation of curvature at each pixel
motion - TBC



### Files in progress using 4Dsegment - file folders titles as descriptive as possible 
	# Frankie (20 CPUs. 40 with hyperthreading), Eddie (8 CPUs. 16 with hyperthreading) 
	# Marvin (24 CPUs. 48 with hyperthreading) are our servers



### Analysis to compare two DL algorithms - to transform low resolution into high resolution.
1. The first is the nicolo algorithm composed of a combination of the Wenjia network - that transforms low resolution grayscale to low resolution segmentation - plus a three-level resnet network - that allows to transform the low resolution (outgoing from the Wenjia network) and transform it into high resolution.
2. The second is a standard U-net proposed by JD and map low resolution segmentation to high resolution.

At present JD has not yet forwarded its algorithm. I'm waiting for updates.

The analysis will be saved in the following folder: `./UKBB_40616/1k_CMRs_nicolo_vs_jd_SuperRes`

Whereas the source files are located in: `./UKBB_40616/1k_CMRs_4DSuperes_motion`


Where we will find two folders:
  1. nicolo_analysis
  2. jd_analysis



### Numbers updated 13/01/2020

| S:\UKBB_40616	| 4Dsegment of 27,000 UK BB |
| --------------------------------- | --------------------------------------------------- |
| 27k_UKBB_NIFTI	| 26,876 copies of Wenjia's files - multiple views segmented	|
| 27k_failed_4dsegment_pipeline	| 172 scans that could not be segmented (not enough slices, poor quality images, etc)	|
| 27k_failed_QC	| 61 scans with poor segmentations - to try again	|
| 27k_QCed_to_do_motion	| 26,554 3D seg and co-reg QCed. Motion to do	|
| 27k_WT_txts	| 26,554 for lv_myoed_wallthickness txts	|
| 27k_WT_vtks	| 26,554 for lv_myoed_wallthickness vtks	|
| 1k_CMRs_4DSuperes_motion	| 987 copies for Nicolo to test motion	|



## Steps for UK BB data prepping
Code in S:\DL_segmentation\code



**UK BB prepping:**

- remove all other files apart from the lvsa cine using this code -> clean2.py (S:\DL_segmentation\code). Just need to change the path at the bottom
- if required, rename sa.nii to LVSA.nii.gz using this code -> Rename files recursively.R
- identify and delete duplicates (images already processed) using "Delete files already processed" on extract_text_files_to_other_folder
  



**To run motion on docker in Marvin:** 

```bash
sudo docker run -it --rm -v /home/wyedemaa@isd.csc.mrc.ac.uk/cardiac/UKBB_40616/meshes/:/meshes jinmingduan/segmentationmeshmotion /bin/bash
export LD_LIBRARY_PATH=/lib64
cd meshes
python main.py  
```



**To run 4DSegment docker in Frankie:**

```bash
sudo usermod -a -G docker wyedemaa 
(base) [wyedemaa@neon01 ~]$ cd cardiac/DL_segmentation/DL_coregistration/newVersion
(base) [wyedemaa@neon01 newVersion]$ sh run_docker.sh
cd code
root@bdd362477966:/code
sh install.sh
cd ..
root@bdd362477966:/export LD_LIBRARY_PATH=/lib64
cd code
python DMACS_docker.py
```

