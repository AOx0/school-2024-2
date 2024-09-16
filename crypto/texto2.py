# %%
to_pos = lambda w: [ord(c) - ord('a') for c in w]

def cifrar_parte(texto):
    for i, b in enumerate(to_pos(texto)):
        ki = to_pos("key")[i % len("key")]

        if b == ord(' ') - ord('a'):
            yield ' '
        else:
            nc = (ki + b) % 26
            print(f"{ki:>3}, {b:>3}, {ki + b:>3}, {nc:>3}, {chr(nc + ord('a'))}")
            yield chr(nc + ord('a'))

"".join(cifrar_parte("daniel alejandro osornio lopez"))
