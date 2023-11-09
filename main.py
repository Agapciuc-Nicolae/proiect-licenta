# Se importă bibliotecile necesare
import os.path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import codificare
import decodificare

# Definirea variabilelor globale pentru a urmări dacă trei ferestre copil -
# de codificare, decodificare și fereastră de ajutor sunt în stare deschisă sau închisă
codif_deschis = False
decodif_deschis = False
ajutor_deschis = False
# Definirea unei variabile cale_fișier pentru a stoca calea imaginii selectate
cale_fisier = ""

# Componenta ferestrei codificare
# pentru a deschide o nouă fereastră al funcționalității de codificare
def deschide_codif_fereastra():
    # referire la variabila globală pentru a reflecta modificarea la nivel global
    global codif_deschis
    # verifică dacă fereastra este deja deschisă
    if not codif_deschis:
        # Inițializarea unei noi ferestre copil pentru funcțiile de codificare
        codif_fereastra = Toplevel(fereastra)
        # Setarea titlului ferestrei de codificare
        codif_fereastra.title("Stegno - Codificare")
        # Setarea dimensiunii și poziționarea ferestrei de codificare
        codif_fereastra.geometry('800x500+100+400')
        # Setarea proprietății redimensionabile a ferestrei de codificare la false
        codif_fereastra.resizable(False, False)
        # Setarea ferestrei ca un copil al părintelui astfel încât să apară în față
        codif_fereastra.transient(fereastra)

        # Canvas pentru a afișa imaginea după ce imaginea este selectată din fereastra fișierului
        canvas_imagine_originala = Label(codif_fereastra, text="", height=20, width=50, relief="raised",
                                bg="#FFFFFF")
            
        # Plasarea static a canvasului pe fereastră
        canvas_imagine_originala.place(x=400, y=20)

        # Etichetă pentru a indica zona de text de introducere a textului de codificat
        eticheta_mesaj_de_codif = Label(codif_fereastra, text="Mesaj de codificat")
        eticheta_mesaj_de_codif.config(font=("Times New Roman", 12))
        eticheta_mesaj_de_codif.place(x=20, y=20)

        # Zona de text pentru a introduce textul de codificat
        mesaj_de_codif = Text(codif_fereastra, height=7, width=34)
        mesaj_de_codif.config(relief="raised", font=("Times New Roman", 15))
        mesaj_de_codif.place(x=20, y=51)

        # Etichetă pentru a indica câmpul de text la de introducere a parolei de codificare
        parola_de_codif_eticheta = Label(codif_fereastra, text="Parola")
        parola_de_codif_eticheta.config(font=("Times New Roman", 12))
        parola_de_codif_eticheta.place(x=20, y=262)
            
        # Câmp text pentru a introduce parola la codificare
        parola_de_codif = Entry(codif_fereastra, width=34)
        parola_de_codif.config(relief="raised", font=("Times New Roman", 15), show="•")
        parola_de_codif.place(x=20, y=293)

        #Valoare pentru afișarea parolei la operația de codificare
        c_v1=IntVar(value=0)
        #Funcție pentru afișarea parolei la operația de codificare
        def afis_parola_codif():
            if (c_v1.get()==1):
                parola_de_codif.config(show='')
            else:
                parola_de_codif.config(show='•')

        #Căsuță de marcat de afișare a parolei pentru codificare
        afisare_par_cod = Checkbutton(codif_fereastra, text='afișare parola codificare', variable=c_v1, onvalue=1, offvalue=0, command=afis_parola_codif)
        afisare_par_cod.config(font=("Times New Roman", 15))
        afisare_par_cod.place(x=20, y=333)

        # Buton de căutare imagine brută pentru a codifica textul din interiorul acesteia
        # Apelează o funcție rasfoire_imagine() cu eticheta pentru a afișa imaginea ca argument
        buton_rasfoire_imagine = Button(codif_fereastra, text="Selectați o imagine in care vreți să ascundeți mesajul", width=38,
                            command=lambda: rasfoire_imagine(canvas_imagine_originala))
        buton_rasfoire_imagine.config(font=("Times New Roman", 12), bg="#FFFFFF", fg="black", borderwidth=2)
        buton_rasfoire_imagine.place(x=400, y=350)

        # Buton pentru codificarea textului din interiorul imaginii și validarea câmpului de parolă
        # Apelează o funcție pe o clasă de codificare separată
        buton_codif_imagine = Button(codif_fereastra, text="Codificare", width=15,
                            command=lambda: codif_imagine(cale_fisier, parola_de_codif.get(),mesaj_de_codif.get("1.0", END)))
        buton_codif_imagine.config(font=("Times New Roman", 15), bg="#FFFFFF", fg="black", borderwidth=2)
        buton_codif_imagine.place(x=592, y=420)

        # Buton pentru anularea/ieșirea operației de codificare
        buton_inapoi1 = Button(codif_fereastra, text="Anulare", width=15,
                            command=codif_fereastra.destroy)
        buton_inapoi1.config(font=("Times New Roman", 15), bg="#FFFFFF", fg="black", borderwidth=2)
        buton_inapoi1.place(x=102, y=420)
        
        # Setarea stării codif_deschis ca True pentru a indica faptul că fereastra de codificare este deschisă
        codif_deschis = True
        # atribuirea unui manipulator pentru a defini acțiunile atunci când fereastra este încercată să fie închisă
        codif_fereastra.protocol("WM_DELETE_WINDOW",lambda: inchide_codif_fereastra(codif_fereastra))

# metodă pentru a salva fișierul imagine codificat pe o destinație aleasă
def salvare_imagine(imagine_schimbata):
    # obținerea căii destinației de salvat
    cale_salvare = filedialog.asksaveasfile(initialfile="placeholder.png", mode="wb", defaultextension=".png",
                                         filetypes=(("Image File", "*.png"), ("All Files", "*.*")))
    #Afișare eroare dacă utilizatorul anulează calea destinației de salvat
    if not cale_salvare:
        messagebox.showerror("Eroare","Nu ați selectat nimic!")
    # salvarea imaginii
    imagine_schimbata.save(cale_salvare)

# Funcție pentru a apela clasa de codificare de gestionare a codificării
# preia calea imaginii brute, a parolei și a textului pentru a fi codificate ca argumente
def codif_imagine(cale_imagine, parola, mesaj_de_codif):
    # apelarea constructorului clasei Codificare
    act_codif = codificare.Codificare(cale_imagine, parola, mesaj_de_codif)
    # funcția de apelare în clasa Codificare pentru a verifica dacă toate valorile sunt valide
    mesaj = act_codif.valori_valide()
    # verificarea mesajului de stare returnat de funcția de mai sus
    if not mesaj[1]:
        # afișează eroare dacă valorile furnizate sunt nevalide
        messagebox.showerror("Eroare în codificare", mesaj[0])
    else:
        # apelarea unei funcții din clasa Codificare pentru a codifica datele în imagine dacă toate valorile sunt valide
        imagine_schimbata = act_codif.codif_in_imagine()
        # verificarea mesajului de stare returnat din funcția de mai sus
        if imagine_schimbata[1]:
            # apelând funcția salvare_imagine() pentru a afișa dialogul de salvare a imaginii și a salva imaginea de ieșire
            if salvare_imagine(imagine_schimbata[0]) is None:
                messagebox.showinfo("Imagine salvată", "Operația de codificare a avut succes.")
        else:
            # Afișează eroarea dacă apare vreo eroare la codificarea imaginii
            messagebox.showerror("Eroare în codificare", imagine_schimbata[0])

# Componenta ferestrei decodificare
# de deschidere a noii ferestre pentru funcționalitatea de decodificare
def deschide_decodif_fereastra():
    # referire la variabila globală pentru a reflecta modificarea la nivel global
    global decodif_deschis
    if not decodif_deschis:
        # Inițializarea unei noi ferestre copil pentru funcțiile de decodificare
        decodif_fereastra = Toplevel(fereastra)
        # Setarea titlului ferestrei de decodificare
        decodif_fereastra.title("Stegno - Decodificare")
        # Setarea dimensiunii si poziționarea ferestrei de decodificare
        decodif_fereastra.geometry('800x500+900+400')
        # Setarea proprietății redimensionabile a ferestrei de codificare la false
        decodif_fereastra.resizable(False, False)
        # Setarea ferestrei ca un copil al părintelui astfel încât să apară în față
        decodif_fereastra.transient(fereastra)
        # Canvas pentru a afișa imaginea după ce imaginea este selectată din fereastra fișierului
        canvas_imagine_schimbata = Label(decodif_fereastra, text="", height=20, width=50, relief="raised",
                                bg="#FFFFFF")
        # Plasarea static a canvasului pe fereastră
        canvas_imagine_schimbata.place(x=400, y=20)

        # Etichetă pentru a indica zona de text de introducere a textului de decodificat
        eticheta_mesaj_de_decodif = Label(decodif_fereastra, text="Mesaj de decodificat")
        eticheta_mesaj_de_decodif.config(font=("Times New Roman", 12))
        eticheta_mesaj_de_decodif.place(x=20, y=20)

        # Zona de text pentru a introduce textul de decodificat
        mesaj_de_decodif = Text(decodif_fereastra, height=7, width=34)
        mesaj_de_decodif.config(relief="raised", font=("Times New Roman", 15), state=DISABLED)
        mesaj_de_decodif.place(x=20, y=51)

        # Etichetă pentru a indica câmpul de text de introducere a parolei la decodificare
        eticheta_parola_de_decodif = Label(decodif_fereastra, text="Parola")
        eticheta_parola_de_decodif.config(font=("Times New Roman", 12))
        eticheta_parola_de_decodif.place(x=20, y=262)

        # Câmp text pentru a introduce parola la decodificare
        parola_de_decodif = Entry(decodif_fereastra, width=34)
        parola_de_decodif.config(relief="raised", font=("Times New Roman", 15), show="•")
        parola_de_decodif.place(x=20, y=293)

        #Valoare pentru afișarea parolei la operația de codificare
        c_v2=IntVar(value=0)
        #Funcție pentru afișarea parolei la operația de codificare
        def afis_parola_decodif():
            if (c_v2.get()==1):
                parola_de_decodif.config(show='')
            else:
                parola_de_decodif.config(show='•')

        #Căsuță de marcat pentru afișarea parolei la decodificare
        afisare_par_decod = Checkbutton(decodif_fereastra, text='afișare parolă decodificare', variable=c_v2, onvalue=1, offvalue=0, command=afis_parola_decodif)
        afisare_par_decod.config(font=("Times New Roman", 15))
        afisare_par_decod.place(x=20, y=333)

        # Buton de căutare imaginea codificată (sau stego-imaginea) pentru a decodifica
        # Apelează o funcție rasfoire_imagine() cu eticheta pentru a afișa imaginea ca argument
        buton_rasfoire_imagine_stego = Button(decodif_fereastra, text="Selectați o stego-imagine", width=35,command=lambda: rasfoire_imagine(canvas_imagine_schimbata))
        buton_rasfoire_imagine_stego.config(font=("Times New Roman", 14), bg="#000000", fg="white", borderwidth=2)
        buton_rasfoire_imagine_stego.place(x=400, y=350)

        # Buton pentru decodificarea imaginii și validarea câmpului de parolă
        # Apelează o funcție pe o clasă de decodificare separată
        buton_imagine_decodif = Button(decodif_fereastra, text="Decodificare", width=15,
                                command=lambda: decodif_imagine(cale_fisier, parola_de_decodif.get(), mesaj_de_decodif))
        buton_imagine_decodif.config(font=("Times New Roman", 15), bg="#000000", fg="white", borderwidth=2)
        buton_imagine_decodif.place(x=592, y=420)

        # Buton pentru anularea/ieșirea operației de decodificare
        buton_inapoi2 = Button(decodif_fereastra, text="Anulare", width=15,
                                command=decodif_fereastra.destroy)
        buton_inapoi2.config(font=("Times New Roman", 15), bg="#000000", fg="white", borderwidth=2)
        buton_inapoi2.place(x=102, y=420)

        # Setarea stării decodif_deschis ca True pentru a indica faptul că fereastra de decodificare este deschisă
        decodif_deschis = True
        # atribuirea unui manipulator pentru a defini acțiunile atunci când fereastra este încercată să fie închisă
        decodif_fereastra.protocol("WM_DELETE_WINDOW",lambda: inchide_decodif_fereastra(decodif_fereastra))

# Funcție de apelare a clasei Decodificare pentru a gestiona decodificarea
# preia calea stego-imaginii, a parolei și a câmpului de text pentru a afișa textul decodificat ca argumente
def decodif_imagine(cale_imagine, parola, zona_text):
    # apelarea constructorului clasei Decodificare
    act_decodif = decodificare.Decodificare(cale_imagine, parola)
    # apelarea unei metode din clasa Decodificare pentru a verifica dacă toate argumentele furnizate sunt valide
    # returnează starea cu mesajul de stare
    mesaj = act_decodif.valori_valide()
    # verifică starea mesajului returnat
    if not mesaj[1]:
        # afișează un mesaj de eroare dacă valorile furnizate nu sunt valide
        messagebox.showerror("Eroare in decodificare", mesaj[0])
    else:
        # funcția de apelare în interiorul clasei Decodificare pentru a decodfifica textul din imagine
        # returnează text sau mesaj de eroare cu valoare booleană de stare
        text_decodificat = act_decodif.decodificat_din_imagine()
        # verificarea stării mesajului și dacă extragerea mesajului a reușit, afișarea în fereastră
        if text_decodificat[1]:
            # activarea widget-ului de text dezactivat în fereastra de decodificare
            zona_text.config(state=NORMAL)
            # ștergerea câmpului de text înainte de a introduce textul decodificat
            zona_text.delete(1.0, END)
            # introducerea textului decodificat
            zona_text.insert(1.0, text_decodificat[0])
            # re-dezactivarea widget-ului pentru a preveni inserarea accidentală
            zona_text.config(state=DISABLED)
            # afișează mesajul de succes
            messagebox.showinfo("Text decodificat", "Operația de decodificare a avut succes.")
        else:
            # afișează mesajul de eroare dacă apare vreo eroare în timpul procesului de decodificare
            messagebox.showerror("Eroare în decodificare", text_decodificat[0])

# Componente comune
# funcția de deschidere a ferestrei fișierului pentru a răsfoi imaginea care vor fi codificate sau decodificate
def rasfoire_imagine(rama_imagine):
    # Se face referire la variabila globală cale_fisier pentru a stoca calea fișierului
    global cale_fisier
    # Deschiderea casetei de dialog pentru fișiere ca să permită utilizatorului să aleagă un fișier imagine
    cale_fisier = filedialog.askopenfilename(title="Alegeți o imagine",
                                           filetypes=(("Image Files", "*.png"), ("All Files", "*.*")))
    # Daca utilizatorul nu alege fișierul imagine, sistemul va afisa urmatorul mesaj
    if not cale_fisier:
        messagebox.showerror("Eroare","Nu ați selectat nimic!")
    # Obținerea căii imaginii selectate
    imagine_selectata = Image.open(cale_fisier)
    # Setarea lățimii maxime a imaginii pentru a o afișa pe fereastră
    lungime_maxima = 350
    # Calcularea raportului de aspect pentru redimensionarea proporțională a imaginii
    raport_aspect = lungime_maxima / float(imagine_selectata.size[0])
    # Calcularea înălțimii proporționale pentru lățimea definită
    inaltime_maxima = int((float(imagine_selectata.size[1]) * float(raport_aspect)))
    # Redimensionarea imaginii cu înălțimea și lățimea calculate
    imagine_selectata = imagine_selectata.resize((lungime_maxima, inaltime_maxima), Image.ANTIALIAS)
    # convertirea formatului de imagine selectat într-o imagine compatibilă cu tkinter
    imagine_selectata = ImageTk.PhotoImage(imagine_selectata)
    # Setarea configurațiilor de canvas pentru a afișa imaginea pe ramă
    rama_imagine.config(image=imagine_selectata, height=304, width=354)
    rama_imagine.image = imagine_selectata

# funcția de a afișare a fereastrei de asitență când facem clic pe butonul de ajutor
def ajutor():
    # referire la variabila globală pentru a reflecta modificarea la nivel global
    global ajutor_deschis
    # verifică dacă fereastra este deja deschisă
    if not ajutor_deschis:
        # Se inițializează o nouă fereastră copil pentru opțiunea de ajutor
        ajutor_fereastra=Toplevel(fereastra)
        # Setarea titlului ferestrei de ajutor
        ajutor_fereastra.title("Ajutor")
        # Setarea dimensiunii ferestrei de ajutor
        ajutor_fereastra.geometry('600x500')
        # Setarea proprietății redimensionabile a ferestrei de ajutor la false
        ajutor_fereastra.resizable(False, False)
        # Setarea ferestrei ca un copil al părintelui astfel încât să apară în față
        ajutor_fereastra.transient(fereastra)
        # Etichetă pentru a indica zona de text de afișare a textului de ajutor
        text_ajutor = Label(ajutor_fereastra,
                                    text="Stegno este un instrument pentru steganografie pentru imagini "
                                          "folosit pentru a încorpora mesaje text într-o imagine. "
                                          "Textul încorporat este criptat folosind parola."
                                          "\n\nPentru a codifica mesajul într-o imagine, faceți clic pe 'Codificare'"
                                          " și selectați o imagine. Scrieți o parolă și un text de încorporat."
                                          " Apoi faceți clic pe 'Codificare' pentru a încorpora și a salva imaginea cu mesaj. "
                                          "\n\nPentru a decoda mesajul dintr-o imagine codificată, faceți clic pe 'Decodificare' și selectați"
                                          " imaginea codată, furnizați parola folosită pentru a decodifica și faceți clic pe 'Decodificare'."
                                          " Mesajul dvs. decodat va fi afișat pe fereastră. Dacă parola furnizată "
                                          "este incorectă, mesajul nu poate fi extras niciodată.")
        text_ajutor.config(font=("Times New Roman", 14),  justify="center", wraplength=500)
        text_ajutor.pack(padx=20, pady=20)

        # Buton pentru anularea/ieșirea ferestrei de ajutor
        buton_inapoi3 = Button(ajutor_fereastra, text="Ieșire", width=15,
                                command=ajutor_fereastra.destroy)
        buton_inapoi3.config(font=("Times New Roman", 15, "bold"), bg="#32a852", fg="white", borderwidth=2)
        buton_inapoi3.place(x=200, y=420)

        # Setarea stării ajutor_deschis ca True pentru a indica faptul că fereastra de ajutor este deschisă
        ajutor_deschis = True
        # atribuirea unui manipulator pentru a defini acțiunile atunci când fereastra este încercată să fie închisă
        ajutor_fereastra.protocol("WM_DELETE_WINDOW",lambda: inchide_ajutor_fereastra(ajutor_fereastra))

#Funcție de definire a acțiunilor care trebuie efectuate când fereastra de codare este încercată să fie închisă
def inchide_codif_fereastra(codif_fereastra):
    # referire la variabila globală pentru a reflecta modificarea la nivel global
    global codif_deschis
    # Distrugerea ferestrei copil de codificare trecute
    codif_fereastra.destroy()
    # Setarea valorii variabilei globale de urmărire la false pentru a indica faptul că fereastra este închisă
    codif_deschis = False

#Funcție de definire a acțiunilor care trebuie efectuate când fereastra de decodare este încercată să fie închisă
def inchide_decodif_fereastra(decodif_fereastra):
    # referire la variabila globală pentru a reflecta modificarea la nivel global
    global decodif_deschis
    # Distrugerea ferestrei copil de decodificare trecute
    decodif_fereastra.destroy()
    # Setarea valorii variabilei globale de urmărire la false pentru a indica faptul că fereastra este închisă
    decodif_deschis = False

#Funcție de definire a acțiunilor care trebuie efectuate când fereastra de ajutor este încercată să fie închisă
def inchide_ajutor_fereastra(ajutor_fereastra):
    # referire la variabila globală pentru a reflecta modificarea la nivel global
    global ajutor_deschis
    # Distrugerea ferestrei copil de ajutor trecute
    ajutor_fereastra.destroy()
    # Setarea valorii variabilei globale de urmărire la false pentru a indica faptul că fereastra este închisă
    ajutor_deschis = False

# Se inițializează fereastra tkinter
fereastra = Tk()
# Setarea titlului ferestrei
fereastra.title("Stegno")
# Setarea dimensiunii ferestrei si a poziției ei
fereastra.geometry('600x500+500+100')
# Setarea proprietății redimensionabile a ferestrei la false
fereastra.resizable(False, False)

# Inițializarea etichetei pentru a afișa eticheta titlului pe fereastră
titlu_eticheta = Label(fereastra, text="Stegno")
# Punerea etichetei pe fereastră
titlu_eticheta.pack()
# Setarea configurațiilor fonturilor pentru etichetă - familia de fonturi și dimensiunea fontului
titlu_eticheta.config(font=("Times New Roman", 32))

label2 = Label(fereastra, text='Bun venit la Stegno. Pentru a vedea cum funcționează aplicația, apăsați pe butonul "Ajutor", care se află lângă titlul aplicației.')
label2.pack()
label2.config(font=("Times New Roman", 15), wraplength=450)
label2.place(x=80,y=80)

# Buton de inițializare pentru acțiunea de codificare
buton_codif = Button(fereastra, text="Codificare", height=2, width=15, bg="#FFFFFF", fg="black", borderwidth=2,
                    command=deschide_codif_fereastra)
# Setarea configurațiilor de font pentru buton - familia de fonturi, dimensiunea și greutatea fontului
buton_codif.config(font=("Times New Roman", 15, "bold"))
# Punerea butonului pe fereastră
buton_codif.place(x=20, y=250)

# Buton de inițializare pentru acțiunea de decodificare
buton_decodif = Button(fereastra, text="Decodificare", height=2, width=15, bg="#000000", fg="white", borderwidth=2,
                    command=deschide_decodif_fereastra)
# Setarea configurațiilor de font pentru buton - familia de fonturi, dimensiunea și greutatea fontului
buton_decodif.config(font=("Times New Roman", 15, "bold"))
# Punerea butonului pe fereastră
buton_decodif.place(x=390, y=250)

# Buton de inițializare pentru acțiunea de ajutor
buton_ajutor = Button(fereastra, text="Ajutor", height=1, width=5, bg="#32a852", fg="white", borderwidth=2,
                    command=ajutor)
# Setarea configurațiilor de font pentru buton - familia de fonturi, dimensiunea și greutatea fontului
buton_ajutor.config(font=("Times New Roman", 15, "bold"))
# Punerea butonului pe fereastră
buton_ajutor.place(x=380, y=10)

buton_inapoi4 = Button(fereastra, text="Ieșire", height=2, width=15,
                                  command=fereastra.destroy)
buton_inapoi4.config(font=("Times New Roman", 15, "bold"), bg="#444444", fg="white", borderwidth=2)
buton_inapoi4.place(x=200, y=350)

fereastra.mainloop()