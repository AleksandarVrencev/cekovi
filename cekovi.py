from tkinter import *
from tkinter import messagebox
from datetime import *
from dateutil.relativedelta import relativedelta
from db_cekovi import Database
# import DateEntry
from tkcalendar import DateEntry
import re # regular expressions
cekovi = Tk()
cekovi.title("Čekovi")
cekovi.geometry("820x500")
cekovi.resizable(True, True)
# read database
db_cekovi = Database("cekovi.db")
Label(cekovi, text=" " * 45).grid(row=0, column=4, sticky=W, columnspan=3)
# counter for listbox
item_counter = 1
# make a function regex for the entry fields
def regex():
    # make a list of entry fields
    entry_list = [sifra_entry, ime_entry, prezime_entry, ukupan_iznos_entry, uplaceno_entry, broj_cekova_entry, datum_prvi_cek_entry, maros_mix_entry, fishing_world_entry, cek1_entry, cek2_entry, cek3_entry, cek4_entry, cek5_entry, cek6_entry]
    # make a list of regex
    regex_list = ["^[a-zA-Z0-9\s\.\-\_\/]*$", "^[a-zA-Z]*$", "^[a-zA-Z]*$", "^[0-9]*$", "^[0-9]*$", "^[1-6]*$", "^[0-9]{2}.[0-9]{2}.[0-9]{4}$", "^[0-9]*$", "^[0-9]*$", "^[0-9]*$", "^[0-9]*$", "^[0-9]*$", "^[0-9]*$", "^[0-9]*$", "^[0-9]*$"]
    # make a regex for sifra entry field that allows special characters and spaces and numbers and letters
    #regex_list[0] = "^[a-zA-Z0-9\s\.\-\_]*$"
    # make a list of error messages
    error_list = ["Šifra može sadržati samo slova, brojeve i znake '.', '/', '-', '_'!", "Ime može sadržati samo slova!", "Prezime može sadržati samo slova!", "Ukupan iznos može sadržati samo pozitivne brojeve!", "Uplaćeno može sadržati samo pozitivne brojeve!", "Broj čekova može sadržati samo brojeve između 1 i 6!", \
                    "Datum mora biti u formatu dd.mm.yyyy!", "Maros Mix može sadržati samo pozitivne brojeve!", "Fishing World može sadržati samo pozitivne brojeve!", "Ček 1 može sadržati samo pozitivne brojeve!", "Ček 2 može sadržati samo pozitivne brojeve!", "Ček 3 može sadržati samo pozitivne brojeve!", \
                    "Ček 4 može sadržati samo pozitivne brojeve!", "Ček 5 može sadržati samo pozitivne brojeve!", "Ček 6 može sadržati samo pozitivne brojeve!"]
    # make a loop to check if the entry field is empty
    for i in range(len(entry_list)):
        if entry_list[i].get() == "":
            messagebox.showerror("Čekovi", "Popunite prazna polja za unos podataka!")
            entry_list[i].focus()
            return False
        # make a loop to check if the entry field is valid
        elif not re.match(regex_list[i], entry_list[i].get()):
            messagebox.showerror("Čekovi", error_list[i])
            entry_list[i].focus()
            return False
        # check if sum of cekovi and uplaceno is equal to ukupan iznos
        elif int(ukupan_iznos_entry.get()) != int(uplaceno_entry.get()) + int(cek1_entry.get()) + int(cek2_entry.get()) + int(cek3_entry.get()) + int(cek4_entry.get()) + int(cek5_entry.get()) + int(cek6_entry.get()):
            messagebox.showerror("Čekovi", "Zbir polja 'uplaćeno' i čekova mora biti jednak ukupnom iznosu!")
            ukupan_iznos_entry.focus()
            return False
        # check if sum of maros mix and fishing world is equal or less than ukupan iznos
        elif int(ukupan_iznos_entry.get()) < int(maros_mix_entry.get()) + int(fishing_world_entry.get()):
            messagebox.showerror("Čekovi", "Zbir polja 'Maros Mix' i 'Fishing World' mora biti manji ili jednak ukupnom iznosu!")
            ukupan_iznos_entry.focus()
            return False
    # make a list of cek entry fields
    cek_entry_list = [cek1_entry.get(), cek2_entry.get(), cek3_entry.get(), cek4_entry.get(), cek5_entry.get(), cek6_entry.get()]
    for i in range(int(broj_cekova_entry.get())):
        if int(cek_entry_list[i]) == 0:
            messagebox.showerror("Čekovi", "Izabrali ste " + broj_cekova_entry.get() + " čeka\n Svaki od izabranih čekova mora imati vrednost veću od 0!")
            return False 
    return True

# make a function ucitaj to make a label and entry in range of broj_cekova
def ucitaj(*args):
    # date format for users
    datum = datetime.strptime(datum_prvi_cek_text.get(), "%d.%m.%Y").strftime("%d.%m.%Y")
    # date format for database
    datum_db = datetime.strptime(datum_prvi_cek_text.get(), "%d.%m.%Y")
    for i in range(6):
        Label(cekovi, text=" " * 18).grid(row=i, column=4, sticky=W)
        Label(cekovi, text=" " * 10).grid(row=i, column=5, sticky=W)
        Label(cekovi, text=" " * 10).grid(row=i, column=6, sticky=W)

    for i in range(int(broj_cekova_text.get())):
        # increment datum for one month
        datum = (datum_db + relativedelta(months=+i)).strftime("%d.%m.%Y")
        # store cek entry values in a list
        cek_list = [cek1_entry.get(), cek2_entry.get(), cek3_entry.get(), cek4_entry.get(), cek5_entry.get(), cek6_entry.get()]
        # count 60% of maros mix divided by broj_cekova
        maros_mix_cek = int(maros_mix_entry.get()) * 0.6 / int(broj_cekova_entry.get())
        # count 60% of fishing world divided by broj_cekova
        fishing_world_cek = int(fishing_world_entry.get()) * 0.6 / int(broj_cekova_entry.get())
        # make label red if date is in the future and green if date is in the past
        if datetime.strptime(datum, "%d.%m.%Y") > datetime.now():
            Label(cekovi, text=datum, fg="red").grid(row=i, column=4, sticky=W)
            # count 60% of every cek and add it to label
            if maros_mix_cek > 0:
                Label(cekovi, text=maros_mix_cek, fg="blue").grid(row=i, column=5, sticky=W)
            if fishing_world_cek > 0:
                Label(cekovi, text=fishing_world_cek, fg="orange").grid(row=i, column=6, sticky=W)
        else:
            Label(cekovi, text=datum, fg="green").grid(row=i, column=4, sticky=W)
            if maros_mix_cek > 0:
                Label(cekovi, text=maros_mix_cek, fg="blue").grid(row=i, column=5, sticky=W)
            if fishing_world_cek > 0:
                Label(cekovi, text=fishing_world_cek, fg="orange").grid(row=i, column=6, sticky=W)
    for i in range(int(broj_cekova_text.get()), 7):
        Label(cekovi, text=" " * 18).grid(row=i, column=4, sticky=W)
        Label(cekovi, text=" " * 10).grid(row=i, column=5, sticky=W)
        Label(cekovi, text=" " * 10).grid(row=i, column=6, sticky=W)

def dodaj():
    # add regex check
    if regex():
        # add data to database
        db_cekovi.insert(sifra_text.get(), ime_text.get(), 
        prezime_text.get(), ukupan_iznos_text.get(), uplaceno_text.get(), 
        broj_cekova_text.get(), datum_prvi_cek_text.get(), maros_mix_text.get(), 
        fishing_world_text.get(), cek1_text.get(), cek2_text.get(), cek3_text.get(), 
        cek4_text.get(), cek5_text.get(), cek6_text.get())
        svi_podaci()
        ucitaj()
        messagebox.showinfo("Čekovi", "Podatak je uspešno dodat u bazu podataka!")

def izmeni():
    # add regex check
    if regex():
        db_cekovi.update(selected_item[0], sifra_text.get(), ime_text.get(),
        prezime_text.get(), ukupan_iznos_text.get(), uplaceno_text.get(),
        broj_cekova_text.get(), datum_prvi_cek_text.get(), maros_mix_text.get(),
        fishing_world_text.get(), cek1_text.get(), cek2_text.get(), cek3_text.get(),
        cek4_text.get(), cek5_text.get(), cek6_text.get())
        svi_podaci()
        ucitaj()
        messagebox.showinfo("Čekovi", "Podaci izabranog korisnika uspešno izmenjeni!")

def obrisi():
    # check if there is a selected item
    if len(listbox.curselection()) > 0:
        # ask for confirmation
        answer = messagebox.askquestion("Čekovi", "Da li ste sigurni da želite da obrišete izabranog korisnika?")
        if answer == "yes":
            db_cekovi.remove(selected_item[0])
            svi_podaci()
            messagebox.showinfo("Čekovi", "Korisnik uspešno obrisan!")
            clear(False)
    else:
        messagebox.showerror("Čekovi", "Niste izabrali korisnika!")

def svi_podaci():
    global item_counter
    item_counter = 1
    listbox.delete(0, END)
    for row in db_cekovi.fetch():
        listbox.insert(END, str(item_counter) + ". " + row[2] + " " + row[3])
        item_counter += 1

def clear(bool = True):
    sifra_entry.delete(0, END)
    ime_entry.delete(0, END)
    prezime_entry.delete(0, END)
    ukupan_iznos_entry.delete(0, END)
    uplaceno_entry.delete(0, END)
    broj_cekova_entry.delete(0, END)
    datum_prvi_cek_entry.delete(0, END)
    maros_mix_entry.delete(0, END)
    fishing_world_entry.delete(0, END)
    cek1_entry.delete(0, END)
    cek2_entry.delete(0, END)
    cek3_entry.delete(0, END)
    cek4_entry.delete(0, END)
    cek5_entry.delete(0, END)
    cek6_entry.delete(0, END)
    if bool:
        messagebox.showinfo("Čekovi", "Sva polja su obrisana!")

def select_item(event):
    try:
        global selected_item
        index = listbox.curselection()[0]
        lista = []
        for row in db_cekovi.fetch():
            lista.append(row)
        selected_item = lista[index]
        sifra_entry.delete(0, END)
        sifra_entry.insert(END, selected_item[1])
        ime_entry.delete(0, END)
        ime_entry.insert(END, selected_item[2])
        prezime_entry.delete(0, END)
        prezime_entry.insert(END, selected_item[3])
        ukupan_iznos_entry.delete(0, END)
        ukupan_iznos_entry.insert(END, selected_item[4])
        uplaceno_entry.delete(0, END)
        uplaceno_entry.insert(END, selected_item[5])
        broj_cekova_entry.delete(0, END)
        broj_cekova_entry.insert(END, selected_item[6])
        datum_prvi_cek_entry.delete(0, END)
        datum_prvi_cek_entry.insert(END, selected_item[7])
        maros_mix_entry.delete(0, END)
        maros_mix_entry.insert(END, selected_item[8])
        fishing_world_entry.delete(0, END)
        fishing_world_entry.insert(END, selected_item[9])
        cek1_entry.delete(0, END)
        cek1_entry.insert(END, selected_item[10])
        cek2_entry.delete(0, END)
        cek2_entry.insert(END, selected_item[11])
        cek3_entry.delete(0, END)
        cek3_entry.insert(END, selected_item[12])
        cek4_entry.delete(0, END)
        cek4_entry.insert(END, selected_item[13])
        cek5_entry.delete(0, END)
        cek5_entry.insert(END, selected_item[14])
        cek6_entry.delete(0, END)
        cek6_entry.insert(END, selected_item[15])
        ucitaj()
        return True
    except IndexError:
        pass

# make a label and entry for the sifra, ime, prezime, ukupan_iznos, uplaceno, broj_cekova, datum_prvi_cek, maros_mix, fishing_world
sifra_label = Label(cekovi, text="Šifra")
sifra_label.grid(row=0, column=0, padx=10, pady=10)
sifra_text = StringVar()
sifra_entry = Entry(cekovi, textvariable=sifra_text)
sifra_entry.grid(row=0, column=1, padx=10, pady=10)

ime_label = Label(cekovi, text="Ime")
ime_label.grid(row=1, column=0, padx=10, pady=10)
ime_text = StringVar()
ime_entry = Entry(cekovi, textvariable=ime_text)
ime_entry.grid(row=1, column=1, padx=10, pady=10)

prezime_label = Label(cekovi, text="Prezime")
prezime_label.grid(row=2, column=0, padx=10, pady=10)
prezime_text = StringVar()
prezime_entry = Entry(cekovi, textvariable=prezime_text)
prezime_entry.grid(row=2, column=1, padx=10, pady=10)

ukupan_iznos_label = Label(cekovi, text="Ukupan iznos")
ukupan_iznos_label.grid(row=3, column=0, padx=10, pady=10)
ukupan_iznos_text = IntVar()
ukupan_iznos_entry = Entry(cekovi, textvariable=ukupan_iznos_text)
ukupan_iznos_entry.grid(row=3, column=1, padx=10, pady=10)

uplaceno_label = Label(cekovi, text="Uplaćeno")
uplaceno_label.grid(row=4, column=0, padx=10, pady=10)
uplaceno_text = IntVar()
uplaceno_entry = Entry(cekovi, textvariable=uplaceno_text)
uplaceno_entry.grid(row=4, column=1, padx=10, pady=10)

broj_cekova_label = Label(cekovi, text="Broj čekova")
broj_cekova_label.grid(row=5, column=0, padx=10, pady=10)
broj_cekova_text = IntVar()
broj_cekova_entry = Entry(cekovi, textvariable=broj_cekova_text)
broj_cekova_entry.grid(row=5, column=1, padx=10, pady=10)

# make a date entry
datum_prvi_cek_label = Label(cekovi, text="Datum za prvi ček")
datum_prvi_cek_label.grid(row=6, column=0, padx=10, pady=10)
datum_prvi_cek_text = StringVar()
datum_prvi_cek_entry = DateEntry(cekovi, textvariable=datum_prvi_cek_text, width=12, background='darkblue', foreground='white', borderwidth=2)
# start function ucitaj when date is selected
datum_prvi_cek_entry.bind("<<DateEntrySelected>>", ucitaj)
datum_prvi_cek_entry.grid(row=6, column=1, padx=10, pady=10)
# format the date entry to dd/mm/yyyy
datum_prvi_cek_entry.configure(date_pattern='dd.mm.yyyy')
maros_mix_label = Label(cekovi, text="Maroš Mix")
maros_mix_label.grid(row=7, column=0, padx=10, pady=10)
maros_mix_label.config(fg="blue")
maros_mix_text = IntVar()
maros_mix_entry = Entry(cekovi, textvariable=maros_mix_text)
maros_mix_entry.grid(row=7, column=1, padx=10, pady=10)

fishing_world_label = Label(cekovi, text="Fishing World")
fishing_world_label.grid(row=8, column=0, padx=10, pady=10)
fishing_world_label.config(fg="orange")
fishing_world_text = IntVar()
fishing_world_entry = Entry(cekovi, textvariable=fishing_world_text)
fishing_world_entry.grid(row=8, column=1, padx=10, pady=10)

# add six labels and entries for the cekovi
cek1_label = Label(cekovi, text="Ček 1.")
cek1_label.grid(row=0, column=2)
cek1_text = IntVar()
cek1_entry = Entry(cekovi, textvariable=cek1_text)
cek1_entry.grid(row=0, column=3)

cek2_label = Label(cekovi, text="Ček 2.")
cek2_label.grid(row=1, column=2)
cek2_text = IntVar()
cek2_entry = Entry(cekovi, textvariable=cek2_text)
cek2_entry.grid(row=1, column=3)

cek3_label = Label(cekovi, text="Ček 3.")
cek3_label.grid(row=2, column=2)
cek3_text = IntVar()
cek3_entry = Entry(cekovi, textvariable=cek3_text)
cek3_entry.grid(row=2, column=3)

cek4_label = Label(cekovi, text="Ček 4.")
cek4_label.grid(row=3, column=2)
cek4_text = IntVar()
cek4_entry = Entry(cekovi, textvariable=cek4_text)
cek4_entry.grid(row=3, column=3)

cek5_label = Label(cekovi, text="Ček 5.")
cek5_label.grid(row=4, column=2)
cek5_text = IntVar()
cek5_entry = Entry(cekovi, textvariable=cek5_text)
cek5_entry.grid(row=4, column=3)

cek6_label = Label(cekovi, text="Ček 6.")
cek6_label.grid(row=5, column=2)
cek6_text = IntVar()
cek6_entry = Entry(cekovi, textvariable=cek6_text)
cek6_entry.grid(row=5, column=3)

# add listbox and scrollbar to the right side of the window 
listbox = Listbox(cekovi, height=8, width=35)
listbox.grid(row=0, column=7, rowspan=9, columnspan=2, padx=5, pady=10, sticky=N+S+E+W)
scrollbar = Scrollbar(cekovi)
scrollbar.grid(row=0, column=9, rowspan=9, sticky=N+S)
# connect listbox to scrollbar
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)
listbox.bind('<<ListboxSelect>>', select_item)
# add file menu to the menu bar with commands same as buttons
file_menu = Menu(cekovi, tearoff=0)
cekovi.config(menu=file_menu)
file_menu.add_command(label="Dodaj korisnika", command=dodaj)
file_menu.add_command(label="Izmeni korisnika", command=izmeni)
file_menu.add_command(label="Obriši korisnika", command=obrisi)
file_menu.add_command(label="Očisti polja za unos", command=clear)

svi_podaci()
cekovi.mainloop()