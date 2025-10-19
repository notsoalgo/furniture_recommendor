import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Send, Sparkles, Loader2 } from "lucide-react";
import ProductCard from "@/components/product-card";

interface Product {
  uniq_id: string;
  title: string;
  price: number;
  brand: string;
  images?: string;
  creative_description: string;
  similarity_score: number;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  products?: Product[];
}

export default function RecommendationPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      type: 'assistant',
      content: "Hi! I'm your AI furniture consultant. Tell me what you're looking for, and I'll help you find the perfect pieces for your space."
    }
  ]);

  const recommendMutation = useMutation({
    mutationFn: async (userQuery: string) => {
      const response = await fetch('http://localhost:8000/recommend/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery, top_k: 8 })
      });
      
      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }
      
      return response.json();
    },
    onSuccess: (data, userQuery) => {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          type: 'assistant',
          content: `I found ${data.count} great options for "${userQuery}". Here are my top recommendations:`,
          products: data.products
        }
      ]);
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: query
    };
    
    setMessages(prev => [...prev, userMessage]);
    recommendMutation.mutate(query);
    setQuery("");
  };

  const suggestedPrompts = [
    "Modern sofa for small living room",
    "Ergonomic office chair under $500",
    "Rustic dining table for 6 people",
    "Minimalist bedroom furniture set"
  ];

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-semibold tracking-tight">AI Furniture Finder</h1>
              <p className="text-sm text-muted-foreground">Powered by semantic search & AI</p>
            </div>
          </div>
        </div>
      </header>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-2xl ${message.type === 'user' ? 'w-auto' : 'w-full'}`}>
                {message.type === 'user' ? (
                  <div className="bg-primary text-primary-foreground rounded-2xl rounded-br-sm px-4 py-3">
                    <p className="text-base leading-relaxed">{message.content}</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Card className="border bg-card rounded-2xl rounded-bl-sm px-4 py-3">
                      <p className="text-base leading-relaxed text-foreground">{message.content}</p>
                    </Card>
                    
                    {message.products && message.products.length > 0 && (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
                        {message.products.map((product) => (
                          <ProductCard key={product.uniq_id} product={product} />
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {recommendMutation.isPending && (
            <div className="flex justify-start">
              <Card className="border bg-card rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-3">
                <Loader2 className="w-4 h-4 animate-spin text-primary" />
                <p className="text-base text-muted-foreground">Finding the perfect furniture for you...</p>
              </Card>
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t bg-background">
        <div className="max-w-4xl mx-auto px-4 py-4">
          {messages.length === 1 && (
            <div className="mb-4">
              <p className="text-sm text-muted-foreground mb-2">Try these prompts:</p>
              <div className="flex flex-wrap gap-2">
                {suggestedPrompts.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuery(prompt)}
                    className="px-3 py-1.5 text-sm rounded-full border bg-card hover-elevate active-elevate-2 transition-all"
                    data-testid={`button-prompt-${idx}`}
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe the furniture you're looking for..."
              className="resize-none min-h-[60px] text-base"
              data-testid="input-query"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <Button
              type="submit"
              size="icon"
              className="h-[60px] w-[60px] rounded-full"
              disabled={!query.trim() || recommendMutation.isPending}
              data-testid="button-send"
            >
              <Send className="w-5 h-5" />
            </Button>
          </form>
          
          <p className="text-xs text-muted-foreground mt-2 text-center">
            Press Enter to send • Shift + Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
}
