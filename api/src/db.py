import  os
from    sqlalchemy                 import create_engine
from    sqlalchemy.orm             import sessionmaker
from    sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://xtiqdxqijpalyg:29ce786ec9eb67436b1392b438b03cbe8a779f00869cd1ccf763c399e940acb2@ec2-18-209-143-227.compute-1.amazonaws.com:5432/d6i6l2t43ot65q")
# engine = create_engine(result)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()