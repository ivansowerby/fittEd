<div class="flex min-h-screen items-center justify-center bg-base-200">
  <div class="card w-full max-w-md bg-base-100 shadow-2xl">
    <div class="card-body">
      <h2 class="card-title text-2xl font-bold justify-center mb-4">Welcome Back</h2>
      
      <form method="POST" action="?/login" class="space-y-4">
        <div class="form-control">
          <label class="label" for="email">
            <span class="label-text font-medium" id="email">Email</span>
          </label>
          <input 
            name="email" 
            type="email" 
            placeholder="your@email.com"
            class="input input-bordered w-full" 
            required
          />
        </div>
        
        <div class="form-control">
          <label class="label" for="password">
            <span class="label-text font-medium" id="password">Password</span>
          </label>
          <input 
            name="password" 
            type="password" 
            placeholder="••••••••"
            class="input input-bordered w-full" 
            required
          />
        </div>
        
        <div class="form-control mt-6 space-y-2">
          <button class="btn btn-primary w-full">Login</button>
          <button formaction="?/signup" class="btn btn-outline w-full">Sign up</button>
        </div>
      </form>
    </div>
  </div>
</div>