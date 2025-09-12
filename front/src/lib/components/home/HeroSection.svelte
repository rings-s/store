<!-- src/lib/components/home/HeroSection.svelte -->
<script>
    import { ArrowRight, Sparkles } from 'lucide-svelte';
    import Button from '../ui/Button.svelte';
    
    let currentSlide = $state(0);
    const slides = [
      {
        title: 'Premium Collection',
        subtitle: '2025',
        description: 'Discover our exclusive range of carefully curated products',
        image: '/hero-1.jpg',
        color: 'from-purple-600/90 to-pink-600/90'
      },
      {
        title: 'New Arrivals',
        subtitle: 'Just Dropped',
        description: 'Fresh styles and innovative designs for the modern lifestyle',
        image: '/hero-2.jpg',
        color: 'from-blue-600/90 to-purple-600/90'
      }
    ];
    
    $effect(() => {
      const interval = setInterval(() => {
        currentSlide = (currentSlide + 1) % slides.length;
      }, 5000);
      
      return () => clearInterval(interval);
    });
  </script>
  
  <section class="relative h-[90vh] overflow-hidden rounded-3xl mx-4 mt-4">
    {#each slides as slide, index}
      <div
        class="absolute inset-0 transition-opacity duration-1000 {currentSlide === index ? 'opacity-100' : 'opacity-0'}"
      >
        <!-- Background Image -->
        <img
          src={slide.image}
          alt={slide.title}
          class="w-full h-full object-cover"
        />
        
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-r {slide.color}"></div>
        
        <!-- Content -->
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="text-center text-white max-w-4xl px-4 animate-slide-up">
            <div class="flex items-center justify-center gap-2 mb-4">
              <Sparkles class="w-5 h-5" />
              <span class="text-sm font-medium uppercase tracking-wider">
                {slide.subtitle}
              </span>
              <Sparkles class="w-5 h-5" />
            </div>
            
            <h1 class="font-display text-6xl md:text-8xl font-bold mb-6 text-balance">
              {slide.title}
            </h1>
            
            <p class="text-xl md:text-2xl mb-8 text-white/90 max-w-2xl mx-auto">
              {slide.description}
            </p>
            
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="glass" size="lg" icon={ArrowRight} iconPosition="right">
                Shop Collection
              </Button>
              <Button variant="ghost" size="lg" class="text-white hover:bg-white/10">
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </div>
    {/each}
    
    <!-- Slide Indicators -->
    <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-2">
      {#each slides as _, index}
        <button
          onclick={() => currentSlide = index}
          class="w-12 h-1 rounded-full transition-all duration-300 {currentSlide === index ? 'bg-white w-24' : 'bg-white/50'}"
        />
      {/each}
    </div>
  </section>