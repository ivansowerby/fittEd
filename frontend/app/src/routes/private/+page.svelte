<script lang="ts">
	import { goto } from '$app/navigation';
	import { SVG } from '@svgdotjs/svg.js';
	import { untrack } from 'svelte';
    import {
	blur,
	crossfade,
	draw,
	fade,
	fly,
	scale,
	slide
} from 'svelte/transition';
    const { data } = $props();

    let keyword = $state('');

    const { entries } = $derived(data);

    let entries_display: {id: number, name: string}[] = $state([]);
   
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

    $effect(() => {
        keyword;

        untrack(() => {
            entries_display = [];
            entries.forEach((ent) => {
                if (ent.name.includes(keyword.trim()) || keyword.trim().includes(ent.name) || keyword.trim() == '') {
                    entries_display.push(ent);
                }
            })
        })
    });
</script>

<div id="drawing" class="inset-0 fixed"></div>
<div class="fixed inset-0 backdrop-blur-xs"></div>

<style>
    #drawing {
        filter: brightness(1);
    }
</style>

<div class="container mx-auto p-6 max-w-6xl">
  <!-- Header Section -->
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8 z-20">
    <h1 class="text-3xl font-bold z-20">Your Dashboard</h1>
    <a href="/private/new-project" class="btn btn-primary z-10">
      <svg xmlns="http://www.w3.org/2000/svg" class="z-10 h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
      New Project
    </a>
  </div>

  <!-- Search Bar -->
  <div class="form-control w-full mb-6">
    <label for="search" class="label">
      <span class="label-text">Search projects</span>
    </label>
    <input 
      type="text" 
      id="search" 
      placeholder="Search here..." 
      class="input input-bordered w-full"
      bind:value={keyword}
    />
  </div>

  <!-- Projects Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
    {#each entries_display as entry, id}
      <div class="card shadow-md hover:shadow-lg aspect-square transition-all hover:border-2 border-1 border-lime-100 backdrop-blur-xl backdrop-opacity-99" transition:fly={{
        y: 100,
        duration: 500,
        delay: id * 100
      }}>
        <div class="card-body">
          <h2 class="card-title">{entry.name}</h2>
          <div class="card-actions justify-end mt-4">
            <button 
              class="btn btn-sm btn-outline"
              onclick={() => {
                goto(`/private/${entry.id}`);
              }}
            >
              View Details
            </button>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <!-- Empty State (optional) -->
  {#if entries.length === 0}
    <div class="text-center py-12">
      <p class="text-base-content/60 text-lg">No projects yet. Create your first one!</p>
    </div>
  {/if}
</div>