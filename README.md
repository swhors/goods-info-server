# goods-info-server
Operating with NaverApiTest Project

# Before run, install rustc
- sudo apt install rustc
- sudo apt install libssl-dev
- sudo apt install pyopenssl
- pip3 install --no-cache -r requirement

# certificate
## create certificate
- openssl genrsa -out private.key 2048
- openssl rsa -in private.key -pubout -out public.key
- openssl req -new -key private.key -out goods
- openssl req -new -key private.key -out private.csr
- openssl req -x509 -days 365 -key private.key -in private.csr -out simpson.crt -days 365

## convert certificate
* openssl x509 -in simpson.crt -out simpson.pem -outform PEM

* openssl x509 -text -noout -in <certificate>
* https://stackoverflow.com/questions/13732826/convert-pem-to-crt-and-key
* https://blusky10.tistory.com/352


#
