import { getSessionId } from '$lib/requests.js';

export async function POST({ request, locals: { supabase, user } }) {
	let formData = await request.formData();
	let text = formData.get('text');
	let name = formData.get('name');

	if (!text) {
		return new Response(JSON.stringify({ success: false, error: 'Text is required' }), {
			status: 400,
			headers: { 'Content-Type': 'application/json' }
		});
	}

	let session = await getSessionId(text.toString());

	let { data, error } = await supabase
		.from('data')
		.insert({
			user_id: user?.id,
			name: name?.toString() || 'Untitled Project',
			session
		})
		.select('id');

	if (error) {
		return new Response(JSON.stringify({ success: false, error: error.message }));
	}

	// @ts-ignore
	return new Response(JSON.stringify({ success: true, id: data[0].id }));
}
