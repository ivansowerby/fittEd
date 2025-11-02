import { PUBLIC_BACKEND_URL } from '$env/static/public';

export type GetAnalysisReq = {
	session_id: string;
	features: Record<string, number[] | null>;
	config: Record<any, any>;
};

export let getSessionId = async (file: string) => {
	try {
		let res = await fetch(`${PUBLIC_BACKEND_URL}/dataset/create`, {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: file
		});

		console.log('askjdalskjkdaaklsdjadsjkl');
		let data = await res.json();
		console.log(data);
		return data.session_id;
	} catch (e) {
		console.log(e);
	}

	// return 'test-session-id';
};

export let getText = async (session: string) => {
	try {
		console.log(session);
		let res = await fetch(`${PUBLIC_BACKEND_URL}/dataset/get?session_id=${session}`, {
			method: 'GET'
		});
		let data = await res.text();
		console.log(data[0]);
		return data;
	} catch (e) {
		console.log(e);
	}
	// return 'a bunch of garbage';
};

export let deleteSession = async (session: string) => {
	try {
		let res = await fetch(`${PUBLIC_BACKEND_URL}/session/delete?session=${session}`, {
			method: 'GET'
		});
		let data = await res.json();
		return data.success;
	} catch (e) {
		console.log(e);
	}

	// return true;
};

export let getAnalysis = async (req: GetAnalysisReq) => {
	try {
		console.log(JSON.stringify(req));
		let res = await fetch(`${PUBLIC_BACKEND_URL}/label`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(req)
		});

		let data = await res.json();
		console.log(data);
		return data;
	} catch (e) {
		console.log(e);
	}

	// return { result: req.features };
};
