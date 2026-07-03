import os


class RenomeadorQuestoes:

    def __init__(self, pasta, inicio, fim):
        self.pasta = pasta
        self.inicio = inicio
        self.fim = fim

    def obter_imagens(self):

        if not os.path.isdir(self.pasta):
            raise FileNotFoundError(f"Pasta '{self.pasta}' não encontrada.")

        imagens = [
            arquivo
            for arquivo in os.listdir(self.pasta)
            if arquivo.startswith("parte_") and arquivo.endswith(".png")
        ]

        imagens.sort(
            key=lambda arquivo: int(
                arquivo.replace("parte_", "").replace(".png", "")
            )
        )

        return imagens

    def renomear(self):

        imagens = self.obter_imagens()

        esperado = self.fim - self.inicio + 1

        print(f"Imagens encontradas: {len(imagens)}")
        print(f"Questões esperadas: {esperado}")

        if len(imagens) != esperado:
            print("\nATENÇÃO:")
            print("A quantidade de imagens é diferente da quantidade esperada.")
            print("O processo continuará apenas com as imagens existentes.\n")

        numero = self.inicio

        for imagem in imagens:

            if numero > self.fim:
                break

            origem = os.path.join(self.pasta, imagem)

            destino = os.path.join(
                self.pasta,
                f"questao-{numero}.png"
            )

            if os.path.exists(destino):
                os.remove(destino)

            os.rename(origem, destino)

            print(f"{imagem}  ->  questao-{numero}.png")

            numero += 1

        print("\nRenomeação concluída!")


if __name__ == "__main__":

    pasta = "37-43"

    inicio = 37
    fim = 43

    renomeador = RenomeadorQuestoes(
        pasta=pasta,
        inicio=inicio,
        fim=fim
    )

    renomeador.renomear()