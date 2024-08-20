import numpy as np
import sympy as sp

def cifrar(P, Key):
    C = np.array([ord(c) - ord('a') for c in P.lower() if c != ' '])
    Cp = C.reshape(-1, 3)

    return " ".join(["".join([chr(v + ord('a')) for v in np.matmul(c, Key) % 26]) for c in Cp])


def decifrar(C, Key):
    P = np.array([ord(c) - ord('a') for c in C if c != ' '])
    Pp = P.reshape(-1, 3)

    Key_inv = sp.Matrix(Key).inv_mod(26)

    return " ".join(["".join([chr(v + ord('a')) for v in np.matmul(c, Key_inv) % 26]) for c in Pp])

P = "Pay more money"
Key = np.array([[17, 17, 5], [21, 18, 21], [2, 2, 19]])

C = cifrar(P, Key)
P = decifrar(C, Key)

C, P

# matriz inversa en modulo 26:
# np.dot(np.array([[5,8], [17, 3]]),  np.array([[9, 2], [1, 15]])) # No devuelve identidad
# np.dot(np.array([[5,8], [17, 3]]),  np.array([[9, 2], [1, 15]])) % 16 # Si lo hace
