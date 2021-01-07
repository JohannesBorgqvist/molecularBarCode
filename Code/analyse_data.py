#=================================================
# ANALYSE DATA
#=================================================
# SCRIPT WRITTEN BY: Johannes Borgqvist
# DATE: 2020-01-06
# DESCRIPTION:
# The script reads the csv files in the sub folders
# of the "../Results" folder and converts it to a
# tex-folder which will be stored in the various
# sub folders of the "../Figures" folder. These
# tex-files can later be plotted using LaTeX and
# the files for generating the pdf-plots are
# stored in the sub folders of the Figure folder. 
#=================================================
# IMPORTED PACKAGES
#=================================================
import pandas as pd # for reading and writing data files
import numpy as np # for doing numerical calculations (e.g. vector manipulation)
#=================================================
# FUNCTIONS
#=================================================
def generate_LaTeX_plots(x,y,quantiles,colourStr,legendStr,file_str):
    # Define the legend using the "legendStr"
    legendStr = "\\addlegendentry{"+legendStr+"}"
    # Define the end string for plotting
    endStr = "};"
    # Allocate memory for the yStr which will be plotted against the x-value
    yStr = ""
    # The number of plots to include in the file
    num_of_plots = 1
    #Define the various strings that will define the plots in two cases_
    # 1. We are interested in plotting quantiles (y contains three columns to be plotted)
    # 2. We are just interested in a normal 2D plots (i.e. x vs y)
    if quantiles:# Three columns to be plotted
        # In the case of quantiles we want three plots
        num_of_plots = 3
        # Define the defining strings: lower, middle, upper quantiles, legendStr and the fill str between the upper and lower quantiles
        lowerQuantileStr = "\\addplot[forget plot,densely dashed,color="+colourStr+",name path=down]coordinates {"
        middleQuantileStr = "\\addplot[forget plot,densely dashed,color="+colourStr+"]coordinates {"        
        upperQuantileStr = "\\addplot[forget plot,densely dashed,color="+colourStr+",name path=up]coordinates {"
        fillStr = "\\addplot["+colourStr+"!50,opacity=0.1] fill between[of=up and down];"
    else:# Normal x vs y plot
        yStr = "\\addplot[color="+colourStr+"]coordinates {"
    # Open the file to be plotted
    f = open(file_str,"w+")
    # Loop through the number of plots
    for j in range(num_of_plots):
        if quantiles:
            if j == 0:
                yStr =lowerQuantileStr
            elif j == 1:
                yStr =middleQuantileStr
            else:
                yStr =upperQuantileStr                        
        # Write the plot string to the defined file
        f.write("%s\n"%(yStr))
        # Loop through the values in the x vector
        for i in range(x.shape[0]):
            if quantiles:
                f.write("\t(%0.4f\t,\t%0.4f)\n"%(x.iloc[i],y.iloc[j,i]))
            else:
                f.write("\t(%0.4f\t,\t%0.4f)\n"%(x.iloc[i],y.iloc[i]))
        # Write the close string to the file
        f.write("%s\n"%(endStr))    
    # If we have quantiles we add the fill string
    if quantiles:
        f.write("%s\n"%(fillStr))
    # We add the legendentry
    f.write("%s"%(legendStr))
    # Plotting is done, close the file                            
    f.close()
def get_row_dataframe_benchmarking(CPU_index,k_value_index,data_str):
    # Define a data frame using pandas for the input data
    df = pd.DataFrame()
    df = pd.read_csv(data_str)
    # Create a smaller df without unneccessary columns
    df_small = pd.DataFrame()
    df_small = df.iloc[1:df.shape[0],1:df.shape[1]]
    # 3 data frames which we will use to extract
    # specific values from the data fram df_small
    df_CPU = pd.DataFrame()
    df_sorted = pd.DataFrame()
    df_specific_k = pd.DataFrame()
    # We begin by finding the indices for a certain CPU
    indices_for_CPU = df_small[df_small.iloc[:,3]==CPU_index].index.values-1
    # Next we extract these so we only work with 1 CPU at a time
    df_CPU= df_small.iloc[indices_for_CPU,:]
    # Next, we sort the CPUs with respect to the k-values in
    # ascending order (small to large)
    df_sorted = df_CPU.sort_values(by='2',ascending=True)
    # We extract these indices to get the number of k-values, i.e.
    # times that we benchmarked the application
    indices_for_k = df_sorted[df_sorted.iloc[:,2]==k_value_index*10000].index.values-1
    # We define a start index which for this application is the k-value
    # divided by 10000 subtracted by one multiplied by "len(indices_for_k)"
    startIndex = ( k_value_index - 1 ) * len(indices_for_k)
    # Define a list which we fill with execution times
    execution_times = []
    # Since it will eventually contain "len(indices_for_k)" values
    # we loop this number of times and then append the execution
    # time to this vector. Finally, we return this vector as a
    # data frame. 
    for i in range(len(indices_for_k)):
        execution_times.append(df_sorted.iloc[i+startIndex,5])
    return np.asarray(execution_times)
def get_dataframe_benchmarking(CPU_index,num_of_k_values,data_str):
    # First we save the execution time for the first 
    A = get_row_dataframe_benchmarking(CPU_index,1,data_str)
    for k_value_index in range(2,(num_of_k_values+1)):
        newrow = get_row_dataframe_benchmarking(CPU_index,k_value_index,data_str)
        A = np.vstack([A, newrow])    
    return pd.DataFrame(A)




