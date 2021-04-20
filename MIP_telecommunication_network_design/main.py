from gurobipy import *
from grafo_pronto import grafo
from visual import visual
G = grafo()
modelo = Model('telecom')
x = modelo.addVars(len(G.nos),len(G.nos),len(G.demandas),vtype=GRB.BINARY,name='fluxo')
y = modelo.addVars(len(G.nos),len(G.nos),G.tam_capacidade,vtype=GRB.BINARY,name='modulo')
obj = LinExpr()
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for t in range(G.tam_capacidade):
            obj += y[i,j,t] * G.matriz_adjacencia_custo[i][j][t]


for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        fluxo = LinExpr()
        for k in range(len(G.demandas)):
            fluxo += x[i,j,k] * G.matriz_adjacencia_demanda[i][j][k]
        capacidade = LinExpr()
        for t in range(len(G.matriz_adjacencia_capacidade[i][j])):
            capacidade+= y[i,j,t] * G.matriz_adjacencia_capacidade[i][j][t]
        modelo.addLConstr(fluxo <= capacidade)

for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    for i in range(len(G.nos)):
        if i == ok or i == dk:
            continue
        entrando = LinExpr()
        for j in range(len(G.nos)):
            if j == dk or j == i:
                continue
            entrando += x[j,i,k]
        saindo = LinExpr()
        for j in range(len(G.nos)):
            if j == ok or j == i:
                continue
            saindo += x[i,j,k]
        modelo.addLConstr(entrando == saindo)

for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    entrando = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        entrando+= x[j,ok,k]
    saindo = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        saindo += x[ok,j,k]
    modelo.addLConstr(entrando == 0)
    modelo.addLConstr(saindo == 1)

for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    entrando = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        entrando+= x[j,dk,k]
    saindo = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        saindo += x[dk,j,k]
    modelo.addLConstr(entrando == 1)
    modelo.addLConstr(saindo == 0)

modelo.setObjective(obj,sense=GRB.MINIMIZE)
modelo.Params.timeLimit = 60.0
modelo.optimize()

vx = [[[0 for k in range(len(G.demandas))] for j in range(len(G.nos))] for i in range(len(G.nos))]

for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for k in range(len(G.demandas)):
            vx[i][j][k]=int(x[i,j,k].getAttr(GRB.Attr.X))


vy = [[[0 for k in range(G.tam_capacidade)] for j in range(len(G.nos))] for i in range(len(G.nos))]
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for t in range(len(G.matriz_adjacencia_capacidade[i][j])):
            vy[i][j][t] = int(y[i,j,t].getAttr(GRB.Attr.X))

vis = visual(G,vx,vy)


