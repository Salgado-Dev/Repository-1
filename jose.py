from PIL import Image, ImageEnhance, ImageFilter
import os
import shutil

# ==========================
# PROCURAR IMAGEM
# ==========================

script_dir = os.path.dirname(os.path.abspath(__file__))

locais = [
    os.path.join(script_dir, "baixei.png"),
    os.path.join(os.path.expanduser("~"), "Downloads", "baixei.png")
]

imagem = None

for caminho in locais:
    if os.path.isfile(caminho):
        imagem = caminho
        break

if imagem is None:
    print("\nERRO:")
    print("baixei.png não foi encontrada.")
    print("\nLocais verificados:")

    for caminho in locais:
        print(caminho)

    input("\nPressione Enter para sair...")
    raise SystemExit

print(f"\nImagem encontrada:\n{imagem}")

# ==========================
# CORES ANSI
# ==========================

def fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

# ==========================
# ABRIR IMAGEM
# ==========================

try:
    img = Image.open(imagem).convert("RGB")

    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(2.5)
    img = img.filter(ImageFilter.DETAIL)

    largura_terminal = shutil.get_terminal_size().columns

    largura = min(
        max(40, largura_terminal - 2),
        img.width
    )

    proporcao = img.height / img.width

    altura = int(largura * proporcao)

    if altura % 2 != 0:
        altura += 1

    img = img.resize(
        (largura, altura),
        Image.Resampling.LANCZOS
    )

    pixels = img.load()

    os.system("cls" if os.name == "nt" else "clear")

    for y in range(0, altura - 1, 2):

        linha = []

        for x in range(largura):

            r1, g1, b1 = pixels[x, y]
            r2, g2, b2 = pixels[x, y + 1]

            linha.append(
                f"{fg(r1,g1,b1)}"
                f"{bg(r2,g2,b2)}▀"
            )

        linha.append("\033[0m")

        print("".join(linha))

except Exception as erro:

    print("\nERRO:")
    print(erro)

input("\nPressione Enter para sair...")
