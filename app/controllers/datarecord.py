"""Persistência JSON e autenticação, seguindo o padrão do BMVC do professor."""

import json
import os
import uuid
from app.models.user_account import UserAccount
from app.models.produto import Produto

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
USERS_FILE = os.path.join(DB_DIR, "user_accounts.json")
PRODUCTS_FILE = os.path.join(DB_DIR, "produtos.json")


class DataRecord:
    def __init__(self):
        os.makedirs(DB_DIR, exist_ok=True)
        self.__authenticated_users = {}
        self.__user_accounts = []
        self.__products = []
        self.read_users()
        self.read_products()

    # -------------------- Usuários e sessões --------------------
    def read_users(self):
        if not os.path.exists(USERS_FILE):
            # Conta de demonstração para o primeiro acesso local.
            self.__user_accounts = [UserAccount("admin", "aura123")]
            self.save_users()
            return
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.__user_accounts = [UserAccount(**item) for item in data]

    def save_users(self):
        with open(USERS_FILE, "w", encoding="utf-8") as file:
            json.dump([vars(user) for user in self.__user_accounts], file,
                      ensure_ascii=False, indent=4)

    def check_user(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user
                return session_id
        return None

    def get_current_user(self, session_id):
        return self.__authenticated_users.get(session_id)

    def get_username(self, session_id):
        user = self.get_current_user(session_id)
        return user.username if user else None

    def logout(self, session_id):
        self.__authenticated_users.pop(session_id, None)

    # -------------------- Produtos --------------------
    def read_products(self):
        if not os.path.exists(PRODUCTS_FILE):
            self.__products = [
                Produto(1, "Camiseta Essencial", "Camisetas", 59.90, "M", "Azul-claro"),
                Produto(2, "Calça Aurora", "Calças", 129.90, "38", "Jeans"),
                Produto(3, "Vestido Brisa", "Vestidos", 159.90, "P", "Off-white"),
            ]
            self.save_products()
            return
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.__products = [Produto(**item) for item in data]

    def save_products(self):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
            json.dump([product.to_dict() for product in self.__products], file,
                      ensure_ascii=False, indent=4)

    def list_products(self):
        return list(self.__products)

    def get_product(self, product_id):
        for product in self.__products:
            if product.id == product_id:
                return product
        return None

    def create_product(self, data):
        next_id = max((p.id for p in self.__products), default=0) + 1
        product = Produto(next_id, data["nome"], data["categoria"],
                          data["preco"], data["tamanho"], data["cor"])
        self.__products.append(product)
        self.save_products()
        return product

    def update_product(self, product_id, data):
        product = self.get_product(product_id)
        if not product:
            return None
        product.nome = str(data["nome"]).strip()
        product.categoria = str(data["categoria"]).strip()
        product.preco = float(data["preco"])
        product.tamanho = str(data["tamanho"]).strip()
        product.cor = str(data["cor"]).strip()
        self.save_products()
        return product

    def delete_product(self, product_id):
        product = self.get_product(product_id)
        if not product:
            return False
        self.__products = [p for p in self.__products if p.id != product_id]
        self.save_products()
        return True
