"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Copy } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Home() {
  const [category, setCategory] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ category }),
      });

      if (!response.ok) throw new Error("Failed to generate vocabulary");

      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error("Error:", error);
      toast({
        title: "Error",
        description: "Failed to generate vocabulary. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(result);
    toast({
      title: "Copied!",
      description: "The vocabulary list has been copied to your clipboard.",
    });
  };

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Vocabulary Generator</h1>
          <p className="text-muted-foreground">
            Enter a category to generate vocabulary in Spanish and Arabic
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Input
              placeholder="Enter category (e.g., Basic Greetings, Food, Colors)"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full"
            />
          </div>
          <Button type="submit" disabled={loading || !category}>
            {loading ? "Generating..." : "Generate Vocabulary"}
          </Button>
        </form>

        {result && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Generated Vocabulary</h2>
              <Button variant="outline" size="sm" onClick={handleCopy}>
                <Copy className="h-4 w-4 mr-2" />
                Copy
              </Button>
            </div>
            <Textarea
              value={result}
              readOnly
              className="h-[400px] font-mono"
            />
          </div>
        )}
      </div>
    </div>
  );
}