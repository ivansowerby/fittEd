<script lang="ts">
	import { Svg, SVG } from "@svgdotjs/svg.js";

    import {fly} from "svelte/transition"

    let hey = $state(false);
    $effect(() => {
        hey = true;
    });

    function add_path(draw: Svg, line1: string, line2: string, delay: number, dur: number) {
        draw.size("100%", "100%")

        const glowFilter = draw.defs().element('filter').attr({ id: 'glow' });
        glowFilter.element('feGaussianBlur').attr({ stdDeviation: '4', result: 'coloredBlur' });
        const feMerge = glowFilter.element('feMerge');
        feMerge.element('feMergeNode').attr({ in: 'coloredBlur' });
        feMerge.element('feMergeNode').attr({ in: 'SourceGraphic' });

        let gradient = draw.gradient('linear', (add) => {
            add.stop(0, '#87E85500')
            add.stop(0.5, '#64DAD588')
            add.stop(1, '#64DAD500')
        })


        let path = draw.path(line1).fill("none").stroke({width: 3, color: '#ffffff'}).attr({ filter: 'url(#glow)', stroke: gradient });

        let length = path.length();

        // @ts-ignore
        path.stroke({
            dasharray: length,
            dashoffset: length
        })

        path.animate(1000, delay).ease("<>").stroke({dashoffset: 0})

        // @ts-ignore
        path.animate(dur).ease("<>").plot(line2).loop(true, true);

        return path
    }

    $effect(() => { 
        let draw = SVG().addTo("#drawing")
        add_path(draw, "M 0 300 C 573 651 722 -171 1500 211", "M 0 300 C 622 471 661 -33 1500 211", 0, 3000);
        add_path(draw,  "M 0 591 C 676 248 731 566 1500 411", "M 0 591 C 600 616 731 307 1500 411", 200, 3500);
        add_path(draw,  "M 0 100 C 573 651 722 -171 1471 565", "M 0 100 C 629 183 484 402 1471 565",400, 4500);
    });
</script>

<div class="fixed left-0 top-0 bottom-0 right-0" id="drawing"></div>

<div class="hero min-h-screen bg-base-200">
  <div class="hero-content text-center">
    <div class="max-w-md backdrop-blur-xs m-10 p-10 rounded-3xl">        
      {#if hey}
      <!-- <img 
        src="/logo.png" 
        alt="Fit ED Logo" 
        class="mx-auto mb-8 rounded-lg shadow-xl"
      />
 -->
          <h1 class="text-5xl font-bold from-primary to-secondary bg-clip-text kool-title" transition:fly={{y: 100, duration: 1000}}>
            FittED
          </h1>
          <p class="py-6 text-lg text-base-content/70" transition:fly={{y: 100, delay: 50, duration: 1000}}>
            The next generation data prediction tool
          </p>
          <a href="/auth" class="btn btn-primary btn-lg gap-2 cool-btn transition-all bg-base-300 border-accent" transition:fly={{y: 100, delay: 100, duration: 1000}}>
            Log In
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </a>
        {/if}
    </div>
  </div>
</div>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Momo+Signature&display=swap');

    .kool-title {
        font-family: "Momo Signature", cursive;
        font-weight: 400;
        font-style: normal;
    }

    .cool-btn:hover {
        box-shadow:
            0 0 20px 5px rgb(86, 185, 231)
    }

    .cool-btn {
        box-shadow:
             0 0 0px 0px rgb(86, 185, 231)
    }

</style>