from PIL import Image, ImageChops
import os


class AparadorImagens:

    def __init__(
        self,
        pasta_origem="questoes",
        pasta_destino="finalizadas",
        margem=8,
        tolerancia=245
    ):

        self.pasta_origem = pasta_origem
        self.pasta_destino = pasta_destino
        self.margem = margem
        self.tolerancia = tolerancia

        os.makedirs(self.pasta_destino, exist_ok=True)

    def encontrar_area_util(self, imagem):

        fundo = Image.new(
            imagem.mode,
            imagem.size,
            (255, 255, 255)
        )

        diferenca = ImageChops.difference(imagem, fundo)

        diferenca = diferenca.point(
            lambda p: 0 if p < (255 - self.tolerancia) else p
        )

        caixa = diferenca.getbbox()

        if caixa is None:
            return imagem.height

        _, _, _, inferior = caixa

        return min(inferior + self.margem, imagem.height)

    def aparar(self, caminho_entrada, caminho_saida):

        imagem = Image.open(caminho_entrada)

        limite = self.encontrar_area_util(imagem)

        imagem = imagem.crop((0, 0, imagem.width, limite))

        imagem.save(caminho_saida)

        print(f"✓ {os.path.basename(caminho_entrada)}")

    def listar_imagens(self):

        return sorted(
            arquivo
            for arquivo in os.listdir(self.pasta_origem)
            if arquivo.lower().endswith(".png")
        )

    def executar(self):

        imagens = self.listar_imagens()

        if not imagens:
            print("Nenhuma imagem encontrada.")
            return

        print(f"{len(imagens)} imagens encontradas.\n")

        for imagem in imagens:

            entrada = os.path.join(
                self.pasta_origem,
                imagem
            )

            saida = os.path.join(
                self.pasta_destino,
                imagem
            )

            self.aparar(entrada, saida)

        print("\nProcessamento concluído!")


if __name__ == "__main__":

    aparador = AparadorImagens(
        pasta_origem="questoes",
        pasta_destino="finalizadas",
        margem=8
    )

    aparador.executar()