import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";
import { NextResponse } from "next/server";

export const dynamic = 'force-dynamic';

const bedrock = new BedrockRuntimeClient({
  region: process.env.AWS_REGION || "us-east-1",
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
  },
});

export async function POST(req: Request) {
  try {
    const { category } = await req.json();

    const prompt = `Generate a vocabulary list for the category "${category}" in Spanish and Arabic with transliteration. Format the output as a JSON object with the following structure:
    {
      "group": {
        "name": "${category}"
      },
      "words": [
        {
          "spanish": "word in spanish",
          "transliteration": "spanish transliteration in arabic language",
          "arabic": "word in arabic"
        }
      ]
    }
    Include at least 5 relevant words or phrases for this category.`;

    const command = new InvokeModelCommand({
      modelId: "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
      contentType: "application/json",
      accept: "application/json",
      body: JSON.stringify({
        anthropic_version: "bedrock-2023-05-31",
        max_tokens: 1000,
        messages: [
          {
            role: "user",
            content: prompt,
          },
        ],
      }),
    });

    const response = await bedrock.send(command);
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));
    console.log('Raw response:', JSON.stringify(responseBody, null, 2));
    
    // Extract the JSON string from Claude's response
    const match = responseBody.content[0].text.match(/\{[\s\S]*\}/);
    if (!match) {
      throw new Error('No JSON found in response: ' + responseBody.content[0].text);
    }
    
    const content = JSON.parse(match[0]);
    return NextResponse.json(content);
  } catch (error) {
    console.error("Detailed Error:", JSON.stringify(error, null, 2));
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to generate vocabulary', details: error },
      { status: 500 }
    );
  }
}