export default function Navbar(){
const logout = ()=>{
localStorage.removeItem("token")
window.location="/"
}
return(

// <div className="bg-white shadow px-6 py-8 mt-20 flex justify-between items-center">

// <h1 className="text-xl font-bold">
// StockFlow Dashboard
// </h1>

// <button className="bg-red-500 text-white px-4 py-2 rounded">
// Logout
// </button>

// </div>


<div className="bg-gray-800 text-white px-8 py-4 flex justify-between">

<h1 className="text-xl font-bold">
StockFlow
</h1>

<div className="flex gap-4 items-center">

<span>Hi ADMIN</span>

<button
onClick={logout}
className="bg-white text-black px-3 py-1 rounded"
>
Log ud
</button>

</div>

</div>

)

}