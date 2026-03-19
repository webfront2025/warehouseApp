from fastapi import APIRouter
from app.database.database import get_connection

router = APIRouter(prefix="/products")

@router.get("/")
def get_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    return [dict(p) for p in products]


@router.post("/")
def add_product(product: dict):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
        (
            product["name"],
            product["category"],
            product["price"],
            product["quantity"],
        ),
    )

    conn.commit()

    return {"message": "product added"}


@router.put("/{product_id}")
def update_product(product_id: int, product: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE products SET name = ?, category = ?, price = ?, quantity = ? WHERE id = ?",
        (
            product["name"],
            product["category"],
            product["price"],
            product["quantity"],
            product_id,
        ),
    )

    conn.commit()

    return {"message": "product updated"}


@router.delete("/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()

    return {"message": "product deleted"}