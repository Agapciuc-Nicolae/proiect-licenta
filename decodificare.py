import os.path
import numpy as np
import hashlib
from PIL import Image
from Crypto.Cipher import AES

# clasa Decodificare pentru a gestiona activitățile de codificare
class Decodificare:
    # Constructor parametrizat pentru a primi imaginea și parola de decodificat în timpul inițializării obiectului
    def __init__(self, cale_imagine, parola):
        self.cale_imagine = cale_imagine
        self.parola = parola.strip()

    # metodă pentru a verifica dacă imaginea există
    # returnează adevărat dacă imaginea este validă, altfel returnează fals
    def imagine_verificat(self):
        # verifică dacă imaginea există
        if os.path.exists(self.cale_imagine):
            return True
        return False

    # metodă pentru a verifica dacă parola furnizată există
    # returnează adevărat dacă parola există, altfel returnează fals
    def parola_verificata(self):
        # verificare daca parola este vidă
        if len(self.parola) == 0:
            return False
        return True

    def get_text_decodificat(self, string_octeti):
        # generarea unei chei hexadecimale de 32 de octeți din parola furnizată pentru a o utiliza ca cheie secretă AES
        cheia_secreta = hashlib.sha1(str(self.parola).encode()).hexdigest()[:32]
        # crearea unui nou obiect PyCrypto AES pentru a decodifica octeții convertiți
        cheie_decodificata = AES.new(cheia_secreta.encode('utf-8'), AES.MODE_EAX, cheia_secreta.encode())
        # conversia șirului de octeți extrași în octeți
        # funcția eval evaluează sau rulează operația de expresie python pentru șirul de octeți
        valoare_octeti = eval(string_octeti)
        # decodificarea și returnarea textului extras
        return cheie_decodificata.decrypt(valoare_octeti).decode('utf-8')

    # metoda de extragere a datelor binare codificate din imagine
    # aceasta este metoda principală de decodificare în care pixelii fiecărei imagini sunt analizați pentru a extrage date ascunse
    def decodificat_din_imagine(self):
        try:
            # citirea imaginii în modul numai citire din calea furnizată
            imagine_coperta = Image.open(self.cale_imagine, 'r')
            # dacă nu am ales imaginea din calea furnizată, următorul mesaj va fi afișat:
            if not imagine_coperta:
                messagebox.showerror("Eroare","Nu ați selectat nimic!")
            # luând în considerare tipul de imagine ca RGB în mod implicit și setând valoarea canalelor la 3
            c = 3
            # conversia imaginii încărcate într-o matrice numpy pentru a manipula pixelii
            # metoda getdata() din PIL returnează un obiect imagine iterabil
            # metoda list convertește obiectul de pixeli ai imaginii iterabile într-o listă
            # lista returnată este convertită în matrice numpy
            matrice_imagine = np.array(list(imagine_coperta.getdata()))
            # obținerea dimensiunii imaginii sau a numărului total al tuturor canalelor din imagine
            # efectuând împărțirea floor pentru a obține numărul total de pixeli din imagine
            marime_imagine = matrice_imagine.size // c
            # generarea unei valori hash de 5 cifre pentru a identifica pixelul de la care începe decodificarea
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
                                return ["Textul codificat nu a fost găsit. Motivele posibile ar putea fi:\n"
                                        "1. Parolă eronată\n"
                                        "2. Imagine greșită", False]
            # definirea unei variabile pentru a stoca valoarea binară extrasă
            valoare_binara = ""
            # buclă peste fiecare pixel al imaginii din numărul de pixeli generat de hash
            for pix in range(int(val_h), marime_imagine):
                # buclă peste fiecare canal într-un singur pixel al imaginii
                for canal in range(0, c):
                    # atașarea valorii LSB a fiecărui canal
                    valoare_binara += bin(matrice_imagine[pix][canal])[-1]

            # buclă peste fiecare pixel de la început în cazul în care se aplică pixelul de pornire
            for pix in range(int(val_h)):
                for canal in range(0, c):
                    valoare_binara += bin(matrice_imagine[pix][canal])[-1]

            # convertirea valorii binare extrase în listă de valori binare
            # unde fiecare element al listei conține un octet sau o valoare binară de 8 biți
            lista_binara = [valoare_binara[valoare:valoare + 8] for valoare in range(0, len(valoare_binara), 8)]
            # definirea unei variabile pentru a stoca textul decodificat din binar
            text_decodificat = ""  
            # buclă peste lista de valori binare pentru a extrage textul decodificat
            for i in range(len(lista_binara)):
                # verifică dacă textul decodificat conține valoarea delimitatorului
                # întreruperea buclei dacă se găsește valoarea
                if text_decodificat[-4:] == "$@&#":
                    break
                else:
                    # convertirea fiecărui octet al listei binare în text și adăugarea acestora
                    # funcția int convertește fiecare octet din listă în echivalentul său întreg
                    # funcția chr decodifică fiecare valoare întreagă în caracterul Unicode echivalent
                    text_decodificat += chr(int(lista_binara[i], 2))

            # Verificăm din nou dacă textul decodificat conține caractere delimitare și le luăm dacă sunt găsite
            if "$@&#" in text_decodificat:
                
                # luarea caracterelor delimitatoare și extragerea numai a textului codificat
                text_decodificat = text_decodificat[:-4]
                # funcția de apelare pentru a obține textul simplu decodificat din șirul de octeți decodificați
                try:
                    text_decodificat = self.get_text_decodificat(text_decodificat)
                    # returnează text simplu decodificat cu starea
                    return [text_decodificat, True]
                except UnicodeDecodeError:
                    # returnarea mesajului de eroare dacă textul nu este găsit
                    return ["Textul codificat nu a fost găsit. Motivele posibile ar putea fi:\n"
                                "1. Parolă eronată\n"
                                "2. Imagine greșită", False]
            else:
                # returnarea mesajului de eroare dacă textul nu este găsit
                return ["Textul codificat nu a fost găsit. Motivele posibile ar putea fi:\n"
                            "1. Parolă eronată\n"
                            "2. Imagine greșită", False]
        except Exception:
            # returnarea mesajului de eroare dacă textul nu este găsit
            return ["Textul codificat nu a fost găsit. Motivele posibile ar putea fi:\n"
                        "1. Parolă eronată\n"
                        "2. Imagine greșită", False]

    # metodă pentru a verifica toate valorile furnizate și a transmite mesajele de eroare în consecință
    # returnează starea și mesajul pentru verificarea validității
    def valori_valide(self):
        # apelarea metodelor de mai sus una câte una pentru a verifica dacă parola, calea imaginii și textul dat sunt existente
        if not self.imagine_verificat():
            return ["Imaginea trebuie să existe!", False]
        elif not self.parola_verificata():
            return ["Parola nu poate fi vidă.", False]
        else:
            return ["Verificat", True]