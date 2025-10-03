import { useState, useRef, useEffect } from 'react'
import { Send, Pill, Trash2, Search, Loader2 } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { chatApi, type Message, type Source } from '@/lib/api'
import { cn, formatTimestamp } from '@/lib/utils'
import ReactMarkdown from 'react-markdown'

interface ChatMessage extends Message {
  sources?: Source[]
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string>()
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await chatApi.sendMessage(
        input,
        messages,
        sessionId
      )

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        sources: response.sources,
      }

      setMessages((prev) => [...prev, assistantMessage])
      setSessionId(response.session_id)
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: "Désolé, une erreur s'est produite. Veuillez réessayer.",
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearChat = async () => {
    if (sessionId) {
      try {
        await chatApi.clearSession(sessionId)
      } catch (error) {
        console.error('Error clearing session:', error)
      }
    }
    setMessages([])
    setSessionId(undefined)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-primary rounded-lg p-2">
              <Pill className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">PharmaBot</h1>
              <p className="text-sm text-gray-500">Assistant professionnel - Vidal & Meddispar</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Link to="/search">
              <Button variant="outline" size="sm">
                <Search className="w-4 h-4 mr-2" />
                Recherche
              </Button>
            </Link>
            {messages.length > 0 && (
              <Button variant="outline" size="sm" onClick={handleClearChat}>
                <Trash2 className="w-4 h-4 mr-2" />
                Effacer
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="flex-1 overflow-hidden">
        <div className="max-w-4xl mx-auto h-full flex flex-col p-4">
          <ScrollArea className="flex-1 pr-4">
            <div ref={scrollRef} className="space-y-4">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center py-12">
                  <div className="bg-primary/10 rounded-full p-6 mb-4">
                    <Pill className="w-12 h-12 text-primary" />
                  </div>
                  <h2 className="text-2xl font-semibold mb-2">
                    Assistant pour Pharmaciens
                  </h2>
                  <p className="text-gray-600 max-w-md mb-2">
                    Outil professionnel d'aide à la recherche de médicaments et informations pharmaceutiques.
                  </p>
                  <p className="text-sm text-gray-500 max-w-md">
                    Basé exclusivement sur les sources officielles Vidal et Meddispar
                  </p>
                  <div className="mt-6 grid grid-cols-1 gap-3 max-w-2xl w-full">
                    {[
                      'Quelles sont les indications du paracétamol ?',
                      'Interactions médicamenteuses de l\'aspirine',
                      'Posologie de l\'amoxicilline chez l\'adulte',
                    ].map((example, i) => (
                      <Card
                        key={i}
                        className="p-3 cursor-pointer hover:bg-gray-50 transition-colors"
                        onClick={() => setInput(example)}
                      >
                        <p className="text-sm text-gray-700">{example}</p>
                      </Card>
                    ))}
                  </div>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div
                    key={index}
                    className={cn(
                      'flex',
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    )}
                  >
                    <div
                      className={cn(
                        'max-w-[80%] rounded-lg px-4 py-3',
                        message.role === 'user'
                          ? 'bg-primary text-white'
                          : 'bg-white border shadow-sm'
                      )}
                    >
                      <div className="prose prose-sm max-w-none">
                        {message.role === 'assistant' ? (
                          <ReactMarkdown>{message.content}</ReactMarkdown>
                        ) : (
                          <p>{message.content}</p>
                        )}
                      </div>
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-3 pt-3 border-t space-y-2">
                          <p className="text-xs font-semibold text-gray-500">
                            Sources :
                          </p>
                          {message.sources.map((source, i) => (
                            <a
                              key={i}
                              href={source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="block"
                            >
                              <Card className="p-2 hover:bg-gray-50 transition-colors">
                                <div className="flex items-start justify-between gap-2">
                                  <div className="flex-1 min-w-0">
                                    <p className="text-xs font-medium truncate">
                                      {source.title}
                                    </p>
                                    <p className="text-xs text-gray-500 line-clamp-2 mt-1">
                                      {source.content}
                                    </p>
                                  </div>
                                  <Badge variant="outline" className="shrink-0">
                                    {source.source_type}
                                  </Badge>
                                </div>
                              </Card>
                            </a>
                          ))}
                        </div>
                      )}
                      {message.timestamp && (
                        <p className="text-xs mt-2 opacity-70">
                          {formatTimestamp(message.timestamp)}
                        </p>
                      )}
                    </div>
                  </div>
                ))
              )}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white border shadow-sm rounded-lg px-4 py-3">
                    <Loader2 className="w-5 h-5 animate-spin text-primary" />
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          {/* Input Area */}
          <div className="mt-4 bg-white border rounded-lg shadow-sm p-4">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Posez votre question pharmaceutique..."
                className="flex-1"
                disabled={isLoading}
              />
              <Button
                onClick={handleSendMessage}
                disabled={isLoading || !input.trim()}
                size="icon"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </Button>
            </div>
            <p className="text-[10px] text-gray-400 mt-2 leading-tight">
              ⚠️ <span className="font-semibold">Important</span> - Avertissement Légal: Cet assistant est un outil d'aide à la décision pour professionnels de santé. Il ne remplace pas l'expertise d'un pharmacien diplômé. Toujours vérifier les informations critiques dans les sources officielles.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
