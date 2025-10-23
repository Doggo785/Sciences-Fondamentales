N = 3233  # le module public (N = p * q)
E = 17    # l'exposant public (celui qui figure sur le parchemin)

# Liste des nombres chiffrés trouvés sur le parchemin.
# Chaque entier représente un "bloc" chiffré avec RSA.
C = [1877, 1956, 1313, 2235, 281, 2160, 745, 1313, 1992, 281, 1313, 1992, 1369, 3179, 745, 1230, 1992, 1773, 1313, 1992, 612, 2160, 884, 1313, 1992, 1773, 1313, 1992, 597, 1632, 2271, 1773, 1696, 2185, 2160, 1992, 1877, 28, 1992, 2159, 28, 1992, 524, 2790, 1486, 2680, 28, 1992, 2159, 1307, 1486, 1992, 28, 2159, 1992, 2159, 1307, 2310, 2159, 28, 1992, 2159, 2790, 1992, 325, 2790, 3123, 1486, 2726, 2726, 28, 1992, 1759, 28, 1992, 641, 3000, 1486, 28, 3165]

def egcd(a, b):
    """
    Petit algorithme d'Euclide étendu (récursif).
    On l'utilise pour trouver l'inverse de E modulo phi(N).
    Retour : (g, x, y) tel que a*x + b*y = g = gcd(a, b).
    """
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    """
    Trouve l'inverse de 'a' modulo 'm' si possible.
    Renvoie None si 'a' et 'm' ne sont pas premiers entre eux.
    """
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def factor_naive(n):
    """
    Factorisation par essais simples (trial division).
    Très basique : adaptée aux petits N d'exercice.
    Si N est grand (vrai RSA), cette méthode échouera.
    """
    # si N est pair, on renvoie 2 et l'autre facteur
    if n % 2 == 0:
        return 2, n // 2
    i = 3
    import math
    limit = int(math.isqrt(n)) + 1
    # tester les diviseurs impairs jusqu'à sqrt(n)
    while i <= limit:
        if n % i == 0:
            return i, n // i
        i += 2
    return None

def main():
    # 1) On cherche p et q en factorisant N.
    fac = factor_naive(N)
    if fac is None:
        print("Je n'ai pas réussi à factoriser N avec cette méthode (N trop grand).")
        return
    p, q = fac
    # Afficher ce qu'on a trouvé pour transparence
    print(f"Facteurs trouvés : p = {p}, q = {q}")

    # 2) Calcul de phi(N) = (p-1)*(q-1)
    phi = (p - 1) * (q - 1)

    # 3) Calcul de la clé privée d telle que d * E ≡ 1 (mod phi)
    d = modinv(E, phi)
    if d is None:
        print("Impossible de calculer l'inverse de E modulo phi(N).")
        return
    print(f"Clé privée d calculée : d = {d}")

    # 4) Déchiffrement : pour chaque bloc c, on calcule m = c^d mod N
    #    Puis on reconstruit les octets et on concatène pour obtenir le message.
    out = bytearray()
    for c in C:
        m = pow(c, d, N)
        # Si m vaut 0 on ajoute un 0, sinon on convertit l'entier en octets big-endian.
        if m == 0:
            out.extend(b'\x00')
        else:
            blen = (m.bit_length() + 7) // 8
            out.extend(m.to_bytes(blen, 'big'))

    # 5) On essaie d'afficher en UTF-8 (souvent le cas), sinon on tombe en Latin-1.
    try:
        message = out.decode('utf-8')
    except Exception:
        message = out.decode('latin-1')

    print("Message déchiffré :")
    print(message)

if __name__ == '__main__':
    main()
