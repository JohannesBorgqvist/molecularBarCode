#=================================================
# LAUNCH SIMULATIONS
#=================================================
# SCRIPT WRITTEN BY: Johannes Borgqvist
# DATE: 2020-01-04
# DESCRIPTION:
# The script generates converts the data
# files in csv-format which are stored in
# the sub folders of the "../Results" folder
# to tex-files stored in the sub folders of
# the "../Figures" folder. It does so by
# accessing the script named "analyse_data.py".
#=================================================
# IMPORTED SCRIPT
#=================================================
import analyse_data # For conducting the conversions
import pandas as pd # for reading and writing data files
#================================================================        
# FIGURE FOR COUNTING MOLECULAR BARCODES (FIGURE 1):
#================================================================        
# Prompt to user
print("\tGenerating Figure 1\n")
# Find the folder in which we store the data 
folder_str = "../Results/theoretical_vs_simulated"
data_str = folder_str + "/simulatedOutput.csv"
# Define a data frame using pandas
df = pd.DataFrame()
df = pd.read_csv(data_str)
# Create a smaller df without unneccessary columns
df_small = pd.DataFrame()
df_small = df.iloc[1:df.shape[0],1:df.shape[1]]
# Extract the x-vector
x = pd.DataFrame()
x = df_small.iloc[:,2]
# Extract all y-values 
dataPoints = pd.DataFrame()
dataPoints = df_small.iloc[:,5:df.shape[1]]
# Calculate the quantiles which we would like to plot
y = pd.DataFrame()
y = dataPoints.quantile([0.05, 0.50, 0.95],axis = 1)
# Generate the LaTeX plots
quantileVal = True
colourStr = "blue"
legendStr = "Simulated data"
file_str = "../Figures/Fig1/Input/sim.tex"
analyse_data.generate_LaTeX_plots(x,y,quantileVal,colourStr,legendStr,file_str)
# Now we save the theoretical values 
data_str = folder_str + "/theoreticalOutput.csv"
# Read the whole data frame into a pandas frame
df = pd.read_csv(data_str)
# Extract the important data points without empty columns etc.
df_small = df.iloc[1:df.shape[0],1:df.shape[1]]
# Extract the x-vector
x = df_small.iloc[:,2]
# Extract the lower theoretical value
E_L = df_small.iloc[:,3]
# Extract the lower theoretical value
E_U = df_small.iloc[:,4]
# Generate the LaTeX plots: E_L
quantileVal = False
colourStr = "magenta!50"
legendStr = "$E_L$"
file_str = "../Figures/Fig1/Input/E_L.tex"
analyse_data.generate_LaTeX_plots(x,E_L,quantileVal,colourStr,legendStr,file_str)
# Generate the LaTeX plots: E_U
colourStr = "magenta"
legendStr = "$E_U$"
file_str = "../Figures/Fig1/Input/E_U.tex"
analyse_data.generate_LaTeX_plots(x,E_U,quantileVal,colourStr,legendStr,file_str)

# Prompt to user
print("\tDONE!\n")
print("\tThe files are stored in:\n")
print("\t../Figures/Fig1/\n\n")
#================================================================        
# FIGURE FOR BENCHMARKING IMPLEMENTATION (FIGURE 2):
#================================================================        
# Prompt to user
print("\tGenerating Figure 2\n")
#****************************************************************
# STUFF FOR INPUT
#****************************************************************
folder_str = "../Results/benchmarking_script"
data_str = folder_str + "/benchmark.csv"
CPU_index = 1
num_of_k_values = 5
quant = pd.DataFrame()
y = pd.DataFrame()
#****************************************************************
# STUFF FOR OUTPUT
#****************************************************************
# Generate the LaTeX plots
quantileVal = True
colour_strings = ["blue", "magenta", "orange"]
core_strings = ["1", "3", "5"]
cores = [1, 3, 5]
legendStr_partial = " CPU(s)"
file_str_partial = "../Figures/Fig2/Input/"
k_vec = [10000, 20000, 30000, 40000, 50000]
x = pd.DataFrame(k_vec)
#-----------------------------------------------------------------
# Calculate the input vector
#-----------------------------------------------------------------
for i in range(len(cores)):
    y = analyse_data.get_dataframe_benchmarking(cores[i],num_of_k_values,data_str)
    quant = y.quantile([0.05, 0.50, 0.95],axis = 1)
    colourStr = colour_strings[i]
    legendStr = core_strings[i] + legendStr_partial
    file_str = file_str_partial + core_strings[i] + ".tex"
    analyse_data.generate_LaTeX_plots(x,quant,quantileVal,colourStr,legendStr,file_str)
# Prompt to user
print("\tDONE!\n")
print("\tThe files are stored in:\n")
print("\t../Figures/Fig2/\n\n")
