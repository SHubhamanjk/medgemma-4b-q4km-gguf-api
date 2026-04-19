# MedGemma 4B Quantization Guide

This project packages Google MedGemma 4B for local inference by converting the original Hugging Face model into GGUF format and then quantizing it for smaller size and faster runtime. The workflow covered here is:

1. Download the original MedGemma 4B model from Hugging Face.
2. Convert the model to F16 GGUF using llama.cpp.
3. Quantize the GGUF model to Q4_K_M for local deployment.
4. Run inference or expose it through a FastAPI service.

The end result is a compact `.gguf` model that can be used with llama.cpp tooling or inside a Dockerized API.


## Download Quantized Model

Download the quantized model (~2.3 GB) from here: [Click here](https://drive.google.com/file/d/10mrYgRlPNVCeLPZPMxb1hdAX-dGSw5Me/view?usp=sharing)

## Complete Steps from Zero to Quantized Model

### Step 1: Environment Setup

1. Create and activate Python virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Set execution policy (if needed):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

3. Install required Python packages:
```powershell
uv pip install --index-url https://pypi.org/simple "transformers<5" huggingface_hub sentencepiece accelerate numpy gguf protobuf torch~=2.6.0 --extra-index-url https://download.pytorch.org/whl/cpu
```

### Step 2: Hugging Face Authentication

1. Create `.env` file in project root with your HF token:
```
HF_TOKEN=hf_your_token_here
```

2. Login to Hugging Face CLI:
```powershell
$env:HF_TOKEN = (Get-Content .env | Select-String "^HF_TOKEN=" | ForEach-Object { ($_ -split "=",2)[1].Trim() })
huggingface-cli login --token $env:HF_TOKEN
huggingface-cli whoami
```

### Step 3: Download Model from Hugging Face

```powershell
hf download google/medgemma-4b-it --local-dir medgemma --local-dir-use-symlinks False
```

This downloads the original model (~8 GB) to the `medgemma/` folder.

### Step 4: Setup llama.cpp

```powershell
cd .\llama.cpp-master
```

Build the C++ tools on Windows:
```powershell
cmake -S . -B build -DGGML_CUDA=OFF
cmake --build build --config Release -j
```

### Step 5: Convert HF Model to F16 GGUF

From inside `llama.cpp-master` directory:
```powershell
python convert_hf_to_gguf.py ..\medgemma --outfile medgemma-f16.gguf --outtype f16
```

This creates `medgemma-f16.gguf` (~8 GB).

### Step 6: Quantize to Q4_K_M

```powershell
.\build\bin\Release\llama-quantize.exe .\medgemma-f16.gguf .\medgemma-Q4_K_M.gguf Q4_K_M
```

This creates the final quantized model `medgemma-Q4_K_M.gguf` (~2-3 GB).

**Note:** If the exe path differs, find it with:
```powershell
Get-ChildItem .\build -Recurse -Filter *quantize*.exe
```

### Step 7: Test Inference

Run inference with the quantized model:
```powershell
.\build\bin\Release\llama-cli.exe -m .\medgemma-Q4_K_M.gguf -p "Explain symptoms of pneumonia"
```

## File Sizes

- **Original HF model** (medgemma/): ~8 GB
- **F16 GGUF** (medgemma-f16.gguf): ~8 GB  
- **Q4_K_M quantized** (medgemma-Q4_K_M.gguf): ~2-3 GB

Check sizes with:
```powershell
Get-Item .\llama.cpp-master\medgemma-Q4_K_M.gguf | Select-Object FullName, @{Name="SizeGB";Expression={[math]::Round($_.Length/1GB,2)}}
```

## Troubleshooting

- **PowerShell backslash errors**: Use backticks (`) for line continuation or single-line commands
- **transformers==5.5.1 not found**: Use `transformers<5` instead of pinned version
- **HF login fails**: Verify token is valid and has model access permissions
- **Quantize exe not found**: Run cmake build commands first

## Download Quantized Model

Download the quantized model (~2-3 GB) from here: [Click here](https://drive.google.com/file/d/10mrYgRlPNVCeLPZPMxb1hdAX-dGSw5Me/view?usp=sharing)


