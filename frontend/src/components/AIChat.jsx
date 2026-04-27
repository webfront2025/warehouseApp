import { useState } from "react";

export default function AIChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(true); //  close function
  const [isMinimized, setIsMinimized] = useState(false);  // minimize function


  const sendMessage = async () => {
    if (!input.trim()) return;
    const currentInput = input;
    setMessages(prev => [...prev, { role: "user", content: currentInput }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: currentInput })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "ai", content: data.reply }]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return (
    <button 
      onClick={() => setIsOpen(true)}
      className="fixed bottom-5 right-5 bg-blue-600 text-white p-3 rounded-full shadow-lg z-50"
    >
       Chat
    </button>
  );

  return (
   <div className="fixed bottom-5 right-5 z-50 w-80 shadow-2xl border border-gray-300 rounded-lg overflow-hidden bg-white">
      {/* Header & Buttons */}
      <div className="bg-blue-600 p-2 text-white flex justify-between items-center">
        <span className="font-bold text-sm ml-2">AI Assistant</span>
        <div className="flex gap-2">
          <button onClick={() => setIsMinimized(!isMinimized)} className="hover:text-gray-300 font-bold px-1">
            {isMinimized ? "□" : "—"}
          </button>
          <button onClick={() => setIsOpen(false)} className="hover:text-red-300 font-bold px-1">
            ✕
          </button>
        </div>
      </div>

{!isMinimized && (
        <>
          <div className="h-64 overflow-y-auto p-3 bg-gray-50 space-y-2">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <span className={`p-2 rounded-lg text-sm max-w-[85%] ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
                  {msg.content}
                </span>
              </div>
            ))}
            {loading && <div className="text-xs text-gray-400">Tænker...</div>}
          </div>
          <div className="p-2 flex gap-1 border-t">
            <input 
              className="flex-1 p-2 text-sm border rounded" 
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Skriv her..."
            />
            <button onClick={sendMessage} className="bg-blue-600 text-white px-3 py-1 rounded text-sm">Send</button>
          </div>
        </>
      )}
    </div>
  );
}