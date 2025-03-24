import { useState } from "react";
import axios from "axios";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { sender: "user", text: input };
    setMessages([...messages, userMsg]);

    try {
      const response = await axios.post("http://localhost:8000/chat", { message: input });
      const botMsg = { sender: "bot", text: response.data.reply };
      setMessages([...messages, userMsg, botMsg]);
    } catch (error) {
      setMessages([...messages, userMsg, { sender: "bot", text: "Error connecting to AI" }]);
    }
    setInput("");
  };

  return (
    <div style={{ width: "400px", margin: "auto", border: "1px solid black", padding: "10px" }}>
      <h2>AI Assistant</h2>
      <div style={{ height: "300px", overflowY: "scroll", borderBottom: "1px solid black" }}>
        {messages.map((msg, index) => (
          <p key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
            <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong> {msg.text}
          </p>
        ))}
      </div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        placeholder="Ask something..."
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbot;
