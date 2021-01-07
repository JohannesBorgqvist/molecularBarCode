#=================================================
# SIMULATE MOLECULAR BAR CODE
#=================================================
# SCRIPT WRITTEN BY: Johannes Borgqvist
# DATE: 2020-01-04
# DESCRIPTION:
# The script takes in a triplet (n,k,r) where
# n>k>r>1 where n defines the set {1,...,n} of
# integers and then a number is drawn from this
# set with replacement. This is repeated k times
# implying that a list of k integers is generated.
# Given this list, the program calculates the
# number of repeated sequences of length r where
# r=2 means doublettes. The program also calculates
# an upper theoretical value for the expected
# number of repeated sequences of a length r
# as well as a lower value of the expected value.
# The output of the scripts is saved in the folder
# "../Results/". 
#=================================================
# IMPORTED PACKAGES
#=================================================
import math # for mathematics
from math import comb
from math import floor
from math import log
import random # for generating random numbers
import pandas as pd # for reading and writing data files
import numpy as np # for doing numerical calculations (e.g. vector manipulation)
import os # To get control of the terminal to, for example, create directories
import time # To benchmark the code
import multiprocessing as mp # For parallelisation over the CPUs
#=================================================
# CLASSES (1 class in total)
#=================================================
# Class 1: "setAndSamples"
# Class defining a sample with subsamples containing a function
# which calculates the upper and lower expected values
class setAndSamples():
  def __init__(self, n, k, r):
      self.n = n
      self.k = k
      self.r = r
      self.T = comb(n+k-1,k)
      self.R = floor(log(k)/log(r))
  def expectedValueBounds(self, sampleTemp):
      E_L = 0.0
      E_U = 0.0
      for i in range(1,sampleTemp.R+1):
          nTemp = sampleTemp.n -i 
          kTemp = sampleTemp.k - ((sampleTemp.r)**(i))
          E_L += i*((comb(sampleTemp.n,i)*comb(nTemp,kTemp))/(sampleTemp.T))
          E_U += i*((comb(sampleTemp.n,i)*comb((nTemp+kTemp-1),kTemp))/(sampleTemp.T))
      return E_L, E_U
#=================================================
# FUNCTIONS (5 functions in total)
#=================================================
#----------------------------------------------------------------------------
# FUNCTION 1: "save_theoretical_value"
# Function which saves the theoretical value given
# the triplet (n,k,r) into the folder determined
# by the folder string "folder_name".
def save_theoretical_value(n_list,r_list,k_list,folder_name):
  #-----------------------------------------------
  # CREATE OUTPUT FOLDER (Step 1)
  #-----------------------------------------------
  # Step 1: check if the folder exists,
  # and if not we create it
  os.makedirs(folder_name, exist_ok=True)
  #-----------------------------------------------
  # PATHS FOR SAVING THEORETICAL VALUE (Step 2-4)
  #-----------------------------------------------
  # Step 2: Create file name for the theoretical value
  file_name_theoretical = folder_name + "/theoreticalOutput.csv"
  # Step 3: Create the csv file in which we will save the output
  if not os.path.isfile(file_name_theoretical):
    df = pd.DataFrame(index=range(1),columns=range(5))
    df.to_csv(file_name_theoretical)
  # Step 4: Allocate memory for theoretical values
  vec_theoretical = np.zeros((1,5))
  #-----------------------------------------------
  # CALCULATE AND SAVE THEORETICAL VALUE (Step 5)
  #-----------------------------------------------
  # Step 5: Save the theoretical values 
  for n in n_list:# Step 5.1: loop over n:s
    for r in r_list: # Step 5.2: loop over r:s
      for k in k_list: # Step 5.3: loop over k:s
        # Step 5.4: Save the overall parameters in our
        # output vectors, i.e. (n,r,k,num_of_repeats).
        # Start with the theoretical value
        vec_theoretical[0,0] = n
        vec_theoretical[0,1] = r
        vec_theoretical[0,2] = k
        # Step 5.5: Calculate the theoretical values and save them
        sample = setAndSamples(n, k, r)
        [E_L, E_U] = sample.expectedValueBounds(sample)
        vec_theoretical[0,3] = E_L
        vec_theoretical[0,4] = E_U
        # Step 5.6: Save the theoretical vector in in a csv file
        df = pd.DataFrame(vec_theoretical)
        with open(file_name_theoretical, 'a') as f:
          df.to_csv(f, header=False)
#----------------------------------------------------------------------------
# FUNCTION 2: "get_duplicates_with_count"
# Function which counts all repeated sequences
# of all possible lengths in a provided list "l".
# The function takes a list "l" as input and returns
# a dictionary "dictOfElems" containing all values
# that occured more than ones in "l" as well as their
# frequency.
def get_duplicates_with_count(listOfElems):
    # Get frequency count of duplicate elements in the given list
    dictOfElems = dict()
    # Iterate over each element in list
    for elem in listOfElems:
        # If element exists in dict then increment its value else add it in dict
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1    
    # Filter key-value pairs in dictionary. Keep pairs whose value is greater than 1 i.e. only repeated elements from list.
    dictOfElems = { key:value for key, value in dictOfElems.items() if value > 1}
    # Returns a dict of duplicate elements and thier frequency count
    return dictOfElems
#----------------------------------------------------------------------------
# FUNCTION 3: "generate_repeated_sequence"  
# Function which simulates repeated sequences a list l
# with k elements from the set {1,2,...,n} and returns
# a vector "repeated_sequences" containing the values which
# were repeated exactly r times in the list l.
def generate_repeated_sequence(n,k,r):
  # Generate list l from set {1,2,...,n} of length k
  l = []
  for i in range(1,k+1):
    v = random.randint(1,n)
    l.append(v)
  # Get a dictionary containing repeated sequences elements in the list l
  # and their frequency count using the function "get_duplicates_with_count"
  multiple_occurences = get_duplicates_with_count(l)
  # Allocate memory for vector with only repeates of precisely length r
  repeated_sequences = []
  # Loop over the repeated segments in "multiple_occurences" and save
  # the repeated sequences of length r in the vector "repeated_sequences".
  for key, value in multiple_occurences.items():
    if value == r:
      repeated_sequences.append(key)
  # Return the vector with repeated sequences of precisely length r
  return repeated_sequences
#----------------------------------------------------------------------------
# FUNCTION 4: "length_of_repeated_sequences_in_parallel":
# Takes the triplet (n,r,k) as well as an arbitrary index
# i as an input. It generates a sequence "r" using the
# previously defined function "generate_repeated_sequence"
# and then it returns the length of this index. The reason
# why this function contains the index "i" is to allow for
# parallelisation using the multiprocessing library in Python
def length_of_repeated_sequences_in_parallel(n,r,k,i):
    # This is the loop we do in parallel
    #"for i in range(num_of_repeats):"
    # Generate repeated sequences of length r
    rep_sequences = generate_repeated_sequence(n,k,r)
    # Return the number of repeated sequences of length r
    return len(rep_sequences)
#----------------------------------------------------------------------------
# FUNCTION 5: "simulate_repeated_sequences"  
# Function which simulates repeated sequences given the
# triplet (n,k,r) and it does so "num_of_repeats" times. A
# vector "vec" is saved in a csv file determined by the
# input string "foldername". The vector "vec" has "num_of_repeats+5"
# elements where the first four values are: vec[0,0]=n, vec[0,1]=r,
# vec[0,3]=k, vec[0,4]=num_of_CPUs  and vec[0,5]=nuOfRepeats.
# The rest of the "num_of_repeats" values are the number of repeated
# sequences of length r. This program parallelises the counting of the
# repeated sequences and the parallelisation is done over CPUs using the
# "multi processing"-library in python. The number of CPUs which is used
# is determined by the variable "num_of_CPUs". As we invoke parallelisation,
# we also save the execution time to benchmark the code. The execution time
# of the script is saved in a vector similar to the one in which the number
# of repeated sequences were saved. Both these vectors are subsequently stored
# in two csv-files which are found in the sub-folder of "../Results/" determined
# by the string "folder_name". 
def simulate_repeated_sequences(n_list,r_list,k_list,num_of_repeats,num_of_CPUs,folder_name):
  #-----------------------------------------
  # CREATE OUTPUT FOLDER (Step 1)
  #-----------------------------------------
  # Step 1: check if the folder exists,
  # and if not we create it
  os.makedirs(folder_name, exist_ok=True)
  #-----------------------------------------
  # SAVE BENCHMARKING TIME (Step 2-4)
  #-----------------------------------------
  # Step 2: Create file name for the benchmarking time
  file_name_benchmark = folder_name + "/benchmark.csv"
  # Step 3: Create the csv file in which we will save the output
  if not os.path.isfile(file_name_benchmark):
    df = pd.DataFrame(index=range(1),columns=range(6))
    df.to_csv(file_name_benchmark)
  # Step 4: Allocate memory for the execution time
  vec_benchmark = np.zeros((1,6))  
  #-----------------------------------------
  # SAVE SIMULATED OUTPUT (Step 5-7)
  #-----------------------------------------
  # Step 5:Create a file name in which we will save
  # the output
  file_name_simulated = folder_name + "/simulatedOutput.csv"
  # Step 6: Create the csv file in which we will save the output
  if not os.path.isfile(file_name_simulated):
    df = pd.DataFrame(index=range(1),columns=range(num_of_repeats+5))
    df.to_csv(file_name_simulated)
  # Step 7: Allocate memory for the vector "vec" which will be  
  # saved in the csv file
  vec_simulated = np.zeros((1,num_of_repeats+5))
  #-----------------------------------------
  # CALCULATE OUTPUT AND BENCHMARK (Step 8)
  #-----------------------------------------  
  # Step 8: Loop over the n:s, k:s and r:s
  # in the provided lists. Calculate generate
  # sequences using these parameters and count
  # the number of repeated sequences. Do this
  # "nuOfRepeats times". Save all these in the
  # vector "vec"  which is then saved in a
  # csv-file with the name "file_name"
  for n in n_list:# Step 8.1: loop over n:s
    for r in r_list: # Step 8.2: loop over r:s
      for k in k_list: # Step 8.3: loop over k:s
        # Step 8.4: Save overall information in
        # the data files both for the execution
        # time (i.e. benchmarking) and for the
        # actual data (i.e. number of repeated
        # sequences):
        # Benchmarking or execution time
        vec_benchmark[0,0] = n
        vec_benchmark[0,1] = r
        vec_benchmark[0,2] = k
        vec_benchmark[0,3] = num_of_CPUs                        
        vec_benchmark[0,4] = num_of_repeats
        # Simulated values or repeated sequences
        vec_simulated[0,0] = n
        vec_simulated[0,1] = r
        vec_simulated[0,2] = k
        vec_simulated[0,3] = num_of_CPUs                
        vec_simulated[0,4] = num_of_repeats
        # Step 8.5: Take the start time
        start_time = time.time()
        #-----------------------------------------
        # PARALLEL COMPUTATIONS (Step 8.6-8.8)
        #-----------------------------------------  
        # Step 8.6: Start a pool of parallel processes
        # where the number of processes is given by
        # the integer "num_of_CPUs"
        pool = mp.Pool(num_of_CPUs)
        # Step 8.7: Calculate the number of repeated sequences in parallel
        # using the processes in the previously defined pool and this
        # will be done "num_of_repeats" times.
        tempVec = [pool.apply(length_of_repeated_sequences_in_parallel, args=(n,r,k,i)) for i in range(num_of_repeats)]
        # Step 8.8: Close and join the pool to stop parallelisation
        pool.close()
        pool.join()
        # Step 8.9: Save the repeated sequences in our
        # output vector
        vec_simulated[0,5:(num_of_repeats+5)] = tempVec        
        # Step 8.8: Benchmark the code meaning that we
        # calculate the execution time of the script
        # and that we save this in our second output
        # vector
        end_time = time.time()
        run_time = end_time-start_time
        vec_benchmark[0,5] = run_time # The time is reported in seconds
        # Step 8.9: Save the execution time in a csv file
        df = pd.DataFrame(vec_benchmark)
        with open(file_name_benchmark, 'a') as f:
          df.to_csv(f, header=False)
        # Step 8.10: Lastly, we append the "vector_simulated" to the
        # csv file determined by the string "file_name_simulated"
        df = pd.DataFrame(vec_simulated)
        with open(file_name_simulated, 'a') as f:
          df.to_csv(f, header=False)        
#----------------------------------------------------------------------------


