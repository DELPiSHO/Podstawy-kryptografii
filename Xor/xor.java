import java.io.*;
import java.nio.charset.StandardCharsets;

//Yauheni Dzianisau
//238213

public class xor{

    public void przygotowanie(){
        File orig = new File("orig.txt");
        File plain = new File("plain.txt");
        String text = "";
        String allText = "";
        StringBuilder stringBuilder = new StringBuilder(allText);
        try {
            try {
                try {
                    Reader reader = new InputStreamReader(new FileInputStream(orig), StandardCharsets.US_ASCII);
                    BufferedReader bufferedReader = new BufferedReader(reader);
                    Writer writer = new OutputStreamWriter(new FileOutputStream(plain), StandardCharsets.UTF_8);
                    BufferedWriter bufferedWriter = new BufferedWriter(writer);
                    String plainText = "";
                    text = bufferedReader.readLine();
                    while(text!=null){
                        text = text.replaceAll("[,.!?:;'-0123456789]", "");
                        text = text.toLowerCase();
                        plainText = text.substring(0, 35);
                        stringBuilder.append(plainText);
                        stringBuilder.append("\n");
                        text = bufferedReader.readLine();
                    }
                    allText = stringBuilder.toString();
                    bufferedWriter.write(allText);
                    bufferedWriter.close();
                    bufferedReader.close();
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public byte[] klucz(){
        File kluczFile = new File("key.txt");
        String kluczString = new String("");
        int x;
        try {
            try {
                Reader reader = new InputStreamReader(new FileInputStream(kluczFile),StandardCharsets.US_ASCII);
                BufferedReader kluczReader = new BufferedReader(reader);
                try {
                    kluczString = kluczReader.readLine();
                    byte[] bytes = kluczString.getBytes(StandardCharsets.US_ASCII);
                    for(x = 0; x <= kluczString.length()-1; x++){
                        bytes[x] -= 97;
                    }
                    return bytes;
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }
            } catch (FileNotFoundException e) {
                System.out.println("Brak pliku key.txt");
                }
        } catch (IOException e) {
            System.out.println("Cos jest nie tak z plikiem");
            }
        return null;
    }

    public void szyfruj(byte[] klucz){
        File plain = new File("plain.txt");
        File crypto = new File("crypto.txt");
        String text="";
        String allText = "";
        StringBuilder stringBuilder = new StringBuilder(text);
        int wynik = 0;
        try {
            try {
                try {
                    Reader reader = new InputStreamReader(new FileInputStream(plain),StandardCharsets.US_ASCII);
                    BufferedReader bufferedReader = new BufferedReader(reader);
                    Writer writer = new OutputStreamWriter(new FileOutputStream(crypto), StandardCharsets.US_ASCII);
                    BufferedWriter bufferedWriter = new BufferedWriter(writer);
                    text = bufferedReader.readLine();
                    while (text!=null) {
                        stringBuilder.append(text);
                        stringBuilder.append("\n");
                        text = bufferedReader.readLine();
                    }
                    allText = stringBuilder.toString();
                    byte[] bytes = allText.getBytes(StandardCharsets.US_ASCII);
                    int x = 0;
                    int y = 0;
                    char[] znak = new char[bytes.length];
                    StringBuilder record = new StringBuilder(znak[y]);
                    for (y = 0;y <= bytes.length-1;y++) {
                        if(x >= klucz.length - 1){
                            x = 0;
                            }
                        wynik = bytes[y] + klucz[x];
                        x += 1;
                        if(wynik > 122){
                            wynik -= 25;
                            }
                        if(bytes[y] == 10){
                            wynik = 10;
                            x = 0;
                            }
                        znak[y] = (char)wynik;
                        record.append(znak[y]);
                    }
                    allText = record.toString();
                    bufferedWriter.write(allText);
                    bufferedWriter.close();
                    bufferedReader.close();
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void kryptoanaliza(){
        File crypto = new File("crypto.txt");
        File decrypt = new File("decrypt.txt");
        try {
            try {
                try {
                    Reader reader = new InputStreamReader(new FileInputStream(crypto),StandardCharsets.US_ASCII);
                    BufferedReader bufferedReader = new BufferedReader(reader);
                    Writer writer = new OutputStreamWriter(new FileOutputStream(decrypt), StandardCharsets.US_ASCII);
                    BufferedWriter bufferedWriter = new BufferedWriter(writer);
                    int x = 20;
                    int y = 0;

                    String text = bufferedReader.readLine();
                    int textLen = text.length();
                    byte[][] arr = new byte[x][textLen];
                    while(text!=null){
                        arr[y] = text.getBytes(StandardCharsets.US_ASCII);
                        y += 1;
                        text = bufferedReader.readLine();
                    }
                    bufferedReader.close();
                    byte[] bytes = new byte[textLen];
                    int[] bytesPass = new int[textLen];
                    for(int i = 0; i <= 19; i++){
                        for(y = 0; y <= textLen-1; y++ ){
                            if(arr[i][y] < 58){
                                bytes[y] = 32;
                                bytesPass[y] = arr[i][y] - bytes[y];
                            }
                        }
                    }
                    int a = 0;
                    char[] znak = new char[textLen];
                    StringBuilder stringBuilder = new StringBuilder(znak[a]);
                    String koniec = "";
                    for(int i = 0; i <= 19; i++){
                        for(y = 0; y <= textLen - 1; y++ ){
                            arr[i][y] -= bytesPass[y];
                            if (arr[i][y] < 97 && arr[i][y] > 33) { arr[i][y] += 25; }
                            znak[y] = (char)arr[i][y];
                            stringBuilder.append(znak[y]);
                        }
                        stringBuilder.append("\n");
                    }
                    koniec = stringBuilder.toString();
                    bufferedWriter.write(koniec);
                    bufferedWriter.close();
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        String[] arg = args;
        byte[] klucz;
        xor start = new xor();
        switch (arg[0]) {

            case "-p":
                start.przygotowanie();
                System.out.println("Przygotowanie pliku plain.txt");
                break;

            case "-e":
                klucz = start.klucz();
                start.szyfruj(klucz);
                System.out.println("Szyfrowanie...");
                break;

            case "-k":
                start.kryptoanaliza();
                System.out.println("Kryptoanaliza");
        }
    }
}
