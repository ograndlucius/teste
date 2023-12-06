from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database
from pydantic import BaseModel
from typing import List
from app import models

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# Modelo Pydantic para representar a resposta da criação de um item
class ItemCreate(BaseModel):
    nome: str
    descricao: str
    estoque: int
    preco: float  

class UsuarioCreate(BaseModel):
    nome: str
    email: str

class PedidoCreate(BaseModel):
    item_id: int
    quantidade: int

class PedidoResponse(BaseModel):
    id: int
    item_id: int
    quantidade: int
    usuario_id: int

    class Config:
        from_attribute = True

class UsuarioDeleteResponse(models.BaseModel):
    message: str

class ProductReport(BaseModel):
    nome: str
    quantidade_vendida: int

class ProductCustomerReport(BaseModel):
    nome_produto: str
    nome_cliente: str
    quantidade_comprada: int

class AvgConsumptionReport(BaseModel):
    nome_cliente: str
    consumo_medio: float

class LowStockProductReport(BaseModel):
    nome: str
    estoque: int

# Função para popular o banco de dados com dados de exemplo.
def seed_data():
    db = database.SessionLocal()
    db.query(models.ItemDB).delete()
    db.query(models.UsuarioDB).delete()
    db.query(models.PedidoDB).delete()

    users = [
        {'nome': "Adailton Lima Segundo", "email": "adlima@bol.com"},
        {'nome': "Gabriel Badas",         "email": "gbadas@globomail.com"},
        {'nome': "Lucius Nascimento",     "email": "lucius2010@yahoo.com"},
        {'nome': "Professor Xavier",      "email": "xaviersisdb@gmail.com"},
        {'nome': "Vivian Santana",        "email": "adv.vivi@gov.br"},
    ]
    for user in users:
        models.UsuarioDB.create(db, models.UsuarioCreate(**user))

    products = [
        {'nome': "Tilápia Fresca",        "descricao": "Tilápia fresca, perfeita para grelhados e assados.",               "estoque": 10,  "preco": 9.99 },
        {'nome': "Atum Selvagem",         "descricao": "Atum selvagem, ideal para sashimi e pratos de peixe cru.",         "estoque": 8,   "preco": 19.99},
        {'nome': "Salmão do Atlântico",   "descricao": "Salmão do Atlântico, rico em ácidos graxos ômega-3.",              "estoque": 12,  "preco": 14.99},
        {'nome': "Linguado Fresco",       "descricao": "Linguado fresco, delicado e perfeito para pratos gourmet.",        "estoque": 7,   "preco": 24.99},
        {'nome': "Truta Arco-Íris",       "descricao": "Truta arco-íris, saborosa e versátil em várias receitas.",         "estoque": 1,   "preco": 12.99},
        {'nome': "Bacalhau do Atlântico", "descricao": "Bacalhau do Atlântico, clássico em pratos de bacalhau.",           "estoque": 20,  "preco": 29.99},
        {'nome': "Robalo Fresco",         "descricao": "Robalo fresco, excelente para grelhados e pratos assados.",        "estoque": 1,   "preco": 16.99},
        {'nome': "Peixe-gato de Cultivo", "descricao": "Peixe-gato de cultivo, ideal para frituras e ensopados.",          "estoque": 1,   "preco": 8.99 },
        {'nome': "Lula",                  "descricao": "Lula limpa, pronta para preparar pratos de frutos do mar.",        "estoque": 6,   "preco": 22.99}, 
        {'nome': "Camarão Fresco",        "descricao": "Camarão fresco, ótimo para pratos como paella e camarão ao alho.", "estoque": 5,   "preco": 18.99}, 
    ]
    
    for product in products: 
        item = models.ItemDB.create(db, product["nome"], product["descricao"], product["estoque"], product["preco"])
        print(f"Item criado: {item}")

    db.close()

# Chama a função seed_data sempre que o aplicativo for iniciado ou reiniciado
seed_data()

## ROTAS DE ESTOQUE ##########################################################################################################################################

# Rota para criar um novo item
@app.post("/estoque/adicionar/", response_model=models.Item)
def create_item(item_create: ItemCreate, db: Session = Depends(database.get_db)):
    return models.ItemDB.create(db, item_create.nome, item_create.descricao, item_create.estoque, item_create.preco)


# Rota para obter todos os itens
@app.get("/estoque/", response_model_exclude_unset=True)
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    # Retorno dos modelos reais (models.ItemDB) nas respostas das rotas
    return models.ItemDB.get_all(db, skip=skip)

# Rota para obter um item por ID
@app.get("/estoque/{item_id}", response_model_exclude_unset=True)
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    item = models.ItemDB.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return item

# Rota para atualizar um item por ID
@app.put("/estoque/atualizar/{item_id}", response_model=ItemCreate)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(database.get_db)):
    updated_item = models.ItemDB.update(db, item_id, item.nome, item.descricao, item.estoque, item.preco)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return updated_item

# Rota para excluir um item por ID
@app.delete("/estoque/remove/{item_id}", response_model_exclude_unset=True)
def delete_item(item_id: int, db: Session = Depends(database.get_db)):
    deleted_item = models.ItemDB.delete(db, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return JSONResponse(content={"message": "Item excluído."})

# ROTAS CLIENTES ####################################################################################################################################################
# Rota para criar um novo usuário
@app.post("/usuarios/adicionar/", response_model=models.Usuario)
def create_usuario(usuario_create: UsuarioCreate, db: Session = Depends(database.get_db)):
    return models.UsuarioDB.create(db, usuario_create)

# Rota para obter todos os usuários
@app.get("/usuarios/", response_model=List[models.Usuario])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return models.UsuarioDB.get_all(db, skip=skip, limit=limit)

# Rota para obter um usuário por ID
@app.get("/usuarios/{usuario_id}", response_model=models.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    usuario = models.UsuarioDB.get_by_id(db, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario

# Rota para atualizar um usuário por ID
@app.put("/usuarios/atualizar/{usuario_id}", response_model=models.UsuarioBase)
def update_usuario(usuario_id: int, usuario_update: UsuarioCreate, db: Session = Depends(database.get_db)):
    updated_usuario = models.UsuarioDB.update(db, usuario_id, usuario_update)
    if updated_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return updated_usuario

# Rota para excluir um usuário por ID
@app.delete("/usuarios/remover/{usuario_id}", response_model=UsuarioDeleteResponse)
def delete_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    deleted_usuario = models.UsuarioDB.delete(db, usuario_id)
    if deleted_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {"message": "Usuário excluído."}

# OPERAÇÕES GERAIS ################################################################################################################################################
# Rota para fazer um pedido de compra
@app.post("/pedido/adicionar/{usuario_id}", response_model=models.PedidoResponse)
def add_pedido(usuario_id: int, pedido_create: models.PedidoCreate, db: Session = Depends(database.get_db)):
    # Verifica se o usuário é válido
    usuario = models.UsuarioDB.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Verifica se o item existe
    item = models.ItemDB.get_by_id(db, pedido_create.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado.")

    # Calcula o valor total do pedido
    valor_total = item.preco * pedido_create.quantidade

    # Atualiza o estoque
    if item.estoque >= pedido_create.quantidade:
        item.estoque -= pedido_create.quantidade
        db.commit()

        # Cria o pedido associado ao usuário
        pedido = models.PedidoDB(
            item_id=pedido_create.item_id,
            quantidade=pedido_create.quantidade,
            usuario_id=usuario_id
        )
        db.add(pedido)
        db.commit()

        # Relaciona o pedido ao usuário
        usuario.pedidos.append(pedido)
        db.commit()

    

        return pedido
    else:
        raise HTTPException(status_code=400, detail="Quantidade solicitada maior do que o estoque disponível.")
    
# Relatório de produto mais vendido
@app.get("/relatorios/maisvendido/", response_model=List[ProductReport])
def get_top_sold_products(db: Session = Depends(database.get_db)):
    return models.get_top_sold_products(db)

# Relatório de produto por cliente
@app.get("/relatorios/produtocliente/", response_model=List[ProductCustomerReport])
def get_product_by_customer_report(db: Session = Depends(database.get_db)):
    return models.get_product_by_customer_report(db)

# Relatório de consumo médio por cliente
@app.get("/relatorios/consumocliente/", response_model=List[AvgConsumptionReport])
def get_avg_consumption_by_customer_report(db: Session = Depends(database.get_db)):
    return models.get_avg_consumption_by_customer_report(db)

# Relatório de produto de baixo estoque (igual ou abaixo de 3)
@app.get("/relatorios/baixoestoque/", response_model=List[LowStockProductReport])
def get_low_stock_products_report(db: Session = Depends(database.get_db)):
    return models.get_low_stock_products_report(db)