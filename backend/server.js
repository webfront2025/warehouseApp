const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const db = new sqlite3.Database("./database.db");

// Create table
db.run(`
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  description TEXT,
  quantity INTEGER,
  price REAL,
  location TEXT,
  category TEXT,
  supplier TEXT
)
`);
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  // Simple login (for testing)
  if (username === "admin" && password === "1234") {
    return res.json({ token: "fake-token-123" });
  }

  res.status(401).json({ error: "Invalid credentials" });
});
// ADD PRODUCT
app.post("/products", (req, res) => {
  const { name, description, quantity, price, location, category, supplier } = req.body;

  const sql = `
    INSERT INTO products (name, description, quantity, price, location, category, supplier)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `;

  db.run(sql, [name, description, quantity, price, location, category, supplier], function (err) {
    if (err) {
      console.log(err);
      return res.status(500).json({ error: err });
    }

    res.json({ id: this.lastID, ...req.body });
  });
});

// GET PRODUCTS
app.get("/products", (req, res) => {
  db.all("SELECT * FROM products", [], (err, rows) => {
    if (err) return res.status(500).json(err);
    res.json(rows);
  });
});

app.listen(5000, () => console.log("Server running on port 5000"));