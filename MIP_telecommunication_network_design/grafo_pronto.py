import copy
class modules:
    capacidade = float()
    cost = float()
    def __init__(self,capacidade,cost):
        self.capacidade = capacidade
        self.cost = cost

class nodes:
    nome = str()
    cx = float()
    cy = float()
    def __init__(self,nome,cx,cy):
        self.nome = nome
        self.cx = cx
        self.cy = cy

class links:
    nome = str()
    nome_i=str()
    nome_j=str()
    pre_installed_capacity = float()
    pre_installed_capacity_cost = float()
    routing_cost = float()
    setup_cost = float()
    module_list = []
    idx_i = int()
    idx_j = int()
    def __init__(self,nome,nome_i,nome_j,pre_installed_capacity,pre_installed_capacity_cost,routing_cost,setup_cost,module_list,idx_i,idx_j):
        self.nome = nome
        self.nome_i = nome_i
        self.nome_j = nome_j
        self.pre_installed_capacity = pre_installed_capacity
        self.pre_installed_capacity_cost = pre_installed_capacity_cost
        self.routing_cost = routing_cost
        self.setup_cost = setup_cost
        self.module_list = module_list
        self.idx_i = idx_i
        self.idx_j = idx_j

class demands:
    nome = str()
    nome_i = str()
    nome_j = str()
    routing_unit = int()
    routing_value = float()
    demand_type = str()
    idx_i = int()
    idx_j = int()
    def __init__(self,nome,nome_i,nome_j,routing_unit,routing_value,demand_type,idx_i,idx_j):
        self.nome = nome
        self.nome_i = nome_i
        self.nome_j = nome_j
        self.routing_unit = routing_unit
        self.routing_value = routing_value
        self.demand_type = demand_type
        self.idx_i = idx_i
        self.idx_j = idx_j

class grafo:
    nos = []
    arestas = []
    demandas = []
    idx_nos={}
    matriz_adjacencia = None
    tam_capacidade = 0
    def __processa_nos(self):
        caminho_nodes = r'instancia1\nodes'
        arq = open(caminho_nodes,'r')
        while(1==1):
            linha = arq.readline().split()
            if len(linha) == 0:
                break
            nome = linha[0]
            cx = float(linha[2])
            cy = float(linha[3])
            self.idx_nos[nome] = int(len(self.nos))
            self.nos.append(nodes(nome,cx,cy))
        arq.close()

    def __processa_links(self,tipo_aresta):
        caminho_links = r'instancia1\links'
        arq = open(caminho_links,'r')
        self.matriz_adjacencia = [[-1 for j in range(len(self.nos))] for i in range(len(self.nos))]
        while 1==1:
            linha = arq.readline().split()
            if len(linha) == 0:
                break
            nome = linha[0]
            nome_i = linha[2]
            nome_j = linha[3]
            pre_installed_capacity = float(linha[5])
            pre_installed_capacity_cost = float(linha[6])
            routing_cost = float(linha[7])
            setup_cost = float(linha[8])
            module_list = []
            i=10
            while linha[i] !=')':
                module_list.append(modules(float(linha[i]),float(linha[i+1])))
                i+=2
            if tipo_aresta == 'U':
                self.matriz_adjacencia[self.idx_nos[nome_i]][self.idx_nos[nome_j]] = int(len(self.arestas))
                self.matriz_adjacencia[self.idx_nos[nome_j]][self.idx_nos[nome_i]] = int(len(self.arestas))
            else:
                self.matriz_adjacencia[self.idx_nos[nome_i]][self.idx_nos[nome_j]] = int(len(self.arestas))
            if len(module_list) > self.tam_capacidade:
                self.tam_capacidade = int(len(module_list))
            self.arestas.append(links(nome,nome_i,nome_j,pre_installed_capacity,pre_installed_capacity_cost,routing_cost,setup_cost,module_list,self.idx_nos[nome_i],self.idx_nos[nome_j]))

    def __processa_demands(self):
        caminho_demandas = r'instancia1\demands'
        arq = open(caminho_demandas,'r')
        while 1==1:
            linha = arq.readline().split()
            if len(linha) == 0:
                break
            nome = linha[0]
            nome_i = linha[2]
            nome_j = linha[3]
            routing_unit = int(linha[5])
            demands_value = float(linha[6])
            demands_type = linha[7]
            idx_i = int(self.idx_nos[nome_i])
            idx_j = int(self.idx_nos[nome_j])
            self.demandas.append(demands(nome,nome_i,nome_j,routing_unit,demands_value,demands_type,idx_i,idx_j))

    def __init__(self,tipo_aresta='U'):
        self.__processa_nos()
        self.__processa_links(tipo_aresta)
        self.__processa_demands()

