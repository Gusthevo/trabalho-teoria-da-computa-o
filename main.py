import json

class MaquinaTuring:
    def __init__(self, config_maquina):
        # Aqui inicializa a máquina com a configuração do arquivo JSON
        self.estados = set(config_maquina["K"])  # Conjunto de estados possíveis
        self.alfabeto_fita = set(config_maquina["Gamma"])  # Símbolos da fita
        self.simb_branco = config_maquina["branco"]  # Símbolo em branco (⊔)
        self.simb_inicio = "⊳"  # Símbolo de início da fita
        self.estado_atual = config_maquina["s"]  # Estado atual (começando no estado inicial)
        self.estado_inicial = config_maquina["s"]  # Guarda o estado inicial
        self.estados_parada = set(config_maquina["H"])  # Conjunto de estados de parada (aceitação/rejeição)
        
        # Aqui é preparada as transições (regras da máquina)
        self.transicoes = {}
        for chave, valor in config_maquina["delta"].items():
            # Extrai estado e símbolo de cada transição (ex: "(q0,a)" -> "q0" e "a")
            estado, simbolo = chave.strip("()").split(",")
            self.transicoes[(estado.strip(), simbolo.strip())] = tuple(valor)

        # Configuração inicial da fita
        self.fita = []  # A fita será uma lista de símbolos
        self.pos = 0  # Posição do cabeçote
        self.historico = []  # Lista que vai guardar todos os passos da execução

    def carregar_entrada(self, w):
        # Prepara a fita com a palavra de entrada
        # Formato: [⊳, ⊔, w[0], w[1], ...]
        self.fita = [self.simb_inicio, self.simb_branco] + list(w)
        self.pos = 2  # Começa após os símbolos ⊳⊔
        self.estado_atual = self.estado_inicial
        self.historico = [(self.estado_atual, list(self.fita), self.pos)]  # Salva estado inicial

    def passo(self):
        # Executa UM passo da máquina
        simbolo = self.fita[self.pos]  # Lê símbolo na posição atual
        chave = (self.estado_atual, simbolo)
        
        # Se não há transição definida, a máquina trava
        if chave not in self.transicoes:
            return False
            
        # Aplica a transição: (novo estado, símbolo a escrever, direção)
        novo_estado, escreve, direcao = self.transicoes[chave]
        self.fita[self.pos] = escreve  # Escreve na fita
        self.estado_atual = novo_estado  # Atualiza estado
        
        # Move o cabeçote para a direita ou esquerda
        if direcao == "R":
            self.pos += 1
            if self.pos >= len(self.fita):
                self.fita.append(self.simb_branco)  # Expande a fita se necessário
        elif direcao == "L":
            if self.pos > 0:
                self.pos -= 1
                
        # Registra no histórico
        self.historico.append((self.estado_atual, list(self.fita), self.pos))
        return True

    def executar(self, max_passos=100):
        # Executa a máquina até parar ou atingir o limite de passos
        passos = 0
        while passos < max_passos:
            # Verifica se chegou em estado de parada
            if self.estado_atual in self.estados_parada:
                if self.estado_atual == "q_accept":
                    return (True, "aceita", passos)
                elif self.estado_atual == "q_reject":
                    return (False, "rejeita", passos)
                return (True, f"parou em {self.estado_atual}", passos)
                
            # Executa um passo
            if not self.passo():
                return (False, "rejeita-trava", passos)
            passos += 1
            
        return (False, "rejeita-limite", passos)  # Limite de passos atingido

    def mostrar_historico(self):
        # Mostra todo o histórico de execução no terminal
        for i, (estado, fita, pos) in enumerate(self.historico):
            fita_visual = fita.copy()
            fita_visual[pos] = f"[{fita_visual[pos]}]"  # Destaca posição atual
            fita_str = "".join(fita_visual)
            print(f"Passo {i}: Estado={estado} | Fita={fita_str}")

def main():
    # Função principal que controla a execução
    arquivo_maquina = input("Insira o nome do arquivo da máquina de Turing: ")
    with open(arquivo_maquina, "r", encoding="utf-8") as f:
        dados = json.load(f)  # Carrega configuração do arquivo JSON

    mt = MaquinaTuring(dados)  # Definimos aqui a criação da máquina
    
    palavra = input("Digite a palavra de entrada: ")
    mt.carregar_entrada(palavra)  # Carrega a palavra na fita
    
    # Mostra configuração inicial
    print("Configuração inicial:")
    print("Fita:", mt.fita)
    print("Estado inicial:", mt.estado_atual)
    print("Posição inicial:", mt.pos)

    # Configura limite de passos
    entrada = input("Número padrão de transições por etapa = 100, mas defina quantas quer: ").strip()
    X = int(entrada) if entrada else 100
    continuar = True

    # Loop de execução
    while continuar:
        resultado, motivo, passos = mt.executar(X)
        
        if resultado:
            print(f"\nA Máquina PAROU no estado de parada: {mt.estado_atual} após {passos} passos.")
            break
        else:
            if motivo == "rejeita-trava":
                print(f"\nA Máquina REJEITOU a palavra (travou no estado {mt.estado_atual} após {passos} passos).")
            else:
                print(f"\nA Máquina REJEITOU a palavra (atingiu o limite de {passos} passos no estado {mt.estado_atual}).")
        
        # Pergunta se quer continuar
        resposta = input("Deseja continuar mais X passos? (s/n): ").strip().lower()
        if resposta != "s":
            break

    # Opção para ver histórico completo
    ver_tudo = input("Deseja ver todas as configurações? (s/n): ").strip().lower()
    if ver_tudo == "s":
        print("\nHistórico completo da computação:")
        mt.mostrar_historico()

if __name__ == "__main__":
    main()  # Inicia o programa