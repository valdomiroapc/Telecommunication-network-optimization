from gurobipy import *
from grafo_pronto import grafo
from visual import visual
G = grafo()
modelo = Model('telecom')
x = modelo.addVars(len(G.demandas),len(G.nos),len(G.nos),vtype=GRB.BINARY,name='fluxo')
y = modelo.addVars(G.tam_capacidade,len(G.nos),len(G.nos),vtype=GRB.BINARY,name='modulo')
obj = LinExpr()
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[i][j] !=-1:
            e = G.matriz_adjacencia[i][j]
            aux = G.arestas[e].module_list
            for t in range(len(aux)):
                obj += y[t,i,j]*aux[t].cost

for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[i][j] != -1:
            fluxo = LinExpr()
            for k in range(len(G.demandas)):
                hk = G.demandas[k].routing_value
                fluxo+=x[k,i,j]*hk
            capacidade = LinExpr()
            e = G.matriz_adjacencia[i][j]
            pre_inst = G.arestas[e].pre_installed_capacity
            for t in range(len(G.arestas[e].module_list)):
                cap = G.arestas[e].module_list[t].capacidade
                capacidade+=y[t,i,j]*cap

            modelo.addLConstr(fluxo <= capacidade)

idx = 0
#Flow conservation
for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    for i in range(len(G.nos)):
        if i != ok and i != dk:
            entrando = LinExpr()
            deu = 0
            for j in range(len(G.nos)):
                if G.matriz_adjacencia[j][i] != -1 and j != dk:
                    deu = 1
                    entrando += x[k,j,i]

            saindo = LinExpr()
            deu1 = 0
            for j in range(len(G.nos)):
                if G.matriz_adjacencia[i][j] != -1 and j != ok:
                    deu1 = 1
                    saindo += x[k,i,j]
            if deu:
                modelo.addLConstr(entrando == saindo,name=str(idx))
                idx+=1

for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    saindo = LinExpr()
    deu = 0
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[ok][j] != -1:
            deu = 1
            saindo += x[k,ok,j]
    entrando = LinExpr()
    deu1 = 0
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[j][ok] != -1 and j!=dk:
            deu1 = 1
            entrando += x[k,j,ok]
    if deu:
        modelo.addLConstr(saindo == 1,name=str(idx))
        idx+=1
    if deu1:
        modelo.addLConstr(entrando == 0,name=str(idx))
        idx+=1

for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    entrando = LinExpr()
    deu = 0
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[j][dk] != -1:
            deu = 1
            entrando += x[k,j,dk]
    saindo = LinExpr()
    deu1 = 0
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[dk][j] != -1 and j!=ok:
            deu = 1
            saindo += x[k,dk,j]
    if deu:
        modelo.addLConstr(entrando == 1,name=str(idx))
        idx+=1
    if deu1:
        modelo.addLConstr(saindo == 0,name=str(idx))
        idx+=1

modelo.setObjective(obj,sense=GRB.MINIMIZE)
modelo.Params.timeLimit = 180.0
modelo.optimize()
print('--------------',len(G.demandas),'----',len(G.nos),'-------------')
vx = [[[0 for j in range(len(G.nos))] for i in range(len(G.nos))] for k in range(len(G.demandas))]
for k in range(len(G.demandas)):
    for i in range(len(G.nos)):
        for j in range(len(G.nos)):
            vx[k][i][j]=int(x[k,i,j].getAttr(GRB.Attr.X))


vy = [[[] for j in range(len(G.nos))] for i in range(len(G.nos))]
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        if G.matriz_adjacencia[i][j] != -1:
            e = G.matriz_adjacencia[i][j]
            aux = [0 for t in range(len(G.arestas[e].module_list))]
            for t in range(len(G.arestas[e].module_list)):
                aux[t]=int(y[t,i,j].getAttr(GRB.Attr.X))
            vy[i][j] = aux
        else:
            vy[i][j] = [0 for t in range(G.tam_capacidade)]


vis = visual(G,vx,vy)

print('custo gurobi>>>>>',modelo.getAttr(GRB.Attr.ObjVal))
print(G.tam_capacidade)