<script lang="ts">
	import { goto } from "$app/navigation";
    let selectedFile: File | null = $state(null);
    let fileContent: string | ArrayBuffer | null = $state('');
    let projectName = $state('');
    let isLoading = $state(false);
    let error = $state('');
</script>

<div class="container mx-auto p-6 max-w-2xl">
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title text-2xl mb-6">Create New Project</h2>
			
			<!-- Project Name Input -->
			<div class="form-control w-full mb-4">
				<label for="project-name" class="label">
					<span class="label-text font-semibold">Project Name</span>
					<span class="label-text-alt text-error">{projectName ? '' : 'Required'}</span>
				</label>
				<input 
					id="project-name"
					type="text" 
					bind:value={projectName} 
					placeholder="Enter project name..."
					class="input input-bordered w-full"
					class:input-error={!projectName && error}
				/>
			</div>

			<!-- File Upload -->
			<div class="form-control w-full mb-4">
				<label for="css-file" class="label">
					<span class="label-text font-semibold">Upload csv File</span>
					<span class="label-text-alt text-error">{selectedFile ? '' : 'Required'}</span>
				</label>
				<input 
					id="css-file"
					type="file" 
					accept=".csv"
					class="file-input file-input-bordered w-full"
					class:file-input-error={!selectedFile && error}
					onchange={async (evt) => {
						selectedFile = (evt.target as HTMLInputElement).files?.[0] || null;
						if (!selectedFile) return;
						
						const reader = new FileReader();
						reader.onload = (e) => {
							// @ts-ignore
							fileContent = e.target.result;
						};
						reader.readAsText(selectedFile);
					}}
				/>
				{#if selectedFile}
					<label class="label">
						<span class="label-text-alt text-success">
							<svg xmlns="http://www.w3.org/2000/svg" class="inline h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
							</svg>
							{selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
						</span>
					</label>
				{/if}
			</div>

			<!-- Error Message -->
			{#if error}
				<div class="alert alert-error mb-4">
					<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
					<span>{error}</span>
				</div>
			{/if}

			<!-- File Content Preview -->
			{#if fileContent}
				<div class="form-control mb-4">
					<label class="label">
						<span class="label-text font-semibold">File Preview</span>
					</label>
					<div class="max-h-64 overflow-y-auto">
						<pre class="text-xs"><code>{fileContent}</code></pre>
					</div>
				</div>
			{/if}

			<!-- Submit Button -->
			<div class="card-actions justify-end mt-6">
				<button 
					class="btn btn-primary btn-wide"
					class:loading={isLoading}
					disabled={!selectedFile || !fileContent || !projectName || isLoading}
					onclick={async () => {
						if (!selectedFile || !fileContent || !projectName) {
							error = 'Please fill in all required fields';
							return;
						}
						
						isLoading = true;
						error = '';
						
						const formData = new FormData();
						formData.append('text', fileContent.toString());
						formData.append('name', projectName);
						
						try {
							const response = await fetch('/api/new-project', {
								method: 'POST',
								body: formData
							});
							
							let result = await response.json();
							if (result.success) {
								goto(`/private/${result.id}`);
							} else {
								error = result.error || 'Failed to create project';
								isLoading = false;
							}
						} catch (err) {
							console.error('Error uploading file:', err);
							error = 'An error occurred while uploading the file';
							isLoading = false;
						}
					}}
				>
					{#if isLoading}
						<span class="loading loading-spinner"></span>
						Creating Project...
					{:else}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd" />
						</svg>
						Start Project
					{/if}
				</button>
			</div>
		</div>
	</div>
</div>