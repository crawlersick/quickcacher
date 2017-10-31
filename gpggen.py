import os
import gnupg
homep='/home/sick/gpghome'

os.system('rm -rf '+homep)
gpg = gnupg.GPG(gnupghome=homep)
input_data = gpg.gen_key_input(
            name_email='testgpguser@mydomain.com',
                passphrase='my passphrase')
key = str(gpg.gen_key(input_data))
print (key)
ascii_armored_public_keys = gpg.export_keys(key)
ascii_armored_private_keys = gpg.export_keys(key, True)
with open(homep+'/gpg.pub', 'w') as f:
        f.write(ascii_armored_public_keys)
with open(homep+'/gpg.prv', 'w') as f:
        f.write(ascii_armored_private_keys)

