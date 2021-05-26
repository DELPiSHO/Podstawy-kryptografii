Funkcje skrótu 1
Przygotować plik personal.txt z ujawnionym imieniem i nazwiskiem. Obliczyć wszystkie funkcje skrótu na tym pliku, wyniki zapisać do pliku hash.txt w kolejności coraz dłuższych skrótów. Przesłać oba pliki.

Funkcje skrótu 2
Przygotować drugą wersje pliku personal_.txt, różniącą się jedynie dodatkowym pustym wierszem na końcu. Obliczyć wartość wszystkich funkcji skrótu dla obu wersji pliku połączonego z tym samym plikiem plikiem wykładu hash.pdf (tzn. wykonać polecenia:
cat hash.pdf personal.txt | md5sum >> hash.txt
cat hash.pdf personal_.txt | md5sum >> hash.txt
itd. dla obu wersji pliku z danymi osobowymi). Następnie sprawdzić liczbę bitów (nie bajtów) różnych w obu wynikach. Należy się spodziewać, że w każdej parze ok. połowa bitów będzie różna. Proszę przesłać oba pliki personal.txt oraz plik diff.txt zawierający sześć par wyników dla każdej z funkcji skrótu i liczbę bitów różniących te wyniki (no i oczywiście program liczący te bity wraz ze źródłem). Nie przesyłać pliku hash.pdf.
Przykładowy plik z wynikami: diff.txt.