import json

class MaquinaTuring:
    def __init__(self, config_maquina):
        self.estados = set(config_maquina["K"])
        self.alfabeto_fita = set(config_maquina["Gamma"])
        self.simb_branco = config_maquina["branco"]
        self.simb_inicio = "⊳"
        self.estado_atual = config_maquina["s"]
        self.estado_inicial = config_maquina["s"]
        self.estados_parada = set(config_maquina["H"])
        self.transicoes = {}
        for chave, valor in config_maquina["delta"].items():
            estado, simbolo = chave.strip("()").split(",")
            self.transicoes[(estado.strip(), simbolo.strip())] = tuple(valor)

        self.fita = []
        self.pos = 0
        self.historico = []

    def carregar_entrada(self, w):
        self.fita = [self.simb_inicio, self.simb_branco] + list(w)
        self.pos = 2
        self.estado_atual = self.estado_inicial
        self.historico = [(self.estado_atual, list(self.fita), self.pos)]

    def passo(self):
        simbolo = self.fita[self.pos]
        chave = (self.estado_atual, simbolo)
        if chave not in self.transicoes:
            return False
        novo_estado, escreve, direcao = self.transicoes[chave]
        self.fita[self.pos] = escreve
        self.estado_atual = novo_estado
        if direcao == "R":
            self.pos += 1
            if self.pos >= len(self.fita):
                self.fita.append(self.simb_branco)
        elif direcao == "L":
            if self.pos > 0:
                self.pos -= 1
        self.historico.append((self.estado_atual, list(self.fita), self.pos))
        return True

    def executar(self, max_passos=10):
        passos = 0
        while passos < max_passos:
            if self.estado_atual in self.estados_parada:
                return passos  # já está num estado de parada
            if not self.passo():
                return passos  # não há transição, máquina trava
            passos += 1
            if self.estado_atual in self.estados_parada:
                return passos  # entrou em estado de parada após um passo
        return passos


    def mostrar_historico(self):
        for i, (estado, fita, pos) in enumerate(self.historico):
            fita_visual = fita.copy()
            fita_visual[pos] = f"[{fita_visual[pos]}]"
            fita_str = "".join(fita_visual)
            print(f"Passo {i}: Estado={estado} | Fita={fita_str}")

# Execução da máquina
def main():
    arquivo_maquina = input("Arquivo da máquina de Turing: ")
    with open(arquivo_maquina, "r", encoding="utf-8") as f:
        dados = json.load(f)

    mt = MaquinaTuring(dados)
    palavra = input("Digite a palavra de entrada: ")
    mt.carregar_entrada(palavra)

    entrada = input("Número máximo de transições por etapa (X) [padrão = 10]: ").strip()
    X = int(entrada) if entrada else 10
    continuar = True

    while continuar:
        passos = mt.executar(X)
        if mt.estado_atual in mt.estados_parada:
            print("\nA Máquina parou em um estado de parada.")
            break
        print(f"\nForam executados {passos} passos. A máquina ainda não parou em um estado final.")
        print("Estado atual:", mt.estado_atual)
        resposta = input("Deseja continuar mais X passos? (s/n): ").strip().lower()
        if resposta != "s":
            break

    ver_tudo = input("Deseja ver todas as configurações? (s/n): ").strip().lower()
    if ver_tudo == "s":
        print("\nEsse é o histórico da computação até agora:")
        mt.mostrar_historico()

if __name__ == "__main__":
    main()
