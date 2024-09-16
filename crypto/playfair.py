import colorama

colors = [ colorama.Fore.RED, colorama.Fore.GREEN]

def printm(matrix, highlight=[]):
    f = 0
    for row in matrix:
        for c in row:
            if c in highlight:
                print(colors[f % len(colors)] + c + colorama.Style.RESET_ALL, end=' ')
                f += 1
            else:
                print(c, end=' ')
        print('')
    print('')

matrix = [
    'keyab',
    'cdfgh',
    'ilmno',
    'pqrst',
    'uvwxz'
]

nombre = "danielalejandroxosorniolopezx"

split_name = [nombre[i:i+2] for i in range(0, len(nombre), 2)]

for part in split_name:
    print(part)
    highlight_chars = list(part)
    printm(matrix, highlight=highlight_chars)
