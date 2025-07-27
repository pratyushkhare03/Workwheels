// Main JavaScript for WorkWheels Taxi Management System

document.addEventListener('DOMContentLoaded', function() {
    
    // Real-time price calculation
    const pickupInput = document.querySelector('input[placeholder="Pickup Location"]');
    const destinationInput = document.querySelector('input[placeholder="Destination"]');
    const bookButton = document.querySelector('.btn-taxi');
    
    if (pickupInput && destinationInput && bookButton) {
        function updatePrice() {
            const pickup = pickupInput.value;
            const destination = destinationInput.value;
            
            if (pickup && destination) {
                // Simulate price calculation based on distance
                const basePrice = 50;
                const pricePerKm = 12;
                const estimatedDistance = Math.floor(Math.random() * 15) + 5; // 5-20 km
                const totalPrice = basePrice + (pricePerKm * estimatedDistance);
                
                bookButton.textContent = `Book Now - ₹${totalPrice}`;
            } else {
                bookButton.textContent = 'Book Now - ₹150';
            }
        }
        
        pickupInput.addEventListener('input', updatePrice);
        destinationInput.addEventListener('input', updatePrice);
    }
    
    // Live ETA update simulation
    function updateETA() {
        const etaElement = document.querySelector('.feature-item span');
        if (etaElement && etaElement.textContent.includes('ETA')) {
            const times = ['3 mins', '5 mins', '7 mins', '4 mins', '6 mins'];
            const randomTime = times[Math.floor(Math.random() * times.length)];
            etaElement.textContent = `ETA: ${randomTime}`;
        }
    }
    
    // Update ETA every 30 seconds
    setInterval(updateETA, 30000);
    
    // Animate statistics on scroll
    // const statItems = document.querySelectorAll('.stat-item h3');
    
    // function animateStats() {
    //     statItems.forEach(item => {
    //         const rect = item.getBoundingClientRect();
    //         if (rect.top < window.innerHeight && rect.bottom > 0) {
    //             item.style.opacity = '1';
    //             item.style.transform = 'translateY(0)';
    //         }
    //     });
    // }
    
    // // Initialize stats animation
    // statItems.forEach(item => {
    //     item.style.opacity = '0';
    //     item.style.transform = 'translateY(20px)';
    //     item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    // });
    
    // window.addEventListener('scroll', animateStats);
    // animateStats(); // Initial check
    
    // Service card hover effects
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Form validation and enhancement
    const bookingForm = document.querySelector('.booking-form');
    if (bookingForm) {
        const inputs = bookingForm.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
    }
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Loading animation for booking button
    if (bookButton) {
        bookButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show loading state
            const originalText = this.textContent;
            this.textContent = 'Booking...';
            this.disabled = true;
            
            // Simulate booking process
            setTimeout(() => {
                this.textContent = 'Booking Confirmed!';
                this.style.backgroundColor = '#28a745';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                    this.style.backgroundColor = '';
                }, 2000);
            }, 2000);
        });
    }
    
    // Dynamic driver info update
    // const driverNames = ['Rajesh Kumar', 'Amit Singh', 'Vikram Patel', 'Suresh Reddy'];
    // const carModels = ['Swift Dzire', 'Honda City', 'Hyundai Verna', 'Maruti Ciaz'];
    // const ratings = ['4.8', '4.9', '4.7', '4.6'];
    
    // function updateDriverInfo() {
    //     const driverNameElement = document.querySelector('.driver-details h6');
    //     const ratingElement = document.querySelector('.driver-details p');
    //     const carInfoElement = document.querySelector('.car-info');
        
    //     if (driverNameElement && ratingElement && carInfoElement) {
    //         const randomIndex = Math.floor(Math.random() * driverNames.length);
    //         const randomRides = Math.floor(Math.random() * 3000) + 1000;
            
    //         driverNameElement.textContent = driverNames[randomIndex];
    //         ratingElement.textContent = `${ratings[randomIndex]} ★ (${randomRides} rides)`;
    //         carInfoElement.textContent = `${carModels[randomIndex]} • KA-01-AB-${Math.floor(Math.random() * 9000) + 1000}`;
    //     }
    // }
    
    // // Update driver info every 2 minutes
    // setInterval(updateDriverInfo, 120000);
    
    // Add parallax effect to hero section
    // window.addEventListener('scroll', function() {
    //     const scrolled = window.pageYOffset;
    //     const hero = document.querySelector('.hero');
    //     if (hero) {
    //         const rate = scrolled * -0.5;
    //         hero.style.transform = `translateY(${rate}px)`;
    //     }
    // });
    
    // Initialize tooltips for better UX
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('WorkWheels Taxi Management System initialized successfully!');
}); 