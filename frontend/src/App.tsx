import React, { useEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeSanitize from 'rehype-sanitize'

type Msg = { sender: 'Vous' | 'BassetBot'; text: string }
const API_BASE = import.meta.env.VITE_API_BASE || '/api'
function createVisitorId(){ return (crypto && 'randomUUID' in crypto)? crypto.randomUUID(): String(Date.now())+Math.random() }
export default function App(){
  const [visitorId,setVisitorId]=useState(''); const [msgs,setMsgs]=useState<Msg[]>([{sender:'BassetBot',text:"Salut 👋 Je suis le CV interactif de Basset."}]); const [input,setInput]=useState(''); const [loading,setLoading]=useState(false); const endRef=useRef<HTMLDivElement>(null);
  useEffect(()=>{ const id=localStorage.getItem('basset_vid')||createVisitorId(); localStorage.setItem('basset_vid',id); setVisitorId(id)},[])
  useEffect(()=>{ endRef.current?.scrollIntoView({behavior:'smooth'}) },[msgs])
  async function send(){ const q=input.trim(); if(!q||loading) return; setInput(''); setMsgs(m=>[...m,{sender:'Vous',text:q}]); setLoading(true); try{ const r=await fetch(`${API_BASE}/chat`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q,visitor_id:visitorId})}); const j=await r.json(); setMsgs(m=>[...m,{sender:'BassetBot',text:j.reply}]) }catch{ setMsgs(m=>[...m,{sender:'BassetBot',text:'Erreur serveur.'}]) } finally{ setLoading(false) } }
  function onKey(e:React.KeyboardEvent<HTMLTextAreaElement>){ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); send() } }
  return (<div style={{maxWidth:800,margin:'0 auto',padding:16,fontFamily:'system-ui'}}>
    <h1>BassetBot</h1>
    <div style={{display:'flex',flexDirection:'column',gap:12}}>
      {msgs.map((m,i)=>(<div key={i} style={{alignSelf:m.sender==='Vous'?'flex-end':'flex-start',maxWidth:'85%',background:m.sender==='Vous'?'#2b6cb0':'#1a202c',color:'#fff',padding:12,borderRadius:10}}>
        <div style={{fontSize:12,opacity:.8,marginBottom:6}}>{m.sender}</div>
        <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>{m.text}</ReactMarkdown>
      </div>))}
      <div ref={endRef}/>
    </div>
    <div style={{display:'flex',flexDirection:'column',gap:8,marginTop:16}}>
      <textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={onKey} rows={3} style={{width:'100%',padding:10,borderRadius:8,border:'1px solid #ccc'}} placeholder="Écris ta question et appuie sur Entrée"/>
      <div style={{display:'flex',gap:8}}>
        <button onClick={send} disabled={loading} style={{padding:'8px 14px',borderRadius:8,background:'#2b6cb0',color:'#fff',border:'none'}}>{loading?'Envoi…':'Envoyer'}</button>
        <a href='https://github.com/bassetgueddou' target='_blank'>Code source</a>
      </div>
    </div>
  </div>) }
