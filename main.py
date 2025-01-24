from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Directory to save uploaded and processed files
UPLOAD_DIR = "uploads"
COMPRESSED_DIR = "compressed"
DECOMPRESSED_DIR = "decompressed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(COMPRESSED_DIR, exist_ok=True)
os.makedirs(DECOMPRESSED_DIR, exist_ok=True)

# LZ78 Compression Function
def lz78_compress(input_data):
    dictionary = {}
    data = input_data.decode('utf-8')
    compressed = []
    
    current_string = ""
    dict_size = 1

    for char in data:
        combined = current_string + char
        if combined not in dictionary:
            if current_string:
                compressed.append((dictionary[current_string], char))
            else:
                compressed.append((0, char))
            dictionary[combined] = dict_size
            dict_size += 1
            current_string = ""
        else:
            current_string = combined

    if current_string:
        compressed.append((dictionary[current_string], ""))

    return compressed

# LZ78 Decompression Function
def lz78_decompress(compressed):
    dictionary = {}
    decompressed = ""
    dict_size = 1

    for index, char in compressed:
        if index == 0:
            entry = char
        else:
            entry = dictionary[index] + char

        decompressed += entry
        dictionary[dict_size] = entry
        dict_size += 1

    return decompressed

# API Endpoint to Upload and Compress File
@app.post("/compress")
async def compress_file(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(COMPRESSED_DIR, file.filename + ".lz78")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    with open(input_path, "rb") as f:
        input_data = f.read()
        compressed = lz78_compress(input_data)

    with open(output_path, "w") as f:
        f.write(str(compressed))

    return {"message": "File compressed successfully", "compressed_file": output_path}

# API Endpoint to Decompress File
@app.post("/decompress")
async def decompress_file(file: UploadFile = File(...)):
    input_path = os.path.join(COMPRESSED_DIR, file.filename)
    output_path = os.path.join(DECOMPRESSED_DIR, file.filename.replace(".lz78", ""))

    with open(input_path, "wb") as f:
        f.write(await file.read())

    with open(input_path, "r") as f:
        compressed = eval(f.read())
        decompressed = lz78_decompress(compressed)

    with open(output_path, "w") as f:
        f.write(decompressed)

    return {"message": "File decompressed successfully", "decompressed_file": output_path}

# Endpoint to Download Files
@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    return FileResponse(file_path)

# Run with: uvicorn filename:app --reload
