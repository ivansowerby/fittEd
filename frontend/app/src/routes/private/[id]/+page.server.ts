import { getSessionId, getText } from '$lib/requests.js';
import { redirect } from '@sveltejs/kit';

export let load = async ({ locals: { supabase }, params: { id } }) => {
	const { data, error } = await supabase.from('data').select('session').eq('id', id);

	if (error || !data) {
		console.log(error);
	}

	try {
		let csv = await getText(data[0].session);

		let titles = csv.split('\n')[0].split('\n')[0].split(',');

		return {
			id: (data as { session: string }[])[0].session,
			titles,
			csv
		};
	} catch (e) {
		console.log(e);
		redirect(303, '/error');
	}
};
