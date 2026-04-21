import { useState, useEffect } from "react";
import { API } from "../api/api";
import ProductTable from "../components/ProductTable";
import AddProductForm from "../components/AddProductForm";
import EditProductForm from "../components/EditProductForm";

export default function Dashboard({ setIsLoggedIn }) {
  const [products, setProducts] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [selectedProductId, setSelectedProductId] = useState(null);
  const [editingProduct, setEditingProduct] = useState(null);
  const [searchField, setSearchField] = useState("Navn");
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await API.get("/products");
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handleAddProduct = async (productData) => {
    try {
      await API.post("/products", productData);
      fetchProducts();
      setShowAddForm(false);
    } catch (error) {
      console.error("Error adding product:", error);
      alert("Fejl ved tilføjelse af produkt");
    }
  };

  const handleLogout = () => {
  localStorage.removeItem("token");
  setIsLoggedIn(false);
};
  const handleEditProduct = async (productData) => {
    try {
      await API.put(`/products/${editingProduct.id}`, productData);
      fetchProducts();
      setShowEditForm(false);
      setEditingProduct(null);
    } catch (error) {
      console.error("Error updating product:", error);
      alert("Fejl ved opdatering af produkt");
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (window.confirm("Er du sikker på, du vil slette dette produkt?")) {
      try {
        await API.delete(`/products/${productId}`);
        fetchProducts();
      } catch (error) {
        console.error("Error deleting product:", error);
        alert("Fejl ved sletning af produkt");
      }
    }
  };

  const openEditForm = (product) => {
    setEditingProduct(product);
    setShowEditForm(true);
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

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">StockFlow</h1>
            {/* <div className="text-sm text-gray-600">Logget ind - Produkter</div>  20-04-2026   */}
            <div className="flex items-center gap-4">
  <span className="text-sm text-gray-600">Logget ind</span>
  <button
    onClick={handleLogout}
    className="bg-red-500 text-white px-3 py-1 rounded  hover:bg-red-600 transition"
  >
    Logout
  </button>
</div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Action Buttons */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => setShowAddForm(true)}
            className="w-full sm:w-auto bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition duration-200"
          >
            Tilføj Produkt
          </button>
          <div className="flex gap-2">
            <select
              value={selectedProductId || ""}
              onChange={(e) => setSelectedProductId(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Vælg produkt at redigere</option>
              {filteredProducts.map((product) => (
                <option key={product.id} value={product.id}>
                  {product.name}
                </option>
              ))}
            </select>
            <button
              onClick={() => {
                if (selectedProductId) {
                  const product = products.find(p => p.id === parseInt(selectedProductId));
                  if (product) {
                    openEditForm(product);
                  }
                } else {
                  alert("Vælg venligst et produkt at redigere");
                }
              }}
              className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition duration-200"
            >
              Rediger
            </button>
          </div>
        </div>

        {/* Search */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          <div className="flex gap-4">
            <select
              value={searchField}
              onChange={(e) => setSearchField(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Products Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="overflow-x-auto">
            <table className="min-w-[600px] w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Navn</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Antal</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pris</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Handlinger</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredProducts.map((product) => (
                  <tr key={product.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{product.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{product.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{product.quantity}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">kr. {product.price}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button 
                        onClick={() => openEditForm(product)}
                        className="text-green-600 hover:text-green-900 mr-3"
                      >
                        ✓
                      </button>
                      <button 
                        onClick={() => handleDeleteProduct(product.id)}
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

      {/* Add Product Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md h-full sm:h-auto max-h-[90vh] flex flex-col">
            <div className="p-6 border-b border-gray-200 flex-shrink-0">
              <h2 className="text-xl font-bold text-gray-900">Tilføj Produkt</h2>
            </div>
            <div className="flex-1 overflow-hidden">
              <AddProductForm 
                onSubmit={handleAddProduct}
                onCancel={() => setShowAddForm(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Edit Product Modal */}
      {showEditForm && editingProduct && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md max-h-[90vh] flex flex-col">
            <div className="p-6 border-b border-gray-200 flex-shrink-0">
              <h2 className="text-xl font-bold text-gray-900">Rediger Produkt</h2>
            </div>
            <div className="flex-1 overflow-hidden">
              <EditProductForm 
                product={editingProduct}
                onSubmit={handleEditProduct}
                onCancel={() => {
                  setShowEditForm(false);
                  setEditingProduct(null);
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
