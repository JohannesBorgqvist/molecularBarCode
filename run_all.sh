#!/bin/bash
#=======================================================================
cd ./Code/
echo "============================================================"
echo "RUNNING SCRIPT 1 OUT OF 3"
echo ""
echo ""
echo "Calculating both the theoretical boundaries on the expected values"
echo "and comparing it with simulations with increasing k-values. "
echo "The theoretical values take some time to calculate.  "
echo "The results are stored in the folder:"
echo "../Results/theoretical_vs_simulated"
echo "and the procedure is repeated 1000 times"
echo "============================================================"
echo " "
echo ""
python3 launch_simulations.py theoretical_vs_simulated 1000 7
echo "============================================================"
echo "RUNNING SCRIPT 2 OUT OF 3"
echo ""
echo ""
echo "Benchmarking the script. This has the same setting but we "
echo "repeat one set of simulations 30 times with an increasing number "
echo "of CPUs. "
echo "The results are stored in the folder:"
echo "../Results/benchmarking_script"
echo "and simulations takes hours to execute in total."
echo "So preferrably one should run these scripts over night."
echo "============================================================"
echo " "
echo ""
python3 launch_simulations.py benchmarking_script 1000
echo "============================================================"
echo "RUNNING SCRIPT 3 OUT OF 3"
echo ""
echo ""
echo "We generate the corresponding figures"
echo "The results are stored in the folders:"
echo "../Results/Fig1/Input and ../Results/Fig2/Input"
echo "============================================================"
echo " "
echo ""
python3 generate_figures.py
rm -r __pycache__
echo "Generating Figure 1"
echo ""
cd ../Figures/Fig1
pdflatex SubFigures.tex && pdflatex Fig1.tex
echo "Done"
echo ""
echo "Generating Figure 2"
echo ""
cd ../Fig2/ && pdflatex Fig2.tex && cd ../../
echo "Done"
echo ""
echo "Calculations are done and figures are generated!"
echo ""
echo "Go ahead and read the report in:"
echo "./MathematicalBackground"
