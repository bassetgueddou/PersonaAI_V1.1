import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function App() {
  const [messages, setMessages] = useState([{ role: 'assistant', content: '⚡ Bienvenue ! Posez-moi vos questions.' }])
  const [input, setInput] = useState('')
  const [dark, setDark] = useState(true)

  const sendMessage = async () => {
    if (!input.trim()) return
    const newMessages = [...messages, { role: 'user', content: input }]
    setMessages(newMessages)
    setInput('')
    try {
      const res = await fetch(`${__API_BASE__}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages })
      })
      const data = await res.json()
      setMessages([...newMessages, { role: 'assistant', content: data.reply || '...' }])
    } catch (e) {
      setMessages([...newMessages, { role: 'assistant', content: '❌ Erreur API' }])
    }
  }

  return (
    <div className={dark ? 'dark' : ''}>
      <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
        <header className="p-4 font-bold text-xl bg-white dark:bg-gray-800 shadow flex justify-between">
          PersonaAI
          <button onClick={() => setDark(!dark)} className="px-2 py-1 border rounded">
            {dark ? '☀️' : '🌙'}
          </button>
        </header>
        <main className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`p-3 rounded-lg max-w-xl prose prose-invert dark:prose-invert ${
                m.role === 'user' ? 'bg-emerald-600 text-white' : 'bg-gray-200 dark:bg-gray-700'
              }`}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
              </div>
            </div>
          ))}
        </main>
        <footer className="p-4 bg-white dark:bg-gray-800 flex space-x-2">
          <input
            className="flex-1 border rounded px-3 py-2 dark:bg-gray-700"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Écrivez un message..."
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage} className="px-4 py-2 bg-emerald-600 text-white rounded">
            Envoyer
          </button>
        </footer>
      </div>
    </div>
  )
}
