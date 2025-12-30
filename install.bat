@echo off
echo === Spaghetti App Installer ===

REM Keep window open even on error
setlocal enabledelayedexpansion

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Install Python 3.10 or 3.11 and rerun.
    pause
    exit /b
)

REM Create venv if missing
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

echo === Upgrading pip / setuptools / wheel ===
python -m pip install --upgrade pip setuptools wheel

echo === Installing PyTorch with CUDA ===
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 (
    echo FAILED TO INSTALL PYTORCH
    pause
    exit /b
)

echo === Installing remaining dependencies ===
pip install gradio pillow imageio numpy matplotlib
if errorlevel 1 (
    echo FAILED TO INSTALL DEPENDENCIES
    pause
    exit /b
)

REM Clone NNST repo if missing
if not exist NeuralNeighborStyleTransfer (
    git clone https://github.com/nkolkin13/NeuralNeighborStyleTransfer.git
)

echo === Verifying CUDA ===
python - <<EOF
import torch
print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
assert torch.cuda.is_available(), "CUDA GPU NOT DETECTED"
print("GPU:", torch.cuda.get_device_name(0))
EOF

echo === INSTALL COMPLETE ===
pause
