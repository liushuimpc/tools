
=== Generate a RSA private key ===
openssl genrsa -out test.key 1024


=== Extract public key from private key ===
openssl rsa -in test.key -pubout -out test_pub.key


=== Encrypt the file.txt via public key ===
openssl rsautl -encrypt -in file.txt -inkey test_pub.key -pubin -out file-encrypted.txt


=== Decrypt the file-encrypted.txt via private key ===
openssl rsautl -decrypt -in file-encrypted.txt -inkey test.key -out file-decrypted.txt


=== Signature file.txt via private key ===
openssl rsautl -sign -in file.txt -inkey test.key -out file.txt.sign


=== Verify the file.txt.sign via public key ===
openssl rsautl -verify -in file.txt.sign -inkey test_pub.key -pubin -out file_verify.txt
