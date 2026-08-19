import os

os.environ["DATABASE_URL"] = "sqlite:///./test_loja.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database
from database import Base, get_db
from main import app

engine = create_engine(
    "sqlite:///./test_loja.db",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

created = client.post(
    "/produtos",
    json={"nome": "Teclado", "preco": 99.9, "quantidade": 5},
)
assert created.status_code == 201, created.text
produto_id = created.json()["id"]

assert client.get("/produtos").status_code == 200
assert client.get(f"/produtos/{produto_id}").status_code == 200

updated = client.put(
    f"/produtos/{produto_id}",
    json={"nome": "Teclado mecânico", "preco": 199.9, "quantidade": 3},
)
assert updated.status_code == 200, updated.text
assert updated.json()["nome"] == "Teclado mecânico"

assert client.delete(f"/produtos/{produto_id}").status_code == 204
assert client.get(f"/produtos/{produto_id}").status_code == 404
assert client.get("/produtos/999999").status_code == 404

print("CRUD validado com sucesso.")
