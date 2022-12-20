#! /bin/bash

# First use powerpoint to export the slides to PDF 
# Note: export to PDF, not print to PDF, otherwise trimming will not work.

if [[ -e "~\$figures.pptx" ]]; then
    echo "Close powerpoint (or delete old ~\$figures.pptx) before running this script"
    exit 1
fi

if [[ ! -e figures.pdf ]]; then
    echo "PDF does not exist; export Powerpoint to PDF first (export, don't print!)"
    exit 1
fi

if [[ figures.pptx -nt figures.pdf ]]; then
    echo "Powerpoint is newer than PDF; export Powerpoint to PDF first (export, don't print!)"
    exit 1
fi

echo "Converting PDF to PNG"
magick convert -density 300 -units pixelsperinch -trim +profile "icc" figures.pdf figures.png

echo "Renaming files"
mv figures-0.png monolithic-quantum-computer-circuit-example.png
mv figures-1.png monolithic-quantum-computer-city-plot.png
mv figures-2.png single-qubit-gate-global-to-local-mapping.png
mv figures-3.png two-qubit-gate-global-to-local-mapping-same-processor.png
mv figures-4.png quantum-processor-registers.png
mv figures-5.png 4-bit-local-quantum-fourier-transformation.png
mv figures-6.png bloch-multi-vector-for-4-bit-qft-with-input-3.png
mv figures-7.png density-matrix-city-plot-for-4-bit-qft-with-input-3.png
