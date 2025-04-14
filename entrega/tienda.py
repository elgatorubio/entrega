from abc import ABC, abstractmethod

# Singleton: Gestor del Catálogo
class CatalogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CatalogManager, cls).__new__(cls)
            cls._instance.products = []
        return cls._instance

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products

# Producto base
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"

# Productos específicos
class Electronic(Product):
    pass

class Clothing(Product):
    pass

# Factory Method
class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name, price):
        pass

class ElectronicFactory(ProductFactory):
    def create_product(self, name, price):
        return Electronic(name, price)

class ClothingFactory(ProductFactory):
    def create_product(self, name, price):
        return Clothing(name, price)

# Strategy: Filtros dinámicos
class FilterStrategy(ABC):
    @abstractmethod
    def apply(self, products):
        pass

class PriceFilter(FilterStrategy):
    def __init__(self, max_price):
        self.max_price = max_price

    def apply(self, products):
        return [p for p in products if p.price <= self.max_price]

class CategoryFilter(FilterStrategy):
    def __init__(self, category):
        self.category = category

    def apply(self, products):
        return [p for p in products if isinstance(p, self.category)]

# Uso de la aplicación
if __name__ == "__main__":
    catalog = CatalogManager()

    electronic_factory = ElectronicFactory()
    clothing_factory = ClothingFactory()

    catalog.add_product(electronic_factory.create_product("Laptop", 1200))
    catalog.add_product(clothing_factory.create_product("T-shirt", 25))
    catalog.add_product(electronic_factory.create_product("Smartphone", 800))

    print("\nTodos los productos:")
    for p in catalog.get_products():
        print(p)

    print("\nProductos con precio menor o igual a 1000:")
    price_filter = PriceFilter(1000)
    for p in price_filter.apply(catalog.get_products()):
        print(p)

    print("\nProductos de la categoría Electrónica:")
    category_filter = CategoryFilter(Electronic)
    for p in category_filter.apply(catalog.get_products()):
        print(p)
