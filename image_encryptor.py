
"""
image_encryptor.py
Simple image encryption/decryption using:
 - deterministic pixel permutation (seeded from passphrase)
 - XOR with a keystream (seeded from passphrase)
Works with color (BGR) or grayscale images. Saves output as PNG (lossless).
"""


import cv2
import numpy as np
import hashlib
import argparse
import os
from tkinter import Tk, Button, Label, Entry, filedialog, StringVar


# Utilities for key -> deterministic seeds 
def sha256_to_int(s: str, salt: str = "") -> int:
    """Return a non-negative integer from sha256(salt + s) digest."""
    h = hashlib.sha256((salt + s).encode("utf-8")).digest()
    # Take first 8 bytes -> 64-bit integer
    return int.from_bytes(h[:8], byteorder="big", signed=False)


# Core algorithms 
def generate_permutation(n: int, key: str) -> np.ndarray:
    """Generate a deterministic permutation of range(n) from key."""
    seed = sha256_to_int(key, salt="perm")
    rng = np.random.RandomState(seed % (2**32))
    perm = rng.permutation(n)
    return perm

def generate_keystream(n: int, key: str) -> np.ndarray:
    """Generate a deterministic keystream of n bytes (uint8) from key."""
    seed = sha256_to_int(key, salt="xor")
    rng = np.random.RandomState(seed % (2**32))
    # randint low inclusive, high exclusive, dtype uint8
    return rng.randint(0, 256, size=n, dtype=np.uint8)

def encrypt_bytes(arr_bytes: np.ndarray, key: str) -> np.ndarray:
    """Encrypt a 1-D uint8 array and return encrypted bytes (same shape)."""
    n = arr_bytes.size
    perm = generate_permutation(n, key)
    keystream = generate_keystream(n, key)
    # Permute bytes first
    permuted = arr_bytes[perm]
    # XOR with keystream
    encrypted = np.bitwise_xor(permuted, keystream)
    return encrypted

def decrypt_bytes(enc_bytes: np.ndarray, key: str) -> np.ndarray:
    """Decrypt a 1-D uint8 array encrypted by encrypt_bytes."""
    n = enc_bytes.size
    keystream = generate_keystream(n, key)
    # XOR with keystream -> get permuted bytes
    permuted = np.bitwise_xor(enc_bytes, keystream)
    # Get permutation and invert it
    perm = generate_permutation(n, key)
    inv_perm = np.empty_like(perm)
    inv_perm[perm] = np.arange(n, dtype=np.int64)
    original = permuted[inv_perm]
    return original


# File helpers 
def read_image_as_bytes(path: str):
    """Return (image_array, original_shape, dtype). image_array is np.uint8 array."""
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img, img.shape, img.dtype

def save_bytes_as_image(bytes_flat: np.ndarray, shape, dtype, out_path: str):
    """Reshape flat bytes to shape and save using OpenCV."""
    img = bytes_flat.reshape(shape).astype(dtype)
    # Ensure parent dir exists
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    # Use PNG to avoid lossy compression
    cv2.imwrite(out_path, img)


# High-level encrypt/decrypt functions 
def encrypt_image_file(input_path: str, output_path: str, key: str):
    img, shape, dtype = read_image_as_bytes(input_path)
    flat = img.flatten()
    enc_flat = encrypt_bytes(flat, key)
    save_bytes_as_image(enc_flat, shape, dtype, output_path)

def decrypt_image_file(input_path: str, output_path: str, key: str):
    img, shape, dtype = read_image_as_bytes(input_path)
    flat = img.flatten()
    dec_flat = decrypt_bytes(flat, key)
    save_bytes_as_image(dec_flat, shape, dtype, output_path)



# CLI 
def cli():
    parser = argparse.ArgumentParser(description="Encrypt/decrypt images using pixel manipulation.")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path (prefer .png)")
    parser.add_argument("--key", required=True, help="Passphrase (string) used as key")
    args = parser.parse_args()

    if args.mode == "encrypt":
        encrypt_image_file(args.input, args.output, args.key)
        print(f"Encrypted -> {args.output}")
    else:
        decrypt_image_file(args.input, args.output, args.key)
        print(f"Decrypted -> {args.output}")


# Tkinter GUI 
def launch_gui():
    root = Tk()
    root.title("Image Encryptor (Permutation + XOR)")

    in_path = StringVar()
    out_path = StringVar()
    key_str = StringVar(value="my secret key")

    def browse_input():
        p = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.bmp *.tiff"),("All files","*.*")])
        if p:
            in_path.set(p)

    def browse_output():
        p = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png"),("All files","*.*")])
        if p:
            out_path.set(p)

    def run_encrypt():
        try:
            encrypt_image_file(in_path.get(), out_path.get(), key_str.get())
            status_label.config(text="Encryption completed.")
        except Exception as e:
            status_label.config(text=f"Error: {e}")

    def run_decrypt():
        try:
            decrypt_image_file(in_path.get(), out_path.get(), key_str.get())
            status_label.config(text="Decryption completed.")
        except Exception as e:
            status_label.config(text=f"Error: {e}")

    Label(root, text="Input image:").grid(row=0, column=0, sticky="w")
    Entry(root, textvariable=in_path, width=50).grid(row=0, column=1)
    Button(root, text="Browse", command=browse_input).grid(row=0, column=2)

    Label(root, text="Output file:").grid(row=1, column=0, sticky="w")
    Entry(root, textvariable=out_path, width=50).grid(row=1, column=1)
    Button(root, text="Browse", command=browse_output).grid(row=1, column=2)

    Label(root, text="Key (passphrase):").grid(row=2, column=0, sticky="w")
    Entry(root, textvariable=key_str, width=50).grid(row=2, column=1)

    Button(root, text="Encrypt", command=run_encrypt).grid(row=3, column=0, pady=6)
    Button(root, text="Decrypt", command=run_decrypt).grid(row=3, column=1, pady=6)
    status_label = Label(root, text="", fg="green")
    status_label.grid(row=4, column=0, columnspan=3)

    root.mainloop()


# test helper
def round_trip_test(image_path: str, key: str):
    """Quick test: encrypt then decrypt and compare to original."""
    import tempfile
    enc = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    dec = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    encrypt_image_file(image_path, enc, key)
    decrypt_image_file(enc, dec, key)
    orig = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    got = cv2.imread(dec, cv2.IMREAD_UNCHANGED)
    equal = np.array_equal(orig, got)
    print("Round-trip equality:", equal)
    return equal


# main
if __name__ == "__main__":
    # If run without args, launch GUI; otherwise CLI
    import sys
    if len(sys.argv) == 1:
        launch_gui()
    else:
        cli()
