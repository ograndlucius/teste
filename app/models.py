from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from pydantic import BaseModel
from sqlalchemy import func, label
from . import models


Base = declarative_base()

class ItemBase(BaseModel):
    nome: str
    descricao: str
    estoque: int
    preco: float

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

class ItemDB(Base):
    __tablename__ = "itens"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    estoque = Column(Integer)
    preco = Column(Float)


    @classmethod
    def create(cls, db: Session, nome: str, descricao: str, estoque: int, preco: float):
        item = cls(nome=nome, descricao=descricao, estoque=estoque, preco=preco)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @classmethod
    def get_all(cls, db, skip=0, limit=100):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db, item_id):
        return db.query(cls).filter(cls.id == item_id).first()

    @classmethod
    def update(cls, db, item_id, nome, descricao, estoque, preco):
        item = cls.get_by_id(db, item_id)
        if item:
            item.nome = nome
            item.descricao = descricao
            item.estoque = estoque
            item.preco = preco
            db.commit()
            db.refresh(item)
        return item

    @classmethod
    def delete(cls, db, item_id):
        item = cls.get_by_id(db, item_id)
        if item:
            db.delete(item)
            db.commit()
        return item

class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    pedidos = relationship("PedidoDB", back_populates="usuario")

    @classmethod
    def create(cls, db: Session, usuario_create: UsuarioCreate):
        usuario = cls(**usuario_create.dict())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 10):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: Session, usuario_id: int):
        return db.query(cls).filter(cls.id == usuario_id).first()

    @classmethod
    def update(cls, db: Session, usuario_id: int, usuario_update: UsuarioCreate):
        usuario = cls.get_by_id(db, usuario_id)
        if usuario:
            for key, value in usuario_update.dict().items():
                setattr(usuario, key, value)
            db.commit()
            db.refresh(usuario)
        return usuario

    @classmethod
    def delete(cls, db: Session, usuario_id: int):
        usuario = cls.get_by_id(db, usuario_id)
        if usuario:
            db.delete(usuario)
            db.commit()
        return usuario
    
class PedidoResponse(BaseModel):
    id: int
    item_id: int
    quantidade: int
    usuario_id: int

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    item_id: int
    quantidade: int

class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    item_id = Column(Integer, ForeignKey("itens.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("UsuarioDB", back_populates="pedidos")
    item = relationship("ItemDB")


class ProductReport(BaseModel):
    nome: str
    quantidade_vendida: int

class ProductCustomerReport(BaseModel):
    nome_produto: str
    nome_cliente: str
    quantidade_comprada: int

class AvgConsumptionReport(BaseModel):
    nome_cliente: str
    produto_mais_comprado: str
    consumo_medio_quantidade: float
    consumo_medio_preco: float

class AvgConsumptionResponse(BaseModel):
    response: list[AvgConsumptionReport]

class LowStockProductReport(BaseModel):
    nome: str
    estoque: int

def get_top_sold_products(db: Session, top_count: int = 3):
    result = (
        db.query(models.ItemDB.nome, func.sum(models.PedidoDB.quantidade).label("quantidade_vendida"))
        .join(models.PedidoDB)
        .group_by(models.ItemDB.nome)
        .order_by(func.sum(models.PedidoDB.quantidade).desc())
        .limit(top_count)
        .all()
    )
    return result

def get_product_by_customer_report(db: Session):
    result = (
        db.query(
            models.ItemDB.nome.label("nome_produto"),
            models.UsuarioDB.nome.label("nome_cliente"),
            func.sum(models.PedidoDB.quantidade).label("quantidade_comprada")
        )
        .join(models.PedidoDB, models.PedidoDB.item_id == models.ItemDB.id)
        .join(models.UsuarioDB, models.PedidoDB.usuario_id == models.UsuarioDB.id)
        .group_by(models.ItemDB.nome, models.UsuarioDB.nome)
        .all()
    )
    return result



def get_avg_consumption_by_customer_report(db: Session):
    result = (
        db.query(
            UsuarioDB.nome.label("nome_cliente"),
            label("consumo_medio", func.avg(PedidoDB.quantidade * ItemDB.preco))
        )
        .join(PedidoDB)
        .join(ItemDB)
        .group_by(UsuarioDB.nome)
        .all()
    )

    response_data = [
        {
            "nome_cliente": nome_cliente,
            "consumo_medio": float(consumo_medio) if consumo_medio else 0.0
        }
        for nome_cliente, consumo_medio in result
    ]

    return response_data

def get_low_stock_products_report(db: Session):
    result = db.query(models.ItemDB.nome, models.ItemDB.estoque).filter(models.ItemDB.estoque <= 3).all()
    return [{"nome": nome, "estoque": estoque} for nome, estoque in result]

