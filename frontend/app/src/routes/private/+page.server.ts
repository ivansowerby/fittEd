import { redirect } from '@sveltejs/kit';

export let load = async ({ locals: { supabase } }) => {
	const { data, error } = await supabase.from('data').select('id, name').order('created_at');

	if (error || !data) {
		console.log(error);
		redirect(303, '/error');
	}

	return {
		entries: data as { id: number; name: string }[]
	};
};
