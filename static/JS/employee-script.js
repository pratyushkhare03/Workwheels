// Enhanced form submission
function handleFormSubmission(e) {
  e.preventDefault();
  
  // Show loading
  const loading = document.getElementById('loading');
  const successMessage = document.getElementById('successMessage');
  
  if (loading) loading.style.display = 'block';
  if (successMessage) successMessage.style.display = 'none';
  
  // Actually submit the form
  const form = e.target;
  
  // You can add validation here if needed
  const driverId = form.querySelector('select[name="driver_id"]').value;
  if (!driverId) {
    if (loading) loading.style.display = 'none';
    alert('Please select a driver');
    return;
  }
  
  // Submit the form
  form.submit();
}

// Set default date to today
function setDefaultDate() {
  const dateInput = document.getElementById('date');
  if (dateInput && !dateInput.value) {
    dateInput.value = new Date().toISOString().split('T')[0];
    // Also set min date to today
    dateInput.min = new Date().toISOString().split('T')[0];
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
function initFloatingActionButton() {
  const fab = document.querySelector('.fab');
  if (fab) {
    fab.addEventListener('click', function() {
      // Scroll to form
      const form = document.querySelector('.request-form');
      if (form) {
        form.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }
}

// Initialize action buttons on ride cards
function initActionButtons() {
  // Cancel/Delete buttons
  document.querySelectorAll('.btn-outline-danger').forEach(btn => {
    if (btn.type !== 'submit') {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const card = this.closest('.ride-history-card');
        const requestId = card ? card.querySelector('.card-header').textContent : 'this request';
        if (confirm(`Are you sure you want to cancel ${requestId}?`)) {
          // Find and submit the form
          const form = this.closest('form');
          if (form) {
            form.submit();
          }
        }
      });
    }
  });

  // Track buttons
  document.querySelectorAll('.btn-success').forEach(btn => {
    if (btn.textContent.includes('Track')) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const card = this.closest('.ride-history-card');
        const requestId = card ? card.querySelector('.card-header').textContent : '';
        alert(`Tracking ${requestId}\n\nThis feature will show real-time location tracking.`);
      });
    }
  });

  // Contact buttons
  document.querySelectorAll('.btn-outline-info').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const card = this.closest('.ride-history-card');
      const requestId = card ? card.querySelector('.card-header').textContent : '';
      alert(`Contact Driver for ${requestId}\n\nThis will open communication with the driver.`);
    });
  });

  // Edit buttons
  document.querySelectorAll('.btn-outline-primary').forEach(btn => {
    if (btn.textContent.includes('Edit')) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const card = this.closest('.ride-history-card');
        const requestId = card ? card.querySelector('.card-header').textContent : '';
        alert(`Editing ${requestId}\n\nThis feature will allow you to modify your request.`);
      });
    }
  });
}

// Handle driver selection change
function initDriverSelection() {
  const driverSelect = document.querySelector('select[name="driver_id"]');
  if (driverSelect) {
    driverSelect.addEventListener('change', function() {
      const selectedOption = this.options[this.selectedIndex];
      console.log('Selected driver:', selectedOption.text);
    });
  }
}

// Auto-hide success/error messages
function initMessageAutoHide() {
  const messages = document.querySelectorAll('.alert-message');
  messages.forEach(msg => {
    setTimeout(() => {
      msg.style.animation = 'slideOut 0.5s ease';
      setTimeout(() => {
        msg.remove();
      }, 500);
    }, 5000);
  });
}

// Initialize shift details modal
function initShiftModal() {
  const shiftModal = document.getElementById('shiftModal');
  if (shiftModal) {
    shiftModal.addEventListener('hidden.bs.modal', function () {
      const form = this.querySelector('form');
      if (form) {
        form.reset();
      }
    });
  }
}

// Validate time inputs
function initTimeValidation() {
  const timeInputs = document.querySelectorAll('input[type="time"]');
  timeInputs.forEach(input => {
    input.addEventListener('change', function() {
      // You can add custom time validation here
      console.log('Time selected:', this.value);
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
  
  // Initialize action buttons
  initActionButtons();
  
  // Initialize driver selection
  initDriverSelection();
  
  // Initialize message auto-hide
  initMessageAutoHide();
  
  // Initialize shift modal
  initShiftModal();
  
  // Initialize time validation
  initTimeValidation();
  
  // Add form submission handler
  const form = document.getElementById('rideForm');
  if (form) {
    form.addEventListener('submit', handleFormSubmission);
  }
  
  // Handle shift details form
  const shiftForm = document.querySelector('#shiftModal form');
  if (shiftForm) {
    shiftForm.addEventListener('submit', function(e) {
      // Form will submit normally, just show loading indicator
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML = '<i class="bx bx-loader bx-spin"></i> Saving...';
        submitBtn.disabled = true;
      }
    });
  }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initApp();
  console.log('Employee dashboard initialized successfully');
});

// Handle page visibility change for real-time updates
document.addEventListener('visibilitychange', function() {
  if (!document.hidden) {
    console.log('Page is now visible - you can refresh data here');
    // You can add auto-refresh logic here
  }
});