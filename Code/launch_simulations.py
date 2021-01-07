#=================================================
# LAUNCH SIMULATIONS
#=================================================
# SCRIPT WRITTEN BY: Johannes Borgqvist
# DATE: 2020-01-04
# DESCRIPTION:
# The script launches the simulations defined in
# the experimental designs defined0 in this script.
# The user has to give three command line inputs
# when executing the program according to: 
# "python3 launch_simulations.py name_str x y"
# where "name_str" is the name of the set of
# experiments that are launched, "x" is the number
# of times that the stochastic simulations will
# be executed and "y" is the number of CPUs that
# the script will be executed with. The user has
# to provide at least the first two variables
# (i.e. "name_str" and "x") and if "y" is not
# defined the number of cores are set to the
# number of available cores minus one. 
#=================================================
# IMPORTED PACKAGES
#=================================================
# To access the functions that calculates the
# number of repeated sequences
import simulate_bar_code
# To set the number of CPUs used for parallel
# computing (if needed)
import multiprocessing as mp 
# To read the input arguments defined by the user
import sys
import random # for generating random numbers
#=================================================
# FUNCTIONS
#=================================================
# FUNCTION 1: "is_integer"    
# The function excepts a string and returns a
# logical variable. If the provided string is
# an integer it will return "True" else it will
# return "False". 
def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
# FUNCTION 2: "frange"
# The function is used to generate a list
# with a known step length. Normally, we
# would use something like "list(range(10))"
# but range only increments the values with
# a step length of 1. So this function is
# here as a way of making lists with an
# arbitrary step length.
def frange(start, stop, step=1.0):
    ''' "range()" like function which accept float type''' 
    i = start
    while i < stop:
        yield i
        i += step    
#=================================================
# HANDLE INPUT ARGUMENTS BY USER
#=================================================
# Allocate memory for the experiment, the number of
# repititions and the number of CPUs
experiment = ""
num_of_repeats = 0
num_of_CPUs = 0
# Assign values to the above variables by going
# through the inputs provided by the user:
# Check the number of inputs
if (len(sys.argv)<3):# Too few
    print("\tToo few arguments are provided!\n")
    print("\tAborting execution...\n")
    sys.exit(0) # Exit the program
if (len(sys.argv)>4):# Too many
    print("\tToo many arguments are provided!\n")
    print("\tAborting execution...\n")
    sys.exit(0) # Exit the program
elif ((len(sys.argv)>2)) and ((len(sys.argv)<5)):# Correct number
    experiment = sys.argv[1]
    # Is integer provided for the number of repititions?
    if (is_integer(sys.argv[2])==False): # No integer provided?
        print("\n\tERROR: The second input must be an integer!\n")
        print("\tThis integer corresponds to the number of times that the stochastic simulations will be repeated.\n")
        print("\tAborting execution...\n")
        sys.exit(0) # Exit the program
    else:# Integer provided for the number of repititions
        # Save the number of provided repititions 
        num_of_repeats = int(sys.argv[2])
        # Save or set the number of CPUs used
        if (len(sys.argv)==3):# Number of CPUs not set
            num_of_CPUs = mp.cpu_count()-2
            print("\n\tTHIRD INPUT MISSING\n")
            print("\tSince the number of CPUs has not been provided, the execution of the script will be parallelised with:\n\tnum_of_CPUs\t=\t%d CPUs\n"%(num_of_CPUs))
        elif (len(sys.argv)==4):# Fourth argument provided
            if (is_integer(sys.argv[3])==False):# Not an integer provided
                num_of_CPUs = mp.cpu_count()-2
                print("\n\tTHIRD INPUT NOT AN INTEGER\n")
                print("\tSince the number of CPUs has not been provided correctly, the execution of the script will be parallelised with:\n\tnum_of_CPUs\t=\t%d CPUs\n"%(num_of_CPUs))
            elif(is_integer(sys.argv[3])==True and int(sys.argv[3])>mp.cpu_count()):# Number of CPUs provided correctly but to many of them
                num_of_CPUs = mp.cpu_count()-2
                print("\n\tTHIRD INPUT TOO BIG\n")
                print("\tSince the number of available CPUs is smaller than the desired number of CPUs, the execution of the script will be parallelised with:\n\tnum_of_CPUs\t=\t%d CPUs\n"%(num_of_CPUs))                
            elif(is_integer(sys.argv[3])==True and int(sys.argv[3])<mp.cpu_count()):# Number of CPUs provided correctly
                num_of_CPUs = int(sys.argv[3])

#=================================================
# THE VARIOUS EXPERIMENTS
#=================================================                
# We begin by defining the folder in which
# we will store the generated results
folder_str = "../Results/"+experiment
# Now, we go through the experiments...
if (experiment == "theoretical_vs_simulated"):
    # We define our three lists corresponding
    # to the triplet (n,k,r).
    # THE LIST WITH n-VALUES
    n = 4**12 # Big sample
    n_list = [n] # Create a list as input
    # THE LIST WITH r-VALUES
    r = 2 # Length of repeated sample
    r_list = [r] # Create a list as input
    # THE LIST WITH k-VALUES
    # Here, we use the previously defined
    # "frange"-function which takes in
    # three arguments: a min, max and step length.
    # We do this in three sublist with varying
    # step length
    # SUB LIST 1: small step length
    k_min = 3000
    k_max = 5000
    step_length = 200
    k_list = list(frange(k_min, k_max, step_length)) # Create list       
    # SUB LIST 2: medium step length
    k_min = 5000
    k_max = 10000
    step_length = 500
    k_sublist_1 = list(frange(k_min, k_max, step_length)) # Create list      
    # SUB LIST 3: large step length
    k_min = 10000
    k_max = 50001
    step_length = 10000
    k_sublist_2 = list(frange(k_min, k_max, step_length)) # Create list      
    # Merge the three sub lists using the "extend" function
    k_list.extend(k_sublist_1)
    k_list.extend(k_sublist_2)
    #----------------------------------------------------
    # CALCULATE THE THEORETICAL VALUES
    #----------------------------------------------------
    print("\tCalculating the theoretical values...\n")
    simulate_bar_code.save_theoretical_value(n_list,r_list,k_list,folder_str)
    print("\tDONE\n")
    #----------------------------------------------------
    # SIMULATION OF BAR CODES
    #----------------------------------------------------    
    print("\tSimulating molecular barcodes...\n")
    simulate_bar_code.simulate_repeated_sequences(n_list,r_list,k_list,num_of_repeats,num_of_CPUs,folder_str)
    print("\tDONE\n")
    print("\n\tThe results are stored in the folder:\n\t%s\n\n\tExiting script..."%(folder_str))
elif (experiment == "benchmarking_script"):
    # We define our three lists corresponding
    # to the triplet (n,k,r).
    # THE LIST WITH n-VALUES
    n = 4**12 # Big sample
    n_list = [n] # Create a list as input
    # THE LIST WITH r-VALUES
    r = 2 # Length of repeated sample
    r_list = [r] # Create a list as input
    # THE LIST WITH k-VALUES:
    # Since we are interested in benchmarking this code
    # as we are investigating the run time as a function
    # of the number of cores it is mainly interesting to
    # run simulations with large values of k. Therfore, we
    # investigate merely the large values of k in the
    # following vector
    k_min = 10000
    k_max = 50001
    step_length = 10000
    k_list = list(frange(k_min, k_max, step_length)) # Create list
    # For this particular simulation, we actually ignore the
    # number of cores provided by the user. Instead we use the number
    # of cores provided in the following list
    num_of_CPUs_list = list(frange(1,(mp.cpu_count()-1), 2))
    # Also, to do this reliably, we need to calculate the computation time
    # multiple times. So, we invent a variable called "num_of_runs". Thus,
    # we will get "num_of_runs" run times from the benchmarking to do create
    # some plots with.
    num_of_runs = 30
    # Now we run the simulations using two loops
    print("\tThe simulation starts\n")
    # We introduce a nice index to display which
    # iteration we are currently working on
    index = 0
    # We have a temporary string "str"
    str = ""
    # Loop over the CPUs in the CPU list
    for num_of_CPUs_temp in num_of_CPUs_list:
        # Prompt to the user how many CPUs we are using
        if num_of_CPUs_temp==1:
            str = " CPU\n"
        else:
            str = " CPUs\n"
        # Increment the index for printing
        index +=1
        # Print to the user which index we are working on
        print("\tIteration %d out of %d:\tSimulations using %d%s\n"%(index,len(num_of_CPUs_list),num_of_CPUs_temp,str))  
        # We run through all the sub iterations    
        for i in range(num_of_runs):
            print("\t\tSub iter %d out of %d\n"%(i+1,num_of_runs))
            simulate_bar_code.simulate_repeated_sequences(n_list,r_list,k_list,num_of_repeats,num_of_CPUs_temp,folder_str)
else:
    print("\n\tERROR: The experiment could not be found!\n")
    print("\tThe first input corresponding to the experiment could not be found. If you want to add this experiment you are more than welcome to edit this script called launch_simulations.py and add the experiment.\n")
    print("\tAborting execution...\n")
    sys.exit(0) # Exit the program




