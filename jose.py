from PIL import Image, ImageEnhance, ImageFilter
import os
import shutil

# ==========================
# CONFIG
# ==========================

PASTA_IMAGENS = "imagempy"

# ==========================
# FUNÇÕES
# ==========================

def encontrar_imagem():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    pasta = os.path.join(script_dir, PASTA_IMAGENS)

    if not os.path.exists(pasta):
        os.makedirs(pasta)

        raise FileNotFoundError(
            f"\nA pasta foi criada:\n{pasta}\n\n"
            f"Coloque uma imagem nela e execute novamente."
        )

    extensoes = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".webp"
    )

    for arquivo in os.listdir(pasta):

        if arquivo.lower().endswith(extensoes):
            return os.path.join(pasta, arquivo)

    raise FileNotFoundError(
        f"\nNenhuma imagem encontrada em:\n{pasta}"
    )

def fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

# ==========================
# MAIN
# ==========================

try:

    imagem = encontrar_imagem()

    print(f"\nImagem encontrada:")
    print(imagem)

    img = Image.open(imagem).convert("RGB")

    # Melhorias visuais

    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.DETAIL)

    terminal = shutil.get_terminal_size()

    largura_terminal = max(
        40,
        terminal.columns - 2
    )

    largura = min(
        largura_terminal,
        img.width
    )

    proporcao = img.height / img.width

    altura = int(
        largura * proporcao
    )

    if altura % 2 != 0:
        altura += 1

    img = img.resize(
        (largura, altura),
        Image.Resampling.LANCZOS
    )

    pixels = img.load()

    os.system("cls")

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