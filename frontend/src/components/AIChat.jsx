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

  // clear input immediately
 setInput(() => "");

  // show user message
  setMessages(prev => [
    ...prev,
    { role: "user", content: currentInput }
  ]);

  setLoading(true);

  try {
    const res = await fetch("http://localhost:8000/api/ai/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: currentInput
      })
    });

    const data = await res.json();

    setMessages(prev => [
      ...prev,
      { role: "ai", content: data.reply || "No reply" }
    ]);

  } catch (error) {
    setMessages(prev => [
      ...prev,
      { role: "ai", content: "Server error" }
    ]);
  } finally {
    setLoading(false);
  }
};
  if (!isOpen) return (
    <button onClick={() => setIsOpen(true)}
      className="fixed bottom-5 right-5 bg-blue-600 text-white p-3 rounded-full shadow-lg z-50">
       Chat</button>
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
        <div className="flex flex-col">
          <div className="h-60 overflow-y-auto p-3 bg-gray-50">
             {messages.map((msg, index) => (
              <div key={index}
                   className={`p-2 rounded text-sm max-w-[80%] ${
                    msg.role === "user"
                        ? "bg-blue-500 text-white ml-auto"
                        : "bg-gray-200 text-black mr-auto"
      }`}
    >
      {msg.content}
    </div>
  ))}

  {loading && (
    <div className="text-gray-500 text-sm">
      Thinking...
    </div>
  )}
</div>
          <div className="p-2 border-t flex">
            <input key={messages.length}  value={input} 
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1 border p-1 text-sm rounded" 
              placeholder="Enter message..." />
            <button onClick={sendMessage} className="bg-blue-600 text-white px-3 py-1 rounded text-sm">Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
