# Image Encryption & Decryption Tool  
 "Internship Task 2 – Pixel Manipulation Based Image Encryption using Python"

This project implements a simple image encryption and decryption tool using "pixel permutation" and "XOR-based operations".  
It demonstrates how basic cryptography concepts can be applied to images using "OpenCV, NumPy, Tkinter, and SHA-256 hashing".

---

## Task Summary

This tool allows users to:

- Load any image (JPG, PNG, BMP, etc.)
- Encrypt the image using:
  - Pixel shuffling (permutation)
  - XOR operation with a deterministic keystream
- Decrypt the encrypted image using the same key
- Use either:
  - Graphical User Interface (Tkinter)
  - Command Line Interface (CLI)

This project is part of my internship task to learn:
- Image processing  
- Deterministic randomness  
- Reversible encryption logic  
- Python GUI development  
- Git and GitHub workflow  

---

## Technologies Used
- Python 3  
- OpenCV  
- NumPy  
- Tkinter  
- Hashlib (SHA-256)  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/nethra567/PRODIGY_CS_02.git
cd PRODIGY_CS_02
````

### 2. Install dependencies

```bash
pip install numpy opencv-python
```

---

## Usage

### Run GUI Version

```bash
python image_encryptor.py
```

### GUI Features

- Browse images
- Select output file
- Enter encryption key
- Click "Encrypt" or "Decrypt"

---

## Command Line Version

### Encrypt

```bash
python image_encryptor.py encrypt input.jpg encrypted.png --key "mysecretkey"
```

### Decrypt

```bash
python image_encryptor.py decrypt encrypted.png decrypted.png --key "mysecretkey"
```

> Note: Always use `.png` for encrypted images to avoid compression issues.

---

## Task Structure


image-encryption-tool/
│
├── image_encryptor.py      # Main encryption/decryption + GUI script
├── README.md               # Documentation
└── sample/                 # Sample images


---

## How the Encryption Works

### 1. Pixel Permutation

A deterministic permutation of pixel positions is generated using:

```
SHA-256(key + "perm")
```

-Same key → same permutation
-Wrong key → decryption fails

### 2. XOR Operation

A SHA-256–based keystream is generated.
Each pixel is XOR-ed with the keystream.

---

## Decryption Process

Decryption simply reverses the encryption:

1. XOR again using the same keystream
2. Apply the inverse permutation

- Fully reversible
- Key-dependent
- Simple to understand
 
  Original Image
 <img width="225" height="225" alt="Original" src="https://github.com/user-attachments/assets/965e0baf-37d6-4c9f-9420-41ff7c85b864" />
 
 Encrypted Image
 <img width="225" height="225" alt="encrypted" src="https://github.com/user-attachments/assets/6aab7be0-f3ba-4d67-bc60-617d97c8a9b5" />
 Decrypted Image
 <img width="225" height="225" alt="decrypted" src="https://github.com/user-attachments/assets/bf799246-9f3f-470f-979d-a595dc92e3dc" />
