<script lang="ts">
	import { getAnalysis, type GetAnalysisReq } from '$lib/requests';
	import { SVG } from '@svgdotjs/svg.js';
	import { untrack } from 'svelte';
    const { data } = $props();
    const { id, titles, csv } = $derived(data);
    let numbers: number[] = $state([]);
    let getValues: boolean[] = $state([]);
    let result_display: null | Record<string, string> = $state(null);
    let isLoading = $state(false);
    let score: string | null = $state(null);

    let config_link = $state("");
 
    $effect(() => {
        titles;
        untrack(() => {
            numbers = [];
            getValues = [];
            for (let i = 0; i < titles.length; i++) {
                getValues.push(false);
                numbers.push(0);
            }
        });
    });

    $effect(() => {
        let draw = SVG().addTo("#drawing");
        draw.size("100%", "100%");


        // let pattern = draw.pattern(1500, 1500, function(add) {
            // add.path("M 0 10 H 1500").fill("none").stroke({width: 1, color: "#ffffff"})
        // });

        const glowFilter = draw.defs().element('filter').attr({ id: 'glow' });
        glowFilter.element('feGaussianBlur').attr({ stdDeviation: '4', result: 'coloredBlur' });
        const feMerge = glowFilter.element('feMerge');
        feMerge.element('feMergeNode').attr({ in: 'coloredBlur' });
        feMerge.element('feMergeNode').attr({ in: 'SourceGraphic' });
        
        let gradient = draw.gradient('linear', (add) => {
            add.stop(0, '#87E85500')
            add.stop(0.5, '#64DAD530')
            add.stop(1, '#64DAD500')
        })

        let gradient1 = draw.gradient('linear', (add) => {
            add.stop(0, '#87E85500')
            add.stop(0.5, '#64DAD580')
            add.stop(1, '#64DAD500')
        }).from(0, 0).to(0, 1)


        var pattern = draw.pattern(1500, 100, function(add) {
            let path = add.path("M -500 10 C -500 10 1500 15 1500 10").fill("none").stroke({width: 3, color: '#ffffff'}).attr({ filter: 'url(#glow)', stroke: gradient });
        })

        var pattern2 = draw.pattern(100, 1500, function(add) {
            add.path("M 10 -500 C 10 -500 15 1500 10 1500").fill("none").stroke({width: 3, color: '#ffffff'}).attr({filter: 'url(#glow)', stroke: gradient1});
        })


        let rect = draw.rect("100%", "100%");
        let rect2 = draw.rect("100%", "100%");

        rect.fill(pattern)
        rect2.fill(pattern2)
    })    
</script>

<div id="drawing" class="inset-0 fixed"></div>
<div class="fixed inset-0 backdrop-blur-xs"></div>


<div class="container mx-auto p-6 max-w-6xl">
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<!-- Left Column - Features Configuration -->
		<div class="lg:col-span-2">
			<div class="card bg-base-100 shadow-xl flex p-5">
                <label for="config">Link your config: </label>
                <input type="text" placeholder="raw.github.com/..." class="input" id="config" bind:value={config_link}>
            </div>
            <br />
			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title text-2xl mb-4">Configure Features</h2>
				
					<div class="space-y-3 max-h-[600px] overflow-y-auto pr-2">
						{#each titles as title, idx}
							<div class="card bg-base-200 shadow-sm">
								<div class="card-body p-4">
									<div class="flex items-center justify-between gap-4">
										<div class="flex-1">
											<label class="label cursor-pointer justify-start gap-3">
												<input 
													type="checkbox" 
													bind:checked={getValues[idx]}
													class="checkbox checkbox-primary border-accent border-1"
												/>
												<span class="label-text font-semibold">{title}</span>
											</label>
										</div>
										
										{#if !getValues[idx]}
											<div class="form-control w-32">
												<input 
													bind:value={numbers[idx]} 
													type="number"
													class="input input-bordered input-sm w-full"
													placeholder="Value"
												/>
											</div>
										{:else}
											<div class="badge badge-info gap-2">
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
													<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
												</svg>
												Auto-detect
											</div>
										{/if}
									</div>
								</div>
							</div>
						{/each}
					</div>

					<div class="card-actions justify-end mt-6">
						<button 
							class="btn btn-primary btn-wide"
							class:loading={isLoading}
							disabled={isLoading}
							onclick={async () => {
								isLoading = true;
								let features: Record<string, number[] | null> = {};
								numbers.forEach((num, idx) => {
									if (getValues[idx]) {
										features[titles[idx]] = null;
									} else {
                                        let list = [num];
										features[titles[idx]] = list;
									}
								});
								
								let req = {
									session_id: id,
									features,
									config: {}
								} as GetAnalysisReq;

                                if (config_link.trim()) {
                                    const res_link = await fetch(config_link.trim())
                                    req.config = await res_link.json();
                                    console.log("fetched stuff");
                                } else {
		                            req.config = {
			                            preprocessing: [
				                            {
					                            name: 'PolynomialFeatures',
					                            args: {
						                        degree: 2,
						                        include_bias: false
					                        }
				                        },
				                        {
					                        name: 'StandardScaler',
					                        args: {}
				                            }
			                            ],
			                            model: {
				                            name: 'LinearRegression',
				                            args: {}
			                            }
		                            };
                                }
								
								try {
									let result = await getAnalysis(req);
                                    console.log(result);
									let fields = result.fields as string;
                                    fields.replaceAll("\"", "");
                                    fields.replaceAll("\\n", "\n");
                                    console.log(fields)

                                    let score_strs = (result.score * 100).toString().split(".");
                                    score = score_strs[0] + "." + score_strs[1].substring(0, 2) + "%";

                                    let field_titles = fields.split("\n")[0].split(",")
                                    let field_values = fields.split("\n")[1].split(",").map((str) => {
                                        return parseFloat(str)
                                    })

                                    for (let i = 0; i < field_titles.length; i++) {
                                        for (let j = 0; j < titles.length; j++) {
                                            if (titles[j] == field_titles[i]) {
                                                getValues[j] = false;
                                                numbers[j] = Math.trunc(field_values[i] * 100) / 100;
                                                break;
                                            }
                                        }
                                    }

								} catch (error) {
									console.error(error);
								} finally {
									isLoading = false;
								}
							}}
						>
							{#if isLoading}
								<span class="loading loading-spinner"></span>
								Running Analysis...
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
									<path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
								</svg>
								Run Analysis
							{/if}
						</button>
					</div>
				</div>
			</div>
		</div>

		<!-- Right Column - Results -->
		<div class="lg:col-span-1">
			<div class="card bg-base-100 shadow-xl sticky top-6">
				<div class="card-body">
					<h2 class="card-title text-xl mb-4">Accuracy</h2>
					
					{#if score}
						<div class="mockup-code max-h-[500px] overflow-y-auto">
                            <pre>{score}</pre>
						</div>
					{:else}
						<div class="flex flex-col items-center justify-center py-12 text-center">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-base-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
							</svg>
							<p class="text-base-content/60">No results yet</p>
							<p class="text-sm text-base-content/40 mt-2">Configure features and run analysis</p>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>

	<!-- CSV Data Section -->
	{#if csv}
		<div class="card bg-base-100 shadow-xl mt-6">
			<div class="card-body">
				<h2 class="card-title text-xl mb-4">
					CSV Data
					<div class="badge badge-neutral">Raw Data</div>
				</h2>
				<div class="mockup-code max-h-64 overflow-y-auto">
					<pre class="text-xs"><code>{csv}</code></pre>
				</div>
			</div>
		</div>
	{/if}
</div>