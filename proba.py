from math import comb

p = 0.6
n = 5

print("Probabilités pour k jours avec couverture nuageuse < 50% :")
for k in range(n + 1):
    prob = comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    print(f"{k} jours : {prob:.4f} soit {prob*100:.2f}%")

print("\nProbabilité d'avoir au moins 3 jours avec couverture nuageuse < 50% :")
prob_at_least_3 = sum(comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(3, n + 1))
print(f"{prob_at_least_3*100:.2f}%")