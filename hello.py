#!/usr/bin/env python3
# min_app.py
# Enkelt ett-fils verktøy: kalkulator, to-do (lagres i todo.txt), og tekst-analysator.
# Ingen import av biblioteker (kun innebygde språk-funksjoner).

TODO_FILE = "todo.txt"

def pause():
    input("\nTrykk Enter for å gå tilbake til menyen...")

# -------------------------
# To-do-funksjoner (fil-basert)
# -------------------------
def load_todos():
    todos = []
    try:
        f = open(TODO_FILE, "r", encoding="utf-8")
        for line in f:
            line = line.rstrip("\n")
            if line:
                todos.append(line)
        f.close()
    except Exception:
        # fil finnes kanskje ikke ennå
        pass
    return todos

def save_todos(todos):
    try:
        f = open(TODO_FILE, "w", encoding="utf-8")
        for item in todos:
            f.write(item + "\n")
        f.close()
    except Exception as e:
        print("Klarte ikke lagre todo:", e)

def show_todos():
    todos = load_todos()
    if not todos:
        print("Ingen oppgaver i todo-lista.")
    else:
        print("Oppgaver:")
        for i, t in enumerate(todos, start=1):
            print(f" {i}. {t}")

def add_todo():
    tekst = input("Skriv oppgaven du vil legge til: ").strip()
    if tekst:
        todos = load_todos()
        todos.append(tekst)
        save_todos(todos)
        print("Oppgave lagt til.")
    else:
        print("Tom oppgave — ingenting lagt til.")

def remove_todo():
    todos = load_todos()
    if not todos:
        print("Ingen oppgaver å fjerne.")
        return
    show_todos()
    valg = input("Skriv nummeret til oppgaven du vil fjerne (eller trykk Enter for å avbryte): ").strip()
    if not valg:
        print("Avbryter.")
        return
    if not valg.isdigit():
        print("Ugyldig input.")
        return
    idx = int(valg) - 1
    if 0 <= idx < len(todos):
        fjernet = todos.pop(idx)
        save_todos(todos)
        print(f"Fjernet: {fjernet}")
    else:
        print("Nummer utenfor rekkevidde.")

# -------------------------
# Enkel kalkulator (ingen eval for hele uttrykk)
# Format: <tall> <operator> <tall>, for eksempel: 12 + 5
# Støtter + - * / % ** (potens) // (heltallsdiv)
# -------------------------
def kalkulator():
    print("Enkel kalkulator. Skriv: <tall> <operator> <tall>")
    print("Eksempel: 12 + 5")
    print("Støttede operatorer: + - * / % ** //")
    inp = input("Uttrykk: ").strip()
    if not inp:
        print("Ingen input.")
        return
    parts = inp.split()
    if len(parts) != 3:
        print("Skriv nøyaktig tre deler separert med mellomrom (tall operator tall).")
        return
    a_s, op, b_s = parts
    try:
        # prøv først som heltall, fallback til float
        if "." in a_s or "e" in a_s.lower():
            a = float(a_s)
        else:
            a = int(a_s)
        if "." in b_s or "e" in b_s.lower():
            b = float(b_s)
        else:
            b = int(b_s)
    except Exception:
        print("Kun tall (heltall eller desimal) støttes som operander.")
        return

    try:
        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            res = a / b
        elif op == "%":
            res = a % b
        elif op == "**":
            res = a ** b
        elif op == "//":
            res = a // b
        else:
            print("Ukjent operator.")
            return
    except Exception as e:
        print("Feil ved kalkulasjon:", e)
        return

    print("Resultat:", res)

# -------------------------
# Tekst-analysator: teller ord, unike ord, og tegn
# -------------------------
def tekst_analyse():
    print("Lim inn eller skriv tekst (avslutt med en tom linje):")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines)
    if not text:
        print("Ingen tekst angitt.")
        return
    # tegn
    tegn = len(text)
    # ord (enkel splitting på whitespace)
    ordliste = []
    for part in text.split():
        # fjern noen vanlige tegn rundt ord (enkel rens)
        clean = strip_punctuation(part)
        if clean:
            ordliste.append(clean.lower())
    totalt_ord = len(ordliste)
    unike = {}
    for w in ordliste:
        unike[w] = unike.get(w, 0) + 1
    sortert = sorted(unike.items(), key=lambda kv: -kv[1])
    print("Tegn totalt:", tegn)
    print("Ord totalt:", totalt_ord)
    print("Unike ord:", len(unike))
    print("\nMest brukte ord (topp 10):")
    for i, (w, c) in enumerate(sortert[:10], start=1):
        print(f" {i}. {w} — {c} ganger")

def strip_punctuation(s):
    # fjerner start/slutt "vanlige" skilletegn uten imports
    # beholder norske bokstaver som de er
    start = 0
    end = len(s)
    punct = ".,:;!?\"'()[]{}<>«»/\\|@#¤$%&*+-=—_`~"
    while start < end and s[start] in punct:
        start += 1
    while end > start and s[end-1] in punct:
        end -= 1
    return s[start:end]

# -------------------------
# Hovedmeny
# -------------------------
def hovedmeny():
    while True:
        print("\n=== ENKEL PY-APP (én fil, ingen biblioteker) ===")
        print("1) To-do: vis oppgaver")
        print("2) To-do: legg til oppgave")
        print("3) To-do: fjern oppgave")
        print("4) Kalkulator")
        print("5) Tekst-analysator (teller ord/tegn)")
        print("6) Avslutt")
        valg = input("Velg (1-6): ").strip()
        if valg == "1":
            show_todos()
            pause()
        elif valg == "2":
            add_todo()
            pause()
        elif valg == "3":
            remove_todo()
            pause()
        elif valg == "4":
            kalkulator()
            pause()
        elif valg == "5":
            tekst_analyse()
            pause()
        elif valg == "6":
            print("Ha det! 🙂")
            break
        else:
            print("Ugyldig valg, prøv igjen.")

if __name__ == "__main__":
    hovedmeny()
