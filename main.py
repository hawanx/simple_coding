import gnupg


def import_key(gpg, key_path):
    with open(key_path, 'rb') as f:
        key_data = f.read()
    import_result = gpg.import_keys(key_data)
    return import_result


# Initialize the GPG object
gpg = gnupg.GPG(gnupghome='/Users/hawanx/Desktop')  # specify the GPG home directory if needed

# Path to the key file
key_path = '/Users/hawanx/Desktop/privatekey.asc'

# Import the key
result = import_key(gpg, key_path)

# Check the result
if result:
    print('Key imported successfully:')
    for key in result.results:
        print(key)
else:
    print('Failed to import key')

with open('/Users/hawanx/Desktop/test_gpg_enc.csv.gpg', 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='testing123', output='/Users/hawanx/Desktop/output.csv')
