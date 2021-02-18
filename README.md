# goods-info-server
Operating with NaverApiTest Project

# Before run, install rustc
- sudo apt install rustc
- sudo apt install libssl-dev
- sudo apt install pyopenssl
- pip3 install --no-cache -r requirement

# certificate
## create certificate
- openssl genrsa -out ssh/private.key 2048
- openssl rsa -in ssh/private.key -pubout -out ssh/public.key
- openssl req -new -key ssh/private.key -out ssh/private.csr
- openssl req -x509 -days 365 -key ssh/private.key -in ssh/private.csr -out ssh/simpson.crt -days 365

## convert certificate
* openssl x509 -in ssh\simpson.crt -out ssh\simpson.pem -outform PEM

* openssl x509 -text -noout -in <certificate>
* https://stackoverflow.com/questions/13732826/convert-pem-to-crt-and-key
* https://blusky10.tistory.com/352


#
