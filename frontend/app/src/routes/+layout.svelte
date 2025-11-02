<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

    import { invalidate } from '$app/navigation'
    import { onMount } from 'svelte'

    let { data, children } = $props()
    let { session, supabase } = $derived(data)

    onMount(() => {
        const { data } = supabase.auth.onAuthStateChange((_, newSession) => {
            if (newSession?.expires_at !== session?.expires_at) {
                invalidate('supabase:auth')
            }
        })

        return () => data.subscription.unsubscribe()
    })

</script>

<style>
    .bg {
        background: radial-gradient(circle at 50% 50%, rgba(9, 30, 90, 1) 0%, rgba(3, 12, 42, 1) 100%);
    }
</style>

<div class="fixed inset-0 bg"></div>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}