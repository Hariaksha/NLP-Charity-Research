import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5, 5))
labels = 'A: Arts, Culture, and Humanities', 'B: Education', 'C: Environment', 'D: Animal-Related', 'E: Health Care', "F: Mental Health and Crisis Intervention", "G: Voluntary Health Associations & Medical Disciplines", "H: Medical Research", "I: Crime & Legal-Related", "J: Employment", "K: Food, Agriculture & Nutrition", "L: Housing & Shelter", "M: Public Safety, Disaster Preparedness & Relief", "N: Recreation & Sports", "O: Youth Development", "P: Human Services", "Q: International, Foreign Affairs & National Security", "R: Civil Rights, Social Action & Advocacy", "S: Community Improvement & Capacity Building", "T: Philanthropy, Voluntarism & Grantmaking Foundations", "U: Science & Technology", "V: Social Science", "W: Public & Societal Benefit", "X: Religion-Related", "Y: Mutual & Membership Benefit", "Z: Unknown"

sizes = [len(A), len(B), len(C), len(D), len(E), len(F), len(G), len(H), len(I), len(J), len(K), len(L), len(M), len(N), len(O), len(P), len(Q), len(R), len(S), len(T), len(U), len(V), len(W), len(X), len(Y), len(Z)]

plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.show()