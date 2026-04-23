"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { 
  FileText, 
  Video, 
  Music, 
  Upload, 
  MessageSquare, 
  Plus, 
  Search, 
  Settings,
  MoreVertical,
  Play,
  Send,
  Loader2
} from "lucide-react"
import { UploadDialog } from "@/components/upload-dialog"
import { chatApi, mediaApi } from "@/lib/api"

export default function Dashboard() {
  const [files, setFiles] = useState<any[]>([])
  const [selectedFile, setSelectedFile] = useState<any>(null)
  const [isUploadOpen, setIsUploadOpen] = useState(false)
  const [messages, setMessages] = useState<any[]>([])
  const [input, setInput] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)
  const [timestamps, setTimestamps] = useState<any[]>([])
  
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleUploadSuccess = (newFile: any) => {
    setFiles(prev => [...prev, newFile])
    setSelectedFile(newFile)
    fetchTimestamps(newFile.id)
  }

  const fetchTimestamps = async (fileId: string) => {
    try {
      const response = await mediaApi.getTimestamps(fileId)
      setTimestamps(response.data)
    } catch (err) {
      console.error("Failed to fetch timestamps", err)
    }
  }

  const handleSendMessage = async () => {
    if (!input.trim() || isStreaming) return
    
    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput("")
    setIsStreaming(true)

    let currentResponse = ""
    const assistantMsgIndex = messages.length + 1
    
    setMessages(prev => [...prev, { role: 'assistant', content: "" }])

    const closeStream = chatApi.streamChat(input, "user-123", (token) => {
      currentResponse += token
      setMessages(prev => {
        const newMessages = [...prev]
        newMessages[assistantMsgIndex] = { role: 'assistant', content: currentResponse }
        return newMessages
      })
    })

    // In a real implementation, the stream would close automatically on completion
    // This is simplified for the demo
    setTimeout(() => {
      setIsStreaming(false)
    }, 2000)
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar - File Explorer */}
      <aside className="w-80 border-r border-secondary flex flex-col glass-morphism">
        <div className="p-6 border-b border-secondary">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <span className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">QA</span>
            Multimedia AI
          </h1>
        </div>
        
        <div className="p-4 flex-1 overflow-y-auto space-y-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Your Files</h2>
            <button 
              onClick={() => setIsUploadOpen(true)}
              className="p-1 hover:bg-secondary rounded-full transition-colors"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>
          
          <div className="space-y-1">
            {files.map(file => (
              <FileItem 
                key={file.id} 
                icon={file.contentType === "application/pdf" ? <FileText className="w-4 h-4" /> : <Video className="w-4 h-4" />} 
                name={file.originalFileName} 
                isActive={selectedFile?.id === file.id}
                onClick={() => {
                  setSelectedFile(file)
                  fetchTimestamps(file.id)
                }}
              />
            ))}
            {files.length === 0 && (
              <p className="text-xs text-center text-muted-foreground py-8">No files uploaded yet.</p>
            )}
          </div>
        </div>

        <div className="p-4 border-t border-secondary">
          <button 
            onClick={() => setIsUploadOpen(true)}
            className="w-full flex items-center gap-2 px-4 py-3 bg-primary text-white rounded-xl font-medium hover:bg-primary/90 transition-all shadow-lg shadow-primary/20"
          >
            <Upload className="w-4 h-4" />
            Upload New File
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 bg-[url('/grid.svg')] bg-center bg-fixed">
        {/* Header */}
        <header className="h-16 border-b border-secondary flex items-center justify-between px-6 glass-morphism z-10">
          <div className="flex items-center gap-3">
            {selectedFile && (
              <>
                <div className="w-8 h-8 bg-secondary rounded-lg flex items-center justify-center text-primary">
                  {selectedFile.contentType === "application/pdf" ? <FileText className="w-4 h-4" /> : <Video className="w-4 h-4" />}
                </div>
                <div>
                  <h2 className="text-sm font-semibold truncate max-w-[200px]">{selectedFile.originalFileName}</h2>
                  <p className="text-xs text-muted-foreground">Ready for Q&A</p>
                </div>
              </>
            )}
            {!selectedFile && <h2 className="text-sm font-semibold">Select a file to start</h2>}
          </div>
          
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-secondary rounded-full transition-colors">
              <Settings className="w-4 h-4 text-muted-foreground" />
            </button>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-hidden flex flex-col p-6">
          <div className="flex-1 overflow-y-auto space-y-6 mb-4 scrollbar-hide pr-2">
             {messages.map((msg, idx) => (
               <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                 <div className={`max-w-[80%] p-4 rounded-2xl shadow-sm ${
                   msg.role === 'user' 
                   ? 'bg-primary text-white rounded-tr-none' 
                   : 'glass-morphism rounded-tl-none border border-secondary'
                 }`}>
                   <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                   {msg.content === "" && <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />}
                 </div>
               </div>
             ))}
             <div ref={chatEndRef} />
          </div>

          {/* Input Area */}
          <div className={`max-w-4xl mx-auto w-full glass-morphism p-2 rounded-2xl shadow-xl flex items-end gap-2 border border-secondary transition-all ${!selectedFile ? 'opacity-50 pointer-events-none' : ''}`}>
            <textarea 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSendMessage()
                }
              }}
              placeholder={selectedFile ? "Ask anything about this document..." : "Select a file first"}
              className="flex-1 bg-transparent border-none focus:ring-0 p-3 text-sm min-h-[44px] max-h-32 outline-none resize-none"
              rows={1}
            />
            <button 
              disabled={isStreaming || !input.trim()}
              onClick={handleSendMessage}
              className="bg-primary text-white p-3 rounded-xl hover:bg-primary/90 transition-all disabled:opacity-50"
            >
              {isStreaming ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </main>

      {/* Right Panel - Summary & Metadata */}
      <aside className="w-96 border-l border-secondary flex flex-col glass-morphism overflow-y-auto">
        <div className="p-6 space-y-8">
          <div>
            <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-widest mb-4">Summary</h3>
            <div className="p-4 bg-primary/5 rounded-2xl border border-primary/10">
              <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                {selectedFile?.summary || "Summary will appear here after processing..."}
              </p>
            </div>
          </div>
          
          <div>
            <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-widest mb-4">Topics & Timestamps</h3>
            <div className="space-y-3">
              {timestamps.map((ts, idx) => (
                <TimestampItem key={idx} time={formatTime(ts.timestampSeconds)} label={ts.topic} />
              ))}
              {timestamps.length === 0 && (
                <div className="text-center py-12 border-2 border-dashed border-secondary rounded-2xl">
                  <Play className="w-8 h-8 text-muted-foreground/30 mx-auto mb-2" />
                  <p className="text-xs text-muted-foreground">No timestamps found</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </aside>

      <AnimatePresence>
        {isUploadOpen && (
          <UploadDialog 
            onClose={() => setIsUploadOpen(false)} 
            onUploadSuccess={handleUploadSuccess}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function FileItem({ icon, name, isActive = false, onClick }: { icon: React.ReactNode, name: string, isActive?: boolean, onClick: () => void }) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl transition-all ${isActive ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'hover:bg-secondary/50 text-muted-foreground'}`}
    >
      {icon}
      <span className="text-sm font-medium truncate">{name}</span>
      <MoreVertical className="w-4 h-4 ml-auto opacity-50" />
    </button>
  )
}

function TimestampItem({ time, label }: { time: string, label: string }) {
  return (
    <button className="w-full group flex flex-col gap-2 p-4 rounded-2xl border border-secondary hover:border-primary/50 hover:bg-primary/5 transition-all text-left">
      <div className="flex items-center justify-between">
        <div className="px-2 py-1 bg-primary/10 rounded-md text-[10px] font-mono font-bold text-primary">
          {time}
        </div>
        <Play className="w-3 h-3 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
      <span className="text-sm font-semibold truncate leading-tight">{label}</span>
    </button>
  )
}
