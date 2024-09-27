import os

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from secure_drop import constants


def encrypt_RSA(data: bytes) -> bytes:
    """Encrypts data using RSA.

    Args:
        data (bytes): The plaintext to encrypt.

    Returns:
        bytes: Ciphertext.
    """
    public_key = __get_public_key()
    rsa_enc_obj = PKCS1_OAEP.new(public_key)
    return rsa_enc_obj.encrypt(data)


def decrypt_RSA(data: bytes) -> bytes:
    """Decrypts data using RSA.

    Args:
        data (bytes): The ciphertext to decrypt.

    Returns:
        bytes: Plaintext.
    """
    private_key = __get_private_key()
    rsa_enc_obj = PKCS1_OAEP.new(private_key)
    return rsa_enc_obj.decrypt(data)

#AES is used to encrypt large files and than the key is encrypted with RSA and sent to the reciever.
def encrypt_AES(file_path: str) -> (bytes, str):
    """Encrypts a file using the AES encryption algorithm and encrypts key using encrypt_RSA
    returns the encrypted AES key and the path to the encrypted file .

    Args:
        file_path (str): The path to the file you want to encrypt.

    Returns:
        Tuple[bytes, str]: A tuple containing the encrypted AES key and the path to the encrypted file.
    """

    # Checks if File path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    # Generates a random AES key for 128 bit encryption
    aes_key = get_random_bytes(16) 

    # Encrypt the AES key with RSA
    encrypted_aes_key = encrypt_RSA(aes_key)

    # Encrypt the file
    cipher = AES.new(aes_key, AES.MODE_CFB)
    encrypted_file_path = file_path + '.aes'
    with open(file_path, 'rb') as input_file:
        with open(encrypted_file_path, 'wb') as output_file:
            output_file.write(cipher.iv)
            while chunk := input_file.read(64 * 1024):  # Reads in 64KB in chunks
                output_file.write(cipher.encrypt(chunk))

    return encrypted_aes_key, encrypted_file_path

def decrypt_AES(encrypted_file_path: str, encrypted_aes_key: bytes) -> str:
    """Decrypts an AES-encrypted file using a decrypted AES key and 
    returns the path to the decrypted file.

    Args:
        encrypted_file_path (str): The path to the AES-encrypted file.
        encrypted_aes_key (bytes): The encrypted AES key to decrypt the file.

    Returns:
        str: The path to the decrypted file.
    """

     # Check if the encrypted file exists at the given path
    if not os.path.exists(encrypted_file_path):
        raise FileNotFoundError(f"The encrypted file '{encrypted_file_path}' does not exist.")

    # Decrypt the AES key with RSA
    aes_key = decrypt_RSA(encrypted_aes_key)


    decrypted_file_path = encrypted_file_path + '_decrypted'  # Append '_decrypted' to the file name

    # Decrypt the file
    with open(encrypted_file_path, 'rb') as input_file:
        iv = input_file.read(AES.block_size)
        cipher = AES.new(aes_key, AES.MODE_CFB, iv)
        decrypted_file_path = encrypted_file_path.rstrip('.aes')
        with open(decrypted_file_path, 'wb') as output_file:
            while chunk := input_file.read(64 * 1024):  # Reading in 64KB chunks
                output_file.write(cipher.decrypt(chunk))

    return decrypted_file_path

def __get_public_key() -> RSA.RsaKey:
    """Retrives the public key that SecureDrop generated. If a key pair has not yet been generated, this will first generated the key pair.

    Returns:
        RSA.RsaKey: The public key.
    """

    if not __keys_exist():
        __generate_key_pair()

    return __get_key(constants.PUBLIC_KEY_FILE_PATH)


def __get_private_key() -> RSA.RsaKey:
    """Retrives the private key that SecureDrop generated. If a key pair has not yet been generated, this will first generated the key pair.

    Returns:
        RSA.RsaKey: The private key.
    """

    if not __keys_exist():
        __generate_key_pair()

    return __get_key(constants.PRIVATE_KEY_FILE_PATH)


def __keys_exist() -> bool:
    """Determines whether public and private keys exist for SecureDrop.

    Returns:
        bool: True if public and private keys exist; False otherwise.
    """

    return os.path.exists(constants.PUBLIC_KEY_FILE_PATH) and os.path.exists(constants.PRIVATE_KEY_FILE_PATH)


def __generate_key_pair():
    """Generates an RSA key pair and stores both keys in .pem files.
    """

    private_key = RSA.generate(2048)
    with open(constants.PRIVATE_KEY_FILE_PATH, "wb") as f:
        f.write(private_key.export_key("PEM"))
        f.close()

    public_key = private_key.public_key()
    with open(constants.PUBLIC_KEY_FILE_PATH, "wb") as f:
        f.write(public_key.export_key("PEM"))
        f.close()


def __get_key(key_file_path: str) -> RSA.RsaKey:
    """Imports an RSA key stored in a .pem file at a given path.

    Args:
        key_file_path (str): The path at which the .pem file containing the desired key is located.

    Raises:
        RuntimeError: Raised if the provided key file path does not exist.

    Returns:
        RSA.RsaKey: The imported RSA key.
    """

    if not os.path.exists(key_file_path):
        raise RuntimeError(f"Specified key file does not exist: {key_file_path}")

    with open(key_file_path, "rb") as f:
        key = RSA.import_key(f.read())
        f.close()

    return key
