import { useState, useEffect } from "react";

export default function EditProductForm({ product, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    quantity: "",
    price: "",
    location: "",
    category: "",
    supplier: ""
  });

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || "",
        description: product.description || "",
        quantity: product.quantity?.toString() || "",
        price: product.price?.toString() || "",
        location: product.location || "",
        category: product.category || "",
        supplier: product.supplier || ""
      });
    }
  }, [product]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const productData = {
      name: formData.name,
      description: formData.description,
      quantity: parseInt(formData.quantity),
      price: parseFloat(formData.price),
      location: formData.location,
      category: formData.category,
      supplier: formData.supplier
    };

    onSubmit(productData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-h-[70vh] overflow-y-auto px-2">
      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Produktnavn
        </label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          placeholder="Indtast produktnavn"
        />
      </div>

      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Beskrivelse
        </label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows="3"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm resize-none"
          placeholder="Indtast beskrivelse"
        />
      </div>

      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Antal
        </label>
        <input
          type="number"
          name="quantity"
          value={formData.quantity}
          onChange={handleChange}
          required
          min="0"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          placeholder="0"
        />
      </div>

      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Pris
        </label>
        <input
          type="number"
          name="price"
          value={formData.price}
          onChange={handleChange}
          required
          min="0"
          step="0.01"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          placeholder="0.00"
        />
      </div>

      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Lokation
        </label>
        <input
          type="text"
          name="location"
          value={formData.location}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          placeholder="Indtast lokation"
        />
      </div>

      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Kategori
        </label>
        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        >
          <option value="">Vælg kategori</option>
          <option value="Elektronik">Elektronik</option>
          <option value="Tøj">Tøj</option>
          <option value="Fødevarer">Fødevarer</option>
          <option value="Møbler">Møbler</option>
          <option value="Bøger">Bøger</option>
          <option value="Sport">Sport</option>
          <option value="Andet">Andet</option>
        </select>
      </div>

      <div className="min-w-0">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Leverandør
        </label>
        <input
          type="text"
          name="supplier"
          value={formData.supplier}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          placeholder="Indtast leverandør"
        />
      </div>

      <div className="flex gap-2 pt-4 sticky bottom-0 bg-white pb-2 border-t border-gray-200">
        <button
          type="submit"
          className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 transition duration-200 text-sm font-medium min-w-0"
        >
          Gem
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 bg-gray-300 text-gray-700 py-3 px-4 rounded-md hover:bg-gray-400 transition duration-200 text-sm font-medium min-w-0"
        >
          Annuller
        </button>
      </div>
    </form>
  );
}
