'use client'
import { useEffect, useState } from 'react'

type Item = {
  id: number
  name: string
}

export default function Home() {// frontend/src/pages/index.tsx

    type InterpretResult = { action: string; amount: number; currency: string; recipient: string };

    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [resultTranscribe, setResultTranscribe] = useState<string | null>(null);
    const [resultInterpret, setResultInterpret] = useState<InterpretResult | null>(null);
    const [resultInterpretError, setResultInterpretError] = useState<string | null>(null);
    const [resultTransaction, setResultTransaction] = useState<string | null>(null);
    const [resultTransactionError, setResultTransactionError] = useState<string | null>(null);
    

    const [step, setStep] = useState<"idle" | "transcribing" | "interpreting" | "transaction">("idle");
  
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files && e.target.files[0]) {
        setFile(e.target.files[0]);
      }
    };
  
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      if (!file) return;
  
      setLoading(true);
      setResultTranscribe(null);
      setResultInterpret(null);
  
      const formData = new FormData();
      formData.append("file", file);
  
      try {
        const resTranscribe = await fetch("http://localhost:8000/api/transcribe", {
          method: "GET",
          //body: formData,
        });
  
        if (!resTranscribe.ok) throw new Error("Erreur lors de la transcription");
  
        const dataTranscribe = await resTranscribe.json();
        setResultTranscribe(dataTranscribe.text || "Transcription reçue !");
        console.log("Transcription :" + dataTranscribe);
        // Interprétation
        if (dataTranscribe.text) {
          try {
            const resInterpret = await fetch("http://localhost:8000/api/interpret", {
              method: "GET",
              //body: formData,
            });

            if (!resInterpret.ok) throw new Error("Erreur lors de l'interprétation");

            const dataInterpret = await resInterpret.json();
            setResultInterpret(dataInterpret || "Interprétation reçue !");
            console.log("Interprétation :" + dataInterpret);

            setStep("transaction"); 
            try {
              // On suppose que resultInterpret contient les bons champs
              const resTransaction = await fetch("http://localhost:8000/api/send_xrp", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  amount: dataInterpret.amount,
                  recipient: dataInterpret.recipient == "mom" ? "r9iwLjPvqcaMSodxD38moZfEtiUSQQepfa" : dataInterpret.recipient,
                }),
              });
            
              if (!resTransaction.ok) throw new Error("Erreur lors de la transaction");
            
              const dataTransaction = await resTransaction.json();
              const hash = dataTransaction["result"]["hash"];
              setResultTransaction("Transaction envoyée ! " + 
                (typeof hash === "string" ? "hash: [" + hash.slice(0, 12) + "...]" : ""))
            } catch (err) {
              setResultTransactionError("Erreur transaction : " + (err as Error).message);
            }
          } catch (err) {
              setResultInterpretError("Erreur : " + (err as Error).message);
          }
        }
      } catch (err) {
        setResultTranscribe("Erreur : " + (err as Error).message);
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div style={{ maxWidth: 500, margin: "auto", padding: 32 }}>
        <h1>Transcription Audio</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            required
            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
          type="submit" 
          disabled={loading || !file}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
            {loading ? "Execution en cours..." : "Executer"}
          </button>
          {resultTranscribe && (
            <label className="bg-gray-50 border border-gray-300 rounded-lg p-4 text-gray-900">
              {resultTranscribe}
            </label>
          )}
          {resultInterpret && typeof resultInterpret === "object" && (
            <label className="bg-gray-50 border border-gray-300 rounded-lg p-4 text-gray-900">
              {resultInterpret.action} - {resultInterpret.amount} - {resultInterpret.currency} - {resultInterpret.recipient}
            </label>
          )}
          {resultInterpretError && (
            <label className="bg-red-50 border border-red-300 rounded-lg p-4 text-red-900">
              {resultInterpretError}
            </label>
          )}
          {resultTransaction && (
            <label className="bg-green-50 border border-green-300 rounded-lg p-4 text-green-900">
              {resultTransaction}
          </label>
          )}
          {resultTransactionError && (
            <label className="bg-red-50 border border-red-300 rounded-lg p-4 text-red-900">
              {resultTransactionError}
            </label>
          )}

        </form>
      </div>
    );
  }

