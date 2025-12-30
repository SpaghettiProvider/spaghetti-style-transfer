# Spaghetti Neural Style Transfer App

A simple desktop UI for Neural Neighbor Style Transfer using a local NVIDIA GPU.

## Requirements
- Windows
- NVIDIA GPU
- CUDA installed
- Python 3.10+ (64-bit)

## How to Run Locally
- Download the project files into thier own folder
- Double-click `install.bat` (first time only)
- Double-click `run.bat`
- Open the web UI in your browser


## Notes
- GPU-only (CUDA required)
- Rendering times will vary based on GPU (a 2080ti can take 20-40seconds)
- I've also made version to run/modify in Colab, for those without access to a machine. These will take at least 60 seconds to render.

## How to Run In Google Colab
## This project can be run entirely in Google Colab, using a free GPU, without installing anything locally.

-Go to: https://colab.research.google.com
-Upload the Colab notebook
-Upload the provided .ipynb file from this repository (for example: SpaghettiNeuralNeighbour.ipynb or Spaghetti_UI.ipynb)
-Make sure to Click Runtime → Change runtime type → GPU
-See interal documentation for further instructions



See here for original AI information
https://github.com/nkolkin13/NeuralNeighborStyleTransfer
