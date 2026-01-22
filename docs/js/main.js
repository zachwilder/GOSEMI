// JavaScript for Go Semi & Beyond Newsletter Site

document.addEventListener('DOMContentLoaded', function() {
    console.log('Go Semi & Beyond site loaded');

    // Dropdown Menu
    const setupDropdowns = () => {
        const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

        // Toggle dropdown on click
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                const parent = this.parentElement;
                const menu = parent.querySelector('.dropdown-menu');

                // Close all other open dropdowns
                document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                    if (openMenu !== menu) {
                        openMenu.classList.remove('show');
                    }
                });

                // Toggle current dropdown
                menu.classList.toggle('show');
            });
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });

        console.log('Dropdown menus initialized');
    };

    // Mobile Navigation Toggle
    const setupMobileNav = () => {
        const mobileToggle = document.querySelector('.mobile-nav-toggle');
        const nav = document.querySelector('nav ul');

        if (mobileToggle && nav) {
            mobileToggle.addEventListener('click', function() {
                nav.classList.toggle('show');
                this.classList.toggle('active');
            });
        }

        console.log('Mobile navigation ready');
    };

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Newsletter subscription form handler
    const subscribeForm = document.querySelector('.subscribe-form');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            console.log(`Subscription requested for: ${email}`);

            // Show success message
            alert('Thank you for subscribing to Go Semi & Beyond!');
            this.reset();
        });
    }

    // Large subscribe form handler
    const subscribeFormLarge = document.querySelector('.subscribe-form-large');
    if (subscribeFormLarge) {
        subscribeFormLarge.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            const name = this.querySelector('input[type="text"]')?.value || '';
            console.log(`Subscription requested for: ${name} (${email})`);

            // Show success message
            alert('Thank you for subscribing to Go Semi & Beyond! You will receive our next issue in your inbox.');
            this.reset();
        });
    }

    // Poll form handler
    const pollForm = document.querySelector('.poll-form');
    if (pollForm) {
        pollForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const selected = this.querySelector('input[name="poll"]:checked');
            if (selected) {
                console.log(`Poll vote: ${selected.value}`);
                alert('Thank you for your vote!');
            } else {
                alert('Please select an option before voting.');
            }
        });
    }

    // Article card hover effects (already handled in CSS, but can add more interactivity)
    const articleCards = document.querySelectorAll('.article-card, .issue-card');
    articleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
    });

    // Lazy load images
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }

    // Initialize all components
    setupDropdowns();
    setupMobileNav();
});
