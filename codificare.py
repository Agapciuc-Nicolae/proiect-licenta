import os.path
import numpy as np
import hashlib
from PIL import Image
from Crypto.Cipher import AES

# clasa Codificare pentru a gestiona activitățile de codificare
class Codificare:
    # Constructor parametrizat pentru a primi imaginea, parola și textul de codificat în timpul inițializării obiectului
    def __init__(self, cale_imagine, parola, mesaj_de_codif):
        self.cale_imagine = cale_imagine
        self.parola = parola.strip()
        self.mesaj_de_codif = mesaj_de_codif.strip()

    # metodă pentru a verifica dacă imaginea există
    # returnează adevărat dacă imaginea este există, altfel returnează fals
    def imagine_verificat(self):
        # verifică dacă imaginea există
        if os.path.exists(self.cale_imagine):
            return True
        return False

    # metodă pentru a verifica dacă textul furnizat există
    # returnează adevărat dacă textul există, altfel returnează fals
    def text_verificat(self):
        # verificare dacă textul este vid
        if len(self.mesaj_de_codif) == 0:
            return False
        return True

    # metodă pentru a verifica dacă parola furnizată există
    # returnează adevărat dacă parola există, altfel returnează fals
    def parola_verificata(self):
        # verificare dacă parola există
        if len(self.parola) == 0:
            return False
        return True

    # operatia pentru a obține valoarea binară a textului furnizat pentru a fi codificat
    # returnează echivalentul binar al textului dat
    def text_binar(self):  
        # generarea unei chei hexadecimale de 32 de octeți din parola furnizată pentru a o utiliza ca cheie secretă aes
        cheia_secreta = hashlib.sha1(str(self.parola).encode()).hexdigest()[:32]
        # crearea unui obiect PyCrypto AES pentru codificare
        cheie_codificare = AES.new(cheia_secreta.encode('utf-8'), AES.MODE_EAX, cheia_secreta.encode())
        # generarea de text criptat folosind obiectul AES și textul de codat
        # returnează octeți criptați
        text_codificat = cheie_codificare.encrypt(self.mesaj_de_codif.encode('utf-8'))
        # convertirea obiectului de octeți criptați în șir pentru ușurință
        text_codificat = str(text_codificat)
        # adăugarea unui text delimitator în șirul criptat pentru a indica terminarea textului ascuns
        text_codificat += "$@&#" 
        # generarea unei valori binare din șirul criptat
        # funcția ord convertește fiecare caracter al șirului criptat în echivalentul său unicode
        # funcția de format formatează caracterul criptat valoarea Unicode în biți binari
        # funcția de unire unește valoarea binară a fiecărui caracter din buclă
        valoare_binara = ''.join([format(ord(character), "08b") for character in text_codificat])
        return valoare_binara

    # metoda de a ascunde/codifica datele binare criptate în imagine
    # Aceasta este metoda principală prin care pixelii imaginii sunt modificați pentru a insera mesajul nostru ascuns
    def codif_in_imagine(self):
        try:
            # citirea imaginii în modul numai citire din calea furnizată
            imagine_coperta = Image.open(self.cale_imagine, 'r')
            # dacă nu am ales imaginea din calea furnizată, următorul mesaj va fi afișat:
            if not imagine_coperta:
                messagebox.showerror("Eroare","Nu ați selectat nimic!")
            # obținerea dimensiunii imaginii, necesară atunci când exportați imaginea codificată în sfârșit
            # returnează un tuplu cu lățime și înălțime
            lungime, inaltime = imagine_coperta.size
            # luând în considerare tipul de imagine ca RGB și setând valoarea canalelor la 3
            c = 3
            # conversia imaginii încărcate într-o matrice numpy pentru a manipula pixelii
            # metoda getdata() din PIL returnează un obiect imagine iterabil
            # metoda list convertește obiectul de pixeli ai imaginii iterabile într-o listă
            # lista returnată este convertită în matrice numpy
            matrice_imagine = np.array(list(imagine_coperta.getdata()))
            # obținerea dimensiunii imaginii sau a numărului total al tuturor canalelor din imagine
            # efectuând împărțirea floor pentru a obține numărul total de pixeli din imagine
            marime_imagine = matrice_imagine.size // c
            # obținerea datelor binare pentru a fi codificate
            valoare_binara = self.text_binar()
            # generarea unei valori hash de 5 cifre pentru a identifica pixelul de la care începe codificarea
            val_h = str(int(hashlib.md5(self.parola.encode('utf-8')).hexdigest(), 16))[:5]       
            # verifică dacă numărul hash generat depășește numărul de pixeli din imagine
            # dacă da, eliminăm numărul hash generat cu o cifră și verificăm din nou
            if int(val_h) > marime_imagine:
                val_h = val_h[:4]
                if int(val_h) > marime_imagine:
                    val_h = val_h[:3]
                    if int(val_h) > marime_imagine:
                        val_h = val_h[:2]
                        if int(val_h) > marime_imagine:
                            val_h = val_h[:1]
                            if int(val_h) > marime_imagine:
                                return ['Mărimea imaginii nu este suficientă pentru codificarea textului dat.', False]
            # obținerea dimensiunii datelor binare de codificat
            marime_text = len(valoare_binara)
            # obținerea spațiului total disponibil pentru codificare după ce poziția este definită prin hash
            spatiu_codif = marime_imagine - int(val_h)
            # dacă spațiul de codificare nu este suficient pentru a codifica imaginea,
            # definirea unui boolean pentru a indica faptul că codificarea trebuie continuată de la pixelul de pornire
            pixel_start = False
            if marime_text > spatiu_codif:
                pixel_start = True
            # verifică dacă dimensiunea imaginii este suficientă pentru a codifica textul dat
            if marime_text > matrice_imagine.size:
                return ['Mărimea imaginii nu este suficientă pentru codificarea textului dat.', False]
            else:
                # setarea unei variabile locale pentru a indica valoarea binară de codificat în fiecare iterație
                index_binar = 0
                # buclă peste fiecare pixel al imaginii
                for pix in range(int(val_h), marime_imagine):
                    # buclă peste fiecare canal al unui singur pixel al imaginii
                    for canal in range(0, c):
                        # urmărire index binar pentru a verifica dacă depășește dimensiunea
                        if index_binar < marime_text:
                            # modificarea bitului cel mai puțin semnificativ (Least Significant Bit, LSB) al canalului sau
                            # înlocuirea ultimei valori binare a canalului selectat
                            # cu valoarea indexului binar selectat
                            # funcția bin() convertește valoarea întreagă a canalului selectat în binar
                            # felierea [2:9] extrage toți biții lăsând LSB și „0b” la început
                            # LSB este atașat din valoarea binară a textului
                            # funcția int() convertește valoarea binară (baza 2) înapoi în întreg
                            matrice_imagine[pix, canal] = int(bin(matrice_imagine[pix][canal])[2:9] +
                                                              valoare_binara[index_binar], 2)
                            # creșterea valorii index_binar pentru a indica următoarea valoare de codificat
                            index_binar += 1

                # Codificarea biților din stânga datelor de la început
                if pixel_start:
                    # buclă peste fiecare pixel al imaginii de la început
                    for pix in range(int(val_h)):
                        for canal in range(0, c):
                            if index_binar < marime_text:
                                matrice_imagine[pix, canal] = int(bin(matrice_imagine[pix][canal])[2:9] +
                                                                  valoare_binara[index_binar], 2)
                                index_binar += 1
                # remodelarea matricei imaginii în dimensiunile originale ale imaginii
                matrice_imagine = matrice_imagine.reshape(inaltime, lungime, c)
                # convertirea matricei de imagini modificate înapoi în imagine vizuală folosind funcția PIL fromarray
                # funcția numpy astype definește tipul de date în care să fie returnat -
                # care este un întreg nealocat de 8 biți, cuprins între 0-255 (uint8) în acest caz
                imagine_stego = Image.fromarray(matrice_imagine.astype('uint8'), imagine_coperta.mode)
                # returnarea imaginii codificate cu valoarea de stare booleană
                return [imagine_stego, True]
        except Exception:
            return ['Eroare de nerecunoscut. Motivele posibile ar putea fi:\n'
                    '1. Fișier imagine nerecunoscut\n'
                    '2. Caractere de text inacceptabile', False]

    # metodă pentru a verifica toate valorile furnizate și a transmite mesajele de eroare în consecință
    # returnează starea și mesajul pentru verificarea validității
    def valori_valide(self):
        # apelarea metodelor de mai sus una câte una pentru a verifica dacă parola, calea imaginii și textul dat sunt existente
        if not self.imagine_verificat():
            return ["Imaginea trebuie să existe!", False]
        elif not self.text_verificat():
            return ["Textul de codficat nu poate fi gol.", False]
        elif not self.parola_verificata():
            return ["Parola nu poate fi vidă.", False]
        else:
            return ["Verificat", True]