# %%
import pprint
import matplotlib.pyplot as plt
from collections import Counter


# %%
texto = 'PRV XK VFUSLBQQH AHI IRHDR PHZUBWL. ¡YBWB GB DNXF, FOLXWRUX GB IRHDR! ¡KR MDPDODP!'
texto_clean = 'PRV XK VFUSLBQQH AHI PHZUBWL. ¡YBWB GB DNXF, FOLXWRUX GB IRHDR! ¡KR MDPDODP!'
key = 'xD'

# %%
frequency = Counter(texto_clean)
letters = [char for char in frequency.keys() if char.isalpha()]
total_letters = sum(frequency[char] for char in letters)

relative_counts = [frequency[char] / total_letters * 100 for char in letters]
print(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

plt.bar(letters, relative_counts)
plt.xlabel('Letters')
plt.ylabel('Frequency (%)')
plt.title('Relative Frequency of Letters in Text')
plt.show()

# %%

def remplazar():
    global texto
    for char in texto:
        key = {
            'B': 'e',
            'R': 'o',

            'D': 'a',
            'P': 's',

            'X': 'u',
            'H': 's',

            'F': 'i',
            'U': '_',

            'L': 'n',
            'W': 't',

            'Y': 'v',
            'G': 'd',
            'N': 'q',
            'V': 'y',
            'K': 'n',
            'M': 'p',
            'O': 'r',
            'A': 'e',
            'I': 'a',
        }

        if not char.isalpha():
            yield char
        else:
            yield ' ' if key.get(char) is None else key.get(char)


print(f'{texto}\n{"".join(remplazar())}')
