import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { splitTextBySimilarity } from '$lib/transformer';

export const POST: RequestHandler = async ({ request }) => {
	const data = await request.json();
	const { text = '', threshold = 0.9 } = data;

	if (!text) {
		return json({ error: 'No text provided' }, { status: 400 });
	}

	const groupedSentences = await splitTextBySimilarity(text, threshold);
	return json({ groupedSentences });
};
