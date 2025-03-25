def ecrire_variable(fichier, cle, valeur):
    """Écrit une variable dans un fichier texte."""
    with open(fichier, "w") as f:
        f.write(f"{cle}={valeur}\n")

def lire_variable(fichier, cle):
    """Lit une variable depuis un fichier texte."""
    try:
        with open(fichier, "r") as f:
            lignes = f.readlines()
            for ligne in lignes:
                if ligne.startswith(cle):
                    _, valeur = ligne.strip().split("=")
                    return int(valeur)
    except FileNotFoundError:
        # Si le fichier n'existe pas, retourner None
        return None
    except ValueError:
        print("Erreur : Fichier de sauvegarde corrompu.")
        return None
