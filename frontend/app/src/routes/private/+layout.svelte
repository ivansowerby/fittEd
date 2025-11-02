<script>
  let { data, children } = $props()
  let { supabase } = $derived(data)

  const logout = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) {
      console.error(error)
    }
    window.location.href = '/'
  }
</script>

<header class="navbar bg-base-100 shadow-lg z-10">
  <div class="flex-1">
    <nav>
      <a href="/private" class="btn btn-ghost text-xl">Home</a>
    </nav>
  </div>
  <div class="flex-none">
    <button onclick={logout} class="btn btn-primary">Logout</button>
  </div>
</header>
<main>
  {@render children()}
</main>