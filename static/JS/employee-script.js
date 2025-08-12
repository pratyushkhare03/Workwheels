// Google Maps Places API initialization

function initAutocomplete() {
  const pickupInput = document.getElementById('pickup');
  const dropInput = document.getElementById('drop');

  if (pickupInput && dropInput) {
    const pickupAutocomplete = new google.maps.places.Autocomplete(pickupInput);
    pickupAutocomplete.addListener('place_changed', function() {
      const place = pickupAutocomplete.getPlace();
      if (place.geometry) {
        document.getElementById('pickup-lat').value = place.geometry.location.lat();
        document.getElementById('pickup-lng').value = place.geometry.location.lng();
      }
    });

    const dropAutocomplete = new google.maps.places.Autocomplete(dropInput);
    dropAutocomplete.addListener('place_changed', function() {
      const place = dropAutocomplete.getPlace();
      if (place.geometry) {
        document.getElementById('drop-lat').value = place.geometry.location.lat();
        document.getElementById('drop-lng').value = place.geometry.location.lng();
      }
    });
  }
}

// Enhanced form submission
function handleFormSubmission(e) {
  e.preventDefault();
  
  // Show loading
  const loading = document.getElementById('loading');
  const successMessage = document.getElementById('successMessage');
  
  if (loading) loading.style.display = 'block';
  if (successMessage) successMessage.style.display = 'none';
  
  // Simulate API call
  setTimeout(() => {
    if (loading) loading.style.display = 'none';
    if (successMessage) successMessage.style.display = 'block';
    
    // Reset form
    const form = document.getElementById('rideForm');
    if (form) form.reset();
    
    // Set default date to today
    const dateInput = document.getElementById('date');
    if (dateInput) dateInput.value = new Date().toISOString().split('T')[0];
    
    // Hide success message after 3 seconds
    setTimeout(() => {
      if (successMessage) successMessage.style.display = 'none';
    }, 3000);
  }, 2000);
}

// Set default date to today
function setDefaultDate() {
  const dateInput = document.getElementById('date');
  if (dateInput) {
    dateInput.value = new Date().toISOString().split('T')[0];
  }
}

// Add smooth scrolling
function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
}

// Add intersection observer for animations
function initIntersectionObserver() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe all cards
  document.querySelectorAll('.ride-history-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
  });
}

// Initialize floating action button
// function initFloatingActionButton() {
//   const fab = document.querySelector('.fab');
//   if (fab) {
//     fab.addEventListener('click', function() {
//       // Scroll to form
//       const form = document.querySelector('/employee');
//       if (form) {
//         form.scrollIntoView({ behavior: 'smooth' });
//       }
//     });
//   }
// }

// Initialize logout functionality
function initLogout() {
  const logoutBtn = document.querySelector('.btn-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (confirm('Are you sure you want to logout?')) {
        // Add logout logic here
        alert('Logging out...');
        // window.location.href = 'login.html';
      }
    });
  }
}

// Initialize action buttons on ride cards
function initActionButtons() {
  // Edit buttons
  document.querySelectorAll('.btn-outline-primary').forEach(btn => {
    btn.addEventListener('click', function() {
      const card = this.closest('.ride-history-card');
      const requestId = card.querySelector('.card-header').textContent;
      alert(`Editing ${requestId}`);
    });
  });

  // Cancel buttons
  document.querySelectorAll('.btn-outline-danger').forEach(btn => {
    btn.addEventListener('click', function() {
      const card = this.closest('.ride-history-card');
      const requestId = card.querySelector('.card-header').textContent;
      if (confirm(`Are you sure you want to cancel ${requestId}?`)) {
        alert(`${requestId} cancelled`);
      }
    });
  });

  // Track buttons
  document.querySelectorAll('.btn-success').forEach(btn => {
    btn.addEventListener('click', function() {
      const card = this.closest('.ride-history-card');
      const requestId = card.querySelector('.card-header').textContent;
      alert(`Tracking ${requestId}`);
    });
  });

  // Contact buttons
  document.querySelectorAll('.btn-outline-info').forEach(btn => {
    btn.addEventListener('click', function() {
      const card = this.closest('.ride-history-card');
      const requestId = card.querySelector('.card-header').textContent;
      alert(`Contacting driver for ${requestId}`);
    });
  });

  // Reapply buttons
  document.querySelectorAll('.btn-outline-secondary').forEach(btn => {
    btn.addEventListener('click', function() {
      const card = this.closest('.ride-history-card');
      const requestId = card.querySelector('.card-header').textContent;
      if (confirm(`Reapply for ${requestId}?`)) {
        alert(`Reapplying for ${requestId}`);
      }
    });
  });

  // Feedback buttons
  document.querySelectorAll('.btn-outline-warning').forEach(btn => {
    btn.addEventListener('click', function() {
      const card = this.closest('.ride-history-card');
      const requestId = card.querySelector('.card-header').textContent;
      alert(`Opening feedback form for ${requestId}`);
    });
  });
}

// Initialize all functionality when DOM is loaded
function initApp() {
  // Set default date
  setDefaultDate();
  
  // Initialize smooth scrolling
  initSmoothScrolling();
  
  // Initialize intersection observer
  initIntersectionObserver();
  
  // Initialize floating action button
  initFloatingActionButton();
  
  // Initialize logout
  initLogout();
  
  // Initialize action buttons
  initActionButtons();
  
  // Add form submission handler
  const form = document.getElementById('rideForm');
  if (form) {
    form.addEventListener('submit', handleFormSubmission);
  }
}

// Initialize Google Maps when API is loaded
function initGoogleMaps() {
  if (typeof google !== 'undefined' && google.maps) {
    initAutocomplete();
  } else {
    // Retry after a short delay if Google Maps API is not loaded yet
    setTimeout(initGoogleMaps, 100);
  }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initApp();
  initGoogleMaps();
});

// Initialize Google Maps when window loads (fallback)
window.onload = function() {
  initGoogleMaps();
}; 