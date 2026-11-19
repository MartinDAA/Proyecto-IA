import { defineEnvVars } from '@sveltejs/kit/env';

export const variables = defineEnvVars({
	BACKEND_URL: {
		description: 'URL base de la API de FastAPI.',
		schema: (value) => value || 'http://localhost:8000'
	}
});
