#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################################
# Mannaggiatore automatico per VUA depressi - Python Edition
# Convertito da mannaggia.sh rel 0.2
# Originale:
# idea originale by Alexiobash dallo script incazzatore.sh
# ampliata, riscritta e mantenuta da Pietro "Legolas" Suffritti
# convertita in mannaggia.sh rel 0.2
# Collaborators:
# Enrico "Henryx" Bianchi, Alessandro "Aleskandro" Di Stefano,
# Davide "kk0nrad" Corrado
# patcher e contributors:
# Marco Placidi, Maurizio "Tannoiser" Lemmo, Matteo Panella
# Mattia Munari
# thanks to : Veteran Unix Admins group on Facebook
# released under GNU-GPLv3
############################################################

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import random
import os
import time
import threading
import re
import subprocess
import tempfile
from bs4 import BeautifulSoup
import locale
import platform

class MannaggiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mannaggiatore Automatico")
        self.root.geometry("650x550")
        
        # Variabili di controllo
        self.audio_var = tk.BooleanVar(value=False)
        self.wall_var = tk.BooleanVar(value=False)
        self.spm_var = tk.IntVar(value=60)  # Santi per minuto
        self.nds_var = tk.IntVar(value=-1)  # Numero di santi (-1 = infinito)
        self.shutdown_var = tk.BooleanVar(value=False)
        
        # Flag per controllo esecuzione
        self.running = False
        self.thread = None
        self.saints_count = 0
        
        # Creazione dell'interfaccia
        self._create_widgets()
        
    def _create_widgets(self):
        # Frame principale diviso in due parti
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame sinistro per i controlli
        controls_frame = ttk.LabelFrame(main_frame, text="Impostazioni", padding="10")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Opzione Audio
        ttk.Checkbutton(controls_frame, text="Audio (TTS)", variable=self.audio_var).pack(anchor=tk.W, pady=5)
        
        # Opzione Wall
        ttk.Checkbutton(controls_frame, text="Wall (tutti terminali)", variable=self.wall_var).pack(anchor=tk.W, pady=5)
        
        # Santi per minuto
        spm_frame = ttk.Frame(controls_frame)
        spm_frame.pack(fill=tk.X, pady=5)
        ttk.Label(spm_frame, text="Santi per minuto:").pack(side=tk.LEFT)
        ttk.Spinbox(spm_frame, from_=1, to=120, textvariable=self.spm_var, width=5).pack(side=tk.RIGHT)
        
        # Numero di santi
        nds_frame = ttk.Frame(controls_frame)
        nds_frame.pack(fill=tk.X, pady=5)
        ttk.Label(nds_frame, text="Numero di santi (-1=infinito):").pack(side=tk.LEFT)
        ttk.Spinbox(nds_frame, from_=-1, to=1000, textvariable=self.nds_var, width=5).pack(side=tk.RIGHT)
        
        # Opzione shutdown
        shutdown_check = ttk.Checkbutton(controls_frame, text="Spegni al termine", variable=self.shutdown_var)
        shutdown_check.pack(anchor=tk.W, pady=5)
        
        # Opzione off (shortcut)
        ttk.Button(controls_frame, text="OFF (1 santo e spegni)", 
                  command=self.set_off_mode).pack(fill=tk.X, pady=10)
        
        # Pulsanti Start/Stop
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(buttons_frame, text="Start", command=self.start_mannaggia)
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.stop_mannaggia, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # Contatore santi
        self.counter_label = ttk.Label(controls_frame, text="Santi invocati: 0")
        self.counter_label.pack(pady=10)
        
        # Frame destro per l'output
        output_frame = ttk.LabelFrame(main_frame, text="Output Mannaggia", padding="10")
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Area di testo per l'output
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=40, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        # Barra di stato
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_off_mode(self):
        self.nds_var.set(1)
        self.shutdown_var.set(True)
        self.start_mannaggia()
    
    def add_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def update_counter(self):
        self.counter_label.config(text=f"Santi invocati: {self.saints_count}")
    
    def start_mannaggia(self):
        if self.running:
            return
        
        # Verifica se l'audio è richiesto
        if self.audio_var.get():
            if platform.system() == "Linux":
                try:
                    subprocess.run(["which", "mplayer"], check=True, stdout=subprocess.PIPE)
                except subprocess.CalledProcessError:
                    messagebox.showerror("Errore", "Mplayer non trovato! Installalo con 'sudo apt install mplayer'")
                    return
        
        # Verifica se wall è richiesto e l'utente ha i permessi
        if self.wall_var.get() and os.geteuid() != 0:
            response = messagebox.askyesno("Avviso", 
                "L'opzione wall richiede permessi di root/sudo. Continuare comunque?")
            if not response:
                return
        
        # Verifica se shutdown è selezionato e l'utente ha i permessi
        if self.shutdown_var.get() and os.geteuid() != 0:
            messagebox.showerror("Errore", "L'opzione shutdown richiede permessi di root!")
            self.shutdown_var.set(False)
        
        # Reset contatore
        self.saints_count = 0
        self.update_counter()
        
        # Avvia il thread per la generazione dei mannaggia
        self.running = True
        self.thread = threading.Thread(target=self.mannaggia_worker)
        self.thread.daemon = True
        self.thread.start()
        
        # Aggiorna i pulsanti
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("In esecuzione...")
    
    def stop_mannaggia(self):
        if not self.running:
            return
        
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Fermato")
    
    def get_random_saint(self):
        try:
            # Genera una lettera casuale dell'alfabeto
            letter = chr(random.randint(65, 90))  # A-Z
            
            # Prima richiesta per ottenere il numero di pagine
            resp = requests.get(f"https://www.santiebeati.it/{letter}/")
            soup = BeautifulSoup(resp.content, "html.parser")
            
            # Trova il numero di pagine (se esistono)
            pages = 1
            pages_text = soup.find(text=re.compile("Pagina:"))
            if pages_text:
                pages_match = re.search(r"Pagina:\s*\d+/(\d+)", pages_text)
                if pages_match:
                    pages = int(pages_match.group(1))
            
            # Scegli una pagina casuale
            page = random.randint(1, pages)
            if page == 1:
                path = ""
            else:
                path = f"more{page}.html"
            
            # Scarica la pagina specifica
            url = f"https://www.santiebeati.it/{letter}/{path}"
            resp = requests.get(url)
            resp.encoding = 'ISO-8859-1'  # Il sito usa questa codifica
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Estrai tutti i santi dalla pagina
            saints = []
            for font_tag in soup.find_all("font", size="-2"):
                if font_tag.find_next("font") and font_tag.find_next("font").find("b"):
                    name = font_tag.text.strip()
                    title = font_tag.find_next("font").find("b").text.strip()
                    saints.append(f"{name} {title}")
            
            if not saints:
                return "San Kernel Panic protettore dei programmatori disperati"
            
            # Scegli un santo a caso
            return random.choice(saints)
            
        except Exception as e:
            self.add_output(f"Errore nel recupero dei santi: {str(e)}")
            return "San Kernel Panic protettore dei programmatori disperati"
    
    def say_text(self, text):
        try:
            # Usa Google TTS (come nello script originale)
            text_for_url = text.replace(" ", "+")
            url = f"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={text_for_url}&tl=it"
            
            # Scarica l'audio e riproducilo con mplayer
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_file = f.name
            
            r = requests.get(url)
            with open(temp_file, 'wb') as f:
                f.write(r.content)
            
            subprocess.Popen(["mplayer", "-ao", "alsa", "-really-quiet", "-noconsolecontrols", temp_file],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Il file verrà automaticamente eliminato alla chiusura del programma
        except Exception as e:
            self.add_output(f"Errore nella riproduzione audio: {str(e)}")
    
    def mannaggia_worker(self):
        nds = self.nds_var.get()
        
        while self.running and (nds == -1 or nds > 0):
            # Calcola ritardo in secondi
            delay = 60 / self.spm_var.get()
            
            # Genera il mannaggia
            saint = self.get_random_saint()
            mannaggia_text = f"Mannaggia {saint}"
            
            # Output speciale ogni 50 santi (come nello script originale)
            if self.wall_var.get() and self.saints_count % 50 == 0 and self.saints_count > 0:
                special_text = "systemd merda, poettering vanaglorioso fonte di danni, ti strafulmini santa cunegonda bipalluta protrettice dei VUA"
                self.add_output(special_text)
                
                # Usa wall se abilitato
                if self.wall_var.get():
                    try:
                        process = subprocess.Popen(["sudo", "wall", "-n"], stdin=subprocess.PIPE)
                        process.communicate(special_text.encode())
                    except Exception as e:
                        self.add_output(f"Errore con wall: {str(e)}")
            else:
                # Output normale
                self.add_output(mannaggia_text)
                
                # Usa wall se abilitato
                if self.wall_var.get():
                    try:
                        process = subprocess.Popen(["sudo", "wall", "-n"], stdin=subprocess.PIPE)
                        process.communicate(mannaggia_text.encode())
                    except Exception as e:
                        self.add_output(f"Errore con wall: {str(e)}")
            
            # TTS se abilitato
            if self.audio_var.get():
                self.say_text(mannaggia_text)
            
            # Aggiorna contatore
            self.saints_count += 1
            self.root.after(0, self.update_counter)
            
            # Decrementa nds se necessario
            if nds > 0:
                nds -= 1
            
            # Aspetta prima del prossimo
            time.sleep(delay)
        
        # Fine del ciclo
        self.root.after(0, self.stop_mannaggia)
        
        # Spegni se richiesto
        if self.shutdown_var.get() and os.geteuid() == 0:
            self.add_output("Spegnimento in corso...")
            self.root.after(2000, lambda: os.system("halt"))

def main():
    # Imposta locale per supportare caratteri italiani
    try:
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except:
            pass
    
    root = tk.Tk()
    app = MannaggiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
