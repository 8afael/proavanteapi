from database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Float

# class Users(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True)
#     username = Column(String, unique=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#     role = Column(String)

class Dashboard(Base):
    __tablename__= 'dashboard'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    ticker = Column(String)
    company = Column(String)
    actualValue = Column(Float)
    lucroLiquido = Column(Float)
    patrimonioLiquido = Column(Float)
    acoesEmitidas = Column(BigInteger)
    precoTeto = Column(Float)
    dividendo1ano = Column(Float)
    dividendo2ano = Column(Float)
    dividendo3ano = Column(Float)
    dividendo4ano = Column(Float)
    dividendo5ano = Column(Float)
    #complete = Column(Boolean, default=False)
    #owner_id = Column(Integer, ForeignKey("users.id"))