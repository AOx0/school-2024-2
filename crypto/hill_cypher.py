import numpy as np
import sympy as sp

M = 3

def cifrar(P, Key):
    C = np.array([ord(c) - ord('a') for c in P.lower() if c != ' '])
    Cp = C.reshape(-1, M)

    print(Cp)
    print(np.array([np.matmul(c, Key) % 26 for c in Cp]))

    return " ".join(["".join([chr(v + ord('a')) for v in np.matmul(c, Key) % 26]) for c in Cp])


def decifrar(C, Key):
    P = np.array([ord(c) - ord('a') for c in C if c != ' '])
    Pp = P.reshape(-1, M)

    Key_inv = sp.Matrix(Key).inv_mod(26)

    return " ".join(["".join([chr(v + ord('a')) for v in np.matmul(c, Key_inv) % 26]) for c in Pp])

P = "daniel alejandro osornio lopez"
Key = np.array([[23, 17, 23], [21, 10, 21], [10, 5, 13]])

C = cifrar(P, Key)
P = decifrar(C, Key)

print(C + '\n' + P)


# matriz inversa en modulo 26:
# np.dot(np.array([[5,8], [17, 3]]),  np.array([[9, 2], [1, 15]])) # No devuelve identidad
# np.dot(np.array([[5,8], [17, 3]]),  np.array([[9, 2], [1, 15]])) % 16 # Si lo hace
