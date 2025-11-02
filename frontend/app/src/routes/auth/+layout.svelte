<script>
  let { children } = $props()
</script>

<header class="navbar bg-base-100 shadow-lg">
  <div class="flex-1">
    <nav>
      <a href="/" class="btn btn-ghost text-xl">Home</a>
    </nav>
  </div>
</header>


{@render children()}