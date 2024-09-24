# %%
to_pos = lambda w: [ord(c) - ord('a') for c in w]

def descifrar_parte(texto: str, key: str):
    texto = texto.lower()
    act = 0
    for i, b in enumerate(to_pos(texto)):
        ki = to_pos(key)[act % len(key)]

        if b in [ord(c) - ord('a') for c in [' ', '!', '¡', '.', ',']]:
            yield chr(b + ord('a'))
        else:
            nc = (-ki + b) % 26
            print(f"{ki:>3}, {b:>3}, {-ki + b:>3}, {nc:>3}, {chr(nc + ord('a'))}")
            yield chr(nc + ord('a'))
            act += 1

def cifrar_parte(texto: str, key: str):
    texto = texto.lower()
    act = 0
    for i, b in enumerate(to_pos(texto)):
        ki = to_pos(key)[act % len(key)]

        if b in [ord(c) - ord('a') for c in [' ', '!', '¡', '.', ',']]:
            yield chr(b + ord('a'))
        else:
            nc = (ki + b) % 26
            print(f"{ki:>3}, {b:>3}, {ki + b:>3}, {nc:>3}, {chr(nc + ord('a'))}")
            yield chr(nc + ord('a'))
            act += 1
"".join(cifrar_parte("PRV XK VFUSLBQQH AHI IRHDR PHZUBWL. ¡YBWB GB DNXF, FOLXWRUX GB IRHDR! ¡KR MDPDODP!"))
