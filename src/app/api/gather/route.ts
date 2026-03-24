import { generateText } from "ai";
import { openrouter, MODELS } from "@/lib/openrouter";
import { geminiSearchGrounded } from "@/lib/gemini";

export async function POST() {
  const systemPrompt = `You are a geopolitical intelligence analyst. Your task is to provide a detailed, neutral, factual account of the current situation regarding the Iran-Israel-US military conflict.

Structure your report with sections covering developments across these time windows: past 3 hours, past 6 hours, past 12 hours, and past 24 hours.

Rules:
- Be detailed but neutral — no predictions, no opinions
- Write for AI agent consumption (clear, structured, factual)
- All timestamps in UTC
- If you lack information for a time window, state that clearly
- Cover military actions, diplomatic developments, public statements, and regional reactions`;

  const [geminiResult, grokResult] = await Promise.all([
    geminiSearchGrounded(
      "Provide a comprehensive situational update on the Iran-Israel-US conflict. Cover the past 3h, 6h, 12h, and 24h windows.",
      systemPrompt,
    ),
    generateText({
      model: openrouter(MODELS.grok),
      system: systemPrompt,
      prompt: "Provide a comprehensive situational update on the Iran-Israel-US conflict. Cover the past 3h, 6h, 12h, and 24h windows. Fill in any gaps with the most recent available information.",
    }),
  ]);

  const mergeResult = await generateText({
    model: openrouter(MODELS.grok),
    system: `You are a geopolitical intelligence editor. You will receive two raw intelligence feeds about the Iran-Israel-US conflict. Produce a single, clean, consolidated Ground Truth report.

CRITICAL FORMATTING RULES:
- Do NOT mention sources, feeds, or that multiple inputs were used
- Do NOT label anything as "Source 1" or "Source 2"
- Do NOT include meta-commentary about the report itself
- Write as a single authoritative intelligence document
- Start with a bold title line: "**GROUND TRUTH: IRAN-ISRAEL-US CONFLICT**"
- Follow with report date/time in UTC
- Then an executive overview paragraph (3-5 sentences)
- Then time-window sections: Past 3 Hours, Past 6 Hours, Past 12 Hours, Past 24 Hours
- Within each section use sub-headings: Military Actions, Diplomatic Developments, Public Statements, Regional Reactions
- If the two feeds conflict, use the more recent or more detailed account without noting the discrepancy
- All timestamps in UTC
- Neutral, factual tone — no predictions`,
    prompt: `=== FEED A ===\n${geminiResult}\n\n=== FEED B ===\n${grokResult.text}`,
  });

  return Response.json({ groundTruth: mergeResult.text });
}
