from abc import ABC, abstractmethod

# ---------------------------------------------------------
# Singleton: Gestor del catálogo (una sola instancia global)
# ---------------------------------------------------------
class CatalogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CatalogManager, cls).__new__(cls)
            cls._instance.products = []
        return cls._instance

    # Agregar un producto al catálogo
    def add_product(self, product):
        self.products.append(product)

    # Obtener la lista completa de productos
    def get_products(self):
        return self.products

    # Aplicar una estrategia de filtrado
    def filter_products(self, strategy):
        return strategy.apply(self.products)

# -----------------------------------------------------
# Factory Method: Creación de productos por categoría
# -----------------------------------------------------
class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}: ${self.price}"

# Categoría: Libro
class Book(Product):
    pass

# Categoría: Electrónica
class Electronic(Product):
    pass

# Fábrica de productos según la categoría
class ProductFactory:
    @staticmethod
    def create_product(category, name, price):
        if category == "book":
            return Book(name, price)
        elif category == "electronic":
            return Electronic(name, price)
        else:
            raise ValueError("Categoría desconocida")

# -----------------------------------------------
# Strategy: Filtros dinámicos por precio o clase
# -----------------------------------------------
class FilterStrategy(ABC):
    @abstractmethod
    def apply(self, products):
        pass

# Filtro por precio máximo
class PriceFilter(FilterStrategy):
    def __init__(self, max_price):
        self.max_price = max_price

    def apply(self, products):
        return [p for p in products if p.price <= self.max_price]

# Filtro por categoría (clase del producto)
class CategoryFilter(FilterStrategy):
    def __init__(self, category_type):
        self.category_type = category_type

    def apply(self, products):
        return [p for p in products if isinstance(p, self.category_type)]

# ----------------------
# Programa principal
# ----------------------
if __name__ == "__main__":
    catalog = CatalogManager()

    # Crear productos usando el Factory Method
    p1 = ProductFactory.create_product("book", "El Quijote", 20)
    p2 = ProductFactory.create_product("electronic", "Laptop", 800)
    p3 = ProductFactory.create_product("book", "1984", 15)

    # Agregar productos al catálogo
    catalog.add_product(p1)
    catalog.add_product(p2)
    catalog.add_product(p3)

    # Mostrar todos los productos
    print(" Todos los productos:")
    for p in catalog.get_products():
        print(p)

    # Filtrar por precio
    print("\n Productos con precio <= $100:")
    cheap_filter = PriceFilter(100)
    for p in catalog.filter_products(cheap_filter):
        print(p)

    # Filtrar por categoría Book
    print("\n Productos de categoría 'Book':")
    book_filter = CategoryFilter(Book)
    for p in catalog.filter_products(book_filter):
        print(p)
