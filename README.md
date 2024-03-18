# Project Info
A collection of scripts and other tools

## Scripts
### PreMarking.py
Preprocessing script to populate feedback cells with default values to reduce marking times
#### Features
1. All feedback cells populated with maximum possible score (excluding overall student score)
2. Default Teaching Assistant Comment may be specified (excludes overall Teaching Assistant Comment)
#### Usage
1. Run PreMarking.py ```python PreMarking.py```
2. Enter the target directory containing unmarked ipynbs
3. Enter default Teaching Assistant Comment
4. Processed files stored within a ```marking_folder``` folder within target directory
5. Mark using the ipynb within the ```marking_folder```
