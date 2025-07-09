# Modern Tkinter Battleship (Amiral Battı)
# Tema sistemi, modern font, emoji destekli, alt etiketli

import tkinter as tk
import random
from tkinter import messagebox

BOYUT = 5
HARFLER = ['A', 'B', 'C', 'D', 'E']

TEMALAR = {
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "gemi": "#2ecc71",
        "isabet": "#e74c3c",
        "iska": "#3498db",
        "bos": "#ffffff",
        "panel": "#2c3e50"
    },
    "light": {
        "bg": "#ecf0f1",
        "fg": "#2c3e50",
        "gemi": "#27ae60",
        "isabet": "#c0392b",
        "iska": "#2980b9",
        "bos": "#ffffff",
        "panel": "#bdc3c7"
    }
}

class ModernBattleship:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Amiral Battı - Modern")
        self.tema = "dark"
        self.tema_ayarla()
        self.giris_ekrani()

    def tema_ayarla(self):
        t = TEMALAR[self.tema]
        self.bg = t["bg"]
        self.fg = t["fg"]
        self.gemi_r = t["gemi"]
        self.isabet_r = t["isabet"]
        self.iska_r = t["iska"]
        self.bos_r = t["bos"]
        self.panel_r = t["panel"]
        self.pencere.configure(bg=self.bg)

    def tema_degistir(self):
        self.tema = "light" if self.tema == "dark" else "dark"
        self.tema_ayarla()
        self.reset_oyun()

    def giris_ekrani(self):
        self.clear()

        baslik = tk.Label(self.pencere, text="AMİRAL BATTI", font=("Segoe UI", 24, "bold"), fg=self.fg, bg=self.bg)
        baslik.pack(pady=20)

        tk.Button(self.pencere, text="BAŞLA", font=("Segoe UI", 14), command=self.zorluk_secimi, bg=self.panel_r).pack(pady=10)
        tk.Button(self.pencere, text="🎨 Tema Değiştir", command=self.tema_degistir).pack()

        imza = tk.Label(self.pencere, text="Talha Özkan tarafından yapılmıştır", font=("Segoe UI", 9), fg="gray", bg=self.bg)
        imza.pack(side="left", anchor="s", padx=10, pady=10)

    def zorluk_secimi(self):
        self.clear()
        tk.Label(self.pencere, text="Zorluk Seçin", font=("Segoe UI", 16), bg=self.bg, fg=self.fg).pack(pady=10)
        for z, (gemi, can) in {
            "Kolay (3 Gemi, 5 Can)": (3, 5),
            "Orta (4 Gemi, 4 Can)": (4, 4),
            "Zor (5 Gemi, 3 Can)": (5, 3)
        }.items():
            tk.Button(self.pencere, text=z, width=25, command=lambda g=gemi, c=can: self.baslat(g, c), bg=self.panel_r).pack(pady=5)

    def baslat(self, gemi, can):
        self.GEMI = gemi
        self.CAN = can
        self.oyuncu_can = can
        self.bilgisayar_can = gemi
        self.oyuncu_gemileri = 0
        self.oyuncu_tahta = [["-" for _ in range(BOYUT)] for _ in range(BOYUT)]
        self.bilgisayar_tahta = [["-" for _ in range(BOYUT)] for _ in range(BOYUT)]
        self.oyuncu_butonlar = [[None]*BOYUT for _ in range(BOYUT)]
        self.bilgisayar_butonlar = [[None]*BOYUT for _ in range(BOYUT)]
        self.bilgisayar_saldirdigi = set()
        self.isabet = 0
        self.toplam = 0
        self.gemi_yerlestirme_ekrani()

    def gemi_yerlestirme_ekrani(self):
        self.clear()
        tk.Label(self.pencere, text=f"Gemilerini Yerleştir: {self.oyuncu_gemileri}/{self.GEMI}", bg=self.bg, fg=self.fg, font=("Segoe UI", 14)).pack(pady=10)
        frame = tk.Frame(self.pencere, bg=self.bg)
        frame.pack()
        for y in range(BOYUT):
            for x in range(BOYUT):
                btn = tk.Button(frame, text=f"{HARFLER[y]}{x+1}", width=6, height=2,
                                command=lambda x=x, y=y: self.gemi_koy(x, y), bg=self.bos_r)
                btn.grid(row=y, column=x, padx=2, pady=2)
                self.oyuncu_butonlar[y][x] = btn

    def gemi_koy(self, x, y):
        if self.oyuncu_gemileri >= self.GEMI:
            return
        if self.oyuncu_tahta[y][x] == "G":
            return
        self.oyuncu_tahta[y][x] = "G"
        self.oyuncu_butonlar[y][x].config(bg=self.gemi_r)
        self.oyuncu_gemileri += 1
        if self.oyuncu_gemileri == self.GEMI:
            self.bilgisayar_gemi_yerlestir()
            self.oyun_ekrani()

    def bilgisayar_gemi_yerlestir(self):
        sayac = 0
        while sayac < self.GEMI:
            x, y = random.randint(0, BOYUT-1), random.randint(0, BOYUT-1)
            if self.bilgisayar_tahta[y][x] != "G":
                self.bilgisayar_tahta[y][x] = "G"
                sayac += 1

    def oyun_ekrani(self):
        self.clear()
        self.bilgi = tk.Label(self.pencere, text=f"Can: {self.oyuncu_can} | Rakip Gemi: {self.bilgisayar_can}", bg=self.bg, fg=self.fg, font=("Segoe UI", 14))
        self.bilgi.pack(pady=10)
        frame = tk.Frame(self.pencere, bg=self.bg)
        frame.pack()
        o_frame = tk.LabelFrame(frame, text="Senin Tablon", bg=self.bg, fg=self.fg)
        b_frame = tk.LabelFrame(frame, text="Rakip Tablo", bg=self.bg, fg=self.fg)
        o_frame.grid(row=0, column=0, padx=20)
        b_frame.grid(row=0, column=1, padx=20)

        for y in range(BOYUT):
            for x in range(BOYUT):
                obtn = tk.Label(o_frame, text=f"{HARFLER[y]}{x+1}", width=6, height=2, relief="ridge", font=("Segoe UI", 9), bg=self.bos_r)
                if self.oyuncu_tahta[y][x] == "G":
                    obtn.config(bg=self.gemi_r)
                obtn.grid(row=y, column=x, padx=1, pady=1)
                self.oyuncu_butonlar[y][x] = obtn

                bbtn = tk.Button(b_frame, text=f"{HARFLER[y]}{x+1}", width=6, height=2,
                                 command=lambda x=x, y=y: self.oyuncu_atis(x, y), bg=self.bos_r)
                bbtn.grid(row=y, column=x, padx=1, pady=1)
                self.bilgisayar_butonlar[y][x] = bbtn

    def oyuncu_atis(self, x, y):
        btn = self.bilgisayar_butonlar[y][x]
        if btn['state'] == 'disabled': return

        if self.bilgisayar_tahta[y][x] == "G":
            btn.config(text="🎯", bg=self.isabet_r)
            self.bilgisayar_can -= 1
            self.isabet += 1
        else:
            btn.config(text="❌", bg=self.iska_r)

        btn.config(state="disabled")
        self.toplam += 1
        self.bilgi.config(text=f"Can: {self.oyuncu_can} | Rakip Gemi: {self.bilgisayar_can}")

        if self.bilgisayar_can == 0:
            self.oyun_bitti("Kazandın!")
        else:
            self.pencere.after(800, self.bilgisayar_atis)

    def bilgisayar_atis(self):
        while True:
            x, y = random.randint(0, BOYUT-1), random.randint(0, BOYUT-1)
            if (x, y) not in self.bilgisayar_saldirdigi:
                self.bilgisayar_saldirdigi.add((x, y))
                break

        if self.oyuncu_tahta[y][x] == "G":
            self.oyuncu_can -= 1
            self.oyuncu_butonlar[y][x].config(bg=self.isabet_r, text="💥")
        else:
            self.oyuncu_butonlar[y][x].config(bg=self.iska_r, text="💨")

        self.bilgi.config(text=f"Can: {self.oyuncu_can} | Rakip Gemi: {self.bilgisayar_can}")

        if self.oyuncu_can == 0:
            self.oyun_bitti("Kaybettin!")

    def oyun_bitti(self, mesaj):
        oran = round((self.isabet / self.toplam) * 100, 2) if self.toplam > 0 else 0
        messagebox.showinfo("Oyun Bitti", f"{mesaj}\nİsabet: {self.isabet}\nAtış: {self.toplam}\nBaşarı: %{oran}")
        self.giris_ekrani()

    def clear(self):
        for w in self.pencere.winfo_children():
            w.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernBattleship(root)
    root.mainloop()
