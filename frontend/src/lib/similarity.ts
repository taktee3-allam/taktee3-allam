/**
 * Calculate the cosine similarity between two vectors.
 */
export function cosineSimilarity(a: number[], b: number[]): number {
	if (a.length !== b.length) {
		throw new Error('Vectors must have the same length');
	}

	let dotProduct = 0;
	let magnitudeA = 0;
	let magnitudeB = 0;
	for (let i = 0; i < a.length; i++) {
		dotProduct += a[i] * b[i];
		magnitudeA += a[i] ** 2;
		magnitudeB += b[i] ** 2;
	}
	magnitudeA = Math.sqrt(magnitudeA);
	magnitudeB = Math.sqrt(magnitudeB);
	return dotProduct / (magnitudeA * magnitudeB);
}
