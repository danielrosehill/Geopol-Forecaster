import { GoogleGenAI } from "@google/genai";

const genai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! });

export async function geminiSearchGrounded(prompt: string, systemPrompt?: string): Promise<string> {
  const response = await genai.models.generateContent({
    model: "gemini-3.1-flash-lite-preview",
    contents: [
      ...(systemPrompt
        ? [{ role: "user" as const, parts: [{ text: systemPrompt }] }, { role: "model" as const, parts: [{ text: "Understood. I will follow these instructions." }] }]
        : []),
      { role: "user" as const, parts: [{ text: prompt }] },
    ],
    config: {
      tools: [{ googleSearch: {} }],
    },
  });

  return response.text ?? "";
}
