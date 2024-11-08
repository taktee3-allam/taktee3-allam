export const baseUrl = import.meta.env.DEV ? 'http://127.0.0.1:5000' : 'http://127.0.0.1:5000';

export async function getEmbedding(text: string): Promise<number[]> {
	const response = await fetch(`${baseUrl}/api/embed`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ text })
	});
	const { embedding } = await response.json();
	return embedding;
}

export async function sendPrompt(message: string, useTaqtee3: boolean = false): Promise<string> {
	const response = await fetch(`${baseUrl}/api/prompt`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			prompt: message,
			useTaqtee3
		})
	});

	if (!response.ok) {
		throw await response.text();
	}

	const data = await response.json();
	return data.response;
}

export type Sentence = { sentence: string; embedding: number[] };

/**
 *
 * @param text
 * @param threshold Number between 0 and 100
 * @returns
 */
export async function splitText(text: string, threshold: number): Promise<Sentence[]> {
	const res = await fetch(`${baseUrl}/api/split_text`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ text, threshold: threshold / 100 })
	});
	const data = await res.json();
	console.log(data)
	return data.grouped_sentences;
}
