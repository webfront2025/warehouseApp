import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function Layout({ children }) {
  return (
    // <div className="flex">
    //   <Sidebar />

    //   <div className="flex-1">
    //     <Navbar />
<div className="min-h-screen bg-gray-200">

<Navbar/>
        <div className="max-w-6xl mx-auto p-6">
            {children}
            </div>
      </div>

  );
}
