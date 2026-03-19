import { useState, useEffect } from "react";
import { API } from "../api/api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [products, setProducts] = useState([]);
  const [searchField, setSearchField] = useState("Navn");
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem("token");
    if (token) {
      setIsLoggedIn(true);
      fetchProducts();
    }
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await API.get("/products");
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await API.post("/login", {
        username,
        password,
      });

      localStorage.setItem("token", res.data.token);
      setIsLoggedIn(true);
      alert("Login successful!");
      fetchProducts(); // Load products after login
    } catch {
      alert("Invalid login");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setUsername("");
    setPassword("");
    setProducts([]);
  };

  const handleEdit = async (productId) => {
    const newName = prompt("Enter new name:");
    if (!newName) return;
    
    const newPrice = prompt("Enter new price:");
    if (!newPrice) return;
    
    const newQuantity = prompt("Enter new quantity:");
    if (!newQuantity) return;

    try {
      await API.put(`/products/${productId}`, {
        name: newName,
        category: "general",
        price: parseFloat(newPrice),
        quantity: parseInt(newQuantity)
      });
      fetchProducts(); // Refresh the product list
      alert("Product updated successfully!");
    } catch (error) {
      console.error("Error updating product:", error);
      alert("Error updating product");
    }
  };

  const handleDelete = async (productId) => {
    if (!window.confirm("Are you sure you want to delete this product?")) {
      return;
    }

    try {
      await API.delete(`/products/${productId}`);
      fetchProducts(); // Refresh the product list
      alert("Product deleted successfully!");
    } catch (error) {
      console.error("Error deleting product:", error);
      alert("Error deleting product");
    }
  };

  const filteredProducts = products.filter(product => {
    if (!searchValue) return true;
    
    const fieldMap = {
      'ID': 'id',
      'Navn': 'name', 
      'Beskrivelse': 'description',
      'Antal': 'quantity',
      'Pris': 'price'
    };
    
    const field = fieldMap[searchField] || 'name';
    const value = product[field]?.toString().toLowerCase() || '';
    return value.includes(searchValue.toLowerCase());
  });

  // If not logged in, show login form
  if (!isLoggedIn) {
    return (
      <div className="w-full max-w-4xl">
        <h2 className="inline-block bg-gray-200 px-6 pt-3 rounded-t-xl font-bold text-2xl">
          Login
        </h2>
        <div className="bg-gray-200 rounded-2xl rounded-tl-none p-8 mb-10">
          <form
            onSubmit={handleSubmit}
            className="flex flex-wrap items-end gap-6"
          >
            <div className="flex-grow min-w-[200px]">
              <label for="uname" className="block text-sm font-medium mb-1">
                Username:
              </label>
              <input
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full h-10 rounded-full border-none px-4 shadow-inner"
                required
              />
            </div>
            <div className="flex-grow min-w-[200px]">
              <label for="password" className="block text-sm font-medium mb-1">
                Password:
              </label>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full h-10 rounded-full border-none px-4 shadow-inner"
                required
              />
            </div>
            <button
              className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-2 rounded-full font-medium transition-colors"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  // If logged in, show product table with logout

  return (
    <div className="w-full max-w-6xl">
      {/* Header with logout - ALWAYS visible when logged in */}
      <div className="flex justify-between items-center mb-6 bg-gray-100 p-4 rounded-lg">
        <h2 className="text-xl font-bold text-gray-800">
          Product Inventory
        </h2>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-full font-medium transition-colors shadow-lg"
        >
          🚪 Logout
        </button>
      </div>

      {/* Products Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 sm:p-6 border-b border-gray-200">
          <h2 className="text-lg sm:text-xl font-bold text-gray-900 mb-4">Produkter</h2>
          
          {/* Search */}
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
            <select
              value={searchField}
              onChange={(e) => setSearchField(e.target.value)}
              className="w-full sm:w-auto px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            >
              <option value="ID">ID</option>
              <option value="Navn">Navn</option>
              <option value="Beskrivelse">Beskrivelse</option>
              <option value="Antal">Antal</option>
              <option value="Pris">Pris</option>
            </select>
            
            <input
              type="text"
              placeholder="Søg efter..."
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px]">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Navn</th>
                <th className="hidden sm:table-cell px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Beskrivelse</th>
                <th className="px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Antal</th>
                <th className="px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pris</th>
                <th className="px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Handlinger</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredProducts.map((product) => (
                <tr key={product.id}>
                  <td className="px-4 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-900">{product.id}</td>
                  <td className="px-4 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-900">{product.name}</td>
                  <td className="hidden sm:table-cell px-4 sm:px-6 py-4 text-sm text-gray-900">{product.description || '-'}</td>
                  <td className="px-4 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-900">{product.quantity}</td>
                  <td className="px-4 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-900">kr. {product.price}</td>
                  <td className="px-4 sm:px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button 
                      onClick={() => handleEdit(product.id)}
                      className="text-green-600 hover:text-green-900 mr-2 sm:mr-3"
                    >
                      ✓
                    </button>
                    <button 
                      onClick={() => handleDelete(product.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      ✗
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
