import { SentenceTransformer } from '@tuesdaycrowd/sentence-transformers/src/model';
import { cosineSimilarity } from './similarity';

// const model = await SentenceTransformer.from_pretrained('mixedbread-ai/mxbai-embed-large-v1');
const model = await SentenceTransformer.from_pretrained('paraphrase-multilingual-MiniLM-L12-v2');

export async function splitTextBySimilarity(
	text: string,
	similarityThreshold: number
): Promise<string[]> {
	const sentences = text.split('.');
	const embeddings = await model.encode(sentences);
	const groupedSentences: string[] = [];
	let currentGroup = [sentences[0]];

	for (let i = 1; i < sentences.length; i++) {
		const sim = cosineSimilarity(embeddings[i - 1], embeddings[i]);
		if (sim < similarityThreshold) {
			groupedSentences.push(currentGroup.join(' '));
			currentGroup = [sentences[i]];
		} else {
			currentGroup.push(sentences[i]);
		}
	}

	groupedSentences.push(currentGroup.join(' '));
	return groupedSentences;
}
