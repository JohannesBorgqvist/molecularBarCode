# Generating molecular barcodes and counting repeated sequences
**Author**: Johannes Borgqvist<br>
**Date**: 2021-01-07<br>
This is the github repositry for the generation of molecular bar codes and specifically to count the number of repeated sequences of length r (e.g. r=2 corresponds to the number of doublettes in a generated sequence). The whole project works with a triplet (n,k,r) where an integer is taken from the set {1,...,n} and then saved in a list l and then the integer is put back in to that set. Then this is repeated k times so that the list l contains k elements. Then the question at hand is how many repeated sequences of length r is an arbitrary list of k elements expected to have? A few script has been written in Python which simulate this application, and some figures have been generated using pgfplots and tikz in LaTeX. The scripts generates some data files which are stored in sub folders of the "./Results" folder and these data files are then converted into pdf-figures stored in the "./Figures" folder. The scripts can be found un the sub folder "./Code". There is also a little report written in the folder "./MathematicalBackground" if one wishes to read some of my results with this little toy project. The main three libraries that have been used to generate the results are: 
	
1. "*numpy*" version 1.18.5,
2. "*pandas*" version 1.0.5,
3. "*multiprocess*" version 0.70.11. 

If you wish to run all scripts and generate the figures, it should be possible to achieve this using the "run_all.sh" script. It might be neccessary to get permission to run the file first which can be done by typing "chmod +x run\_all.sh" and then the script is executed with the command "./run\_all.sh". I should say that running all these scripts took maybe four hours on my computer, so this script should only be executed if you have som time to spare. Anyhow, the code has been developed on a linux computer with operative system Ubuntu 20.10. The computer has eight cores of type "Intel(R) Core(TM) i7 10510U" with a clock speed of 1.80GHz and 16079220KiB of RAM. 

My whole idea behind this project was to practice some coding in Python as well as making a reproducible folder structure as well as a github repositry. Then, my friend Gustav comes to me with a little funny problem so I figured, why not take this problem and make it into my excuse for doing some coding! So I played around a bit with some lists, some data frames in *pandas* and I tried to parallelise the application using the *multiprocessing* (although it was not the best attempt at speeding up the application as it did not speed it up in any significant way). Anyhow, the purpose of this was mainly to practice, and it is always funnier to practice on "real" applications. 

Enjoy! 
