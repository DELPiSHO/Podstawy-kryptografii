Program o nazwie xor powinien umożliwiać wywołanie z linijki rozkazowej z następującymi opcjami:
-p (przygotowanie tekstu do przykładu działania),
-e (szyfrowanie),
-k (kryptoanaliza wyłącznie w oparciu o kryptogram)

Nazwy plików są następujące:
orig.txt: plik zawierający dowolny tekst,
plain.txt: plik z tekstem zawierającym co najmniej kilkanaście linijek równej długości, np. 64,
key.txt: plik zawierający klucz, który jest ciągiem dowolnych znaków podanej wyżej długości,
crypto.txt: plik z tekstem zaszyfrow, każda jego linijka jest operacją ⊕ z kluczem,
decrypt.txt: plik z tekstem odszyfrowanym.

Oceniane będą wyłącznie programy zawierające kryptoanalizę.