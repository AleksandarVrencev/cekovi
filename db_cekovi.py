import sqlite3
class Database:
    def __init__(self, db_cekovi):
        self.conn = sqlite3.connect(db_cekovi)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS cekovi (id INTEGER PRIMARY KEY, sifra text, ime text, prezime text, ukupan_iznos int, uplaceno int, broj_cekova int, datum_prvi_cek text, maros_mix int, fishing_world int, cek1 int, cek2 int, cek3 int, cek4 int, cek5 int, cek6 int)")
        self.conn.commit()

    def execute(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def fetch(self):
        self.cur.execute("SELECT * FROM cekovi")
        rows = self.cur.fetchall()
        return rows

    def insert(self, sifra, ime, prezime, ukupan_iznos, uplaceno, broj_cekova, datum_prvi_cek, maros_mix, fishing_world, cek1, cek2, cek3, cek4, cek5, cek6):
        self.cur.execute("INSERT INTO cekovi VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (sifra, ime, prezime, ukupan_iznos, uplaceno, broj_cekova, datum_prvi_cek, maros_mix, fishing_world, cek1, cek2, cek3, cek4, cek5, cek6))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM cekovi WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, sifra, ime, prezime, ukupan_iznos, uplaceno, broj_cekova, datum_prvi_cek, maros_mix, fishing_world, cek1, cek2, cek3, cek4, cek5, cek6):
        self.cur.execute("UPDATE cekovi SET sifra = ?, ime = ?, prezime = ?, ukupan_iznos = ?, uplaceno = ?, broj_cekova = ?, datum_prvi_cek = ?, maros_mix = ?, fishing_world = ?, cek1 = ?, cek2 = ?, cek3 = ?, cek4 = ?, cek5 = ?, cek6 = ? WHERE id = ?",
                         (sifra, ime, prezime, ukupan_iznos, uplaceno, broj_cekova, datum_prvi_cek, maros_mix, fishing_world, cek1, cek2, cek3, cek4, cek5, cek6, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    # write a function to count number of unique ime and prezime in the database
    def count(self):
        self.cur.execute("SELECT COUNT(DISTINCT ime || prezime) FROM cekovi")
        row = self.cur.fetchall()
        return row