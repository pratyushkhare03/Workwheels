// Initialize all functionality when DOM is loaded
function initDriverApp() {
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
  
  // Initialize current ride functionality
  initCurrentRide();
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
  document.querySelectorAll('.ride-card, .current-ride-card').forEach(card => {
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
      // Show quick actions menu
      showQuickActions();
    });
  }
}

// Show quick actions menu
function showQuickActions() {
  const actions = [
    { icon: 'bx bx-map', text: 'View Map', action: () => alert('Opening map...') },
    { icon: 'bx bx-phone', text: 'Call Support', action: () => alert('Calling support...') },
    { icon: 'bx bx-cog', text: 'Settings', action: () => alert('Opening settings...') }
  ];

  // Create quick actions menu
  const menu = document.createElement('div');
  menu.className = 'quick-actions-menu';
  menu.style.cssText = `
    position: fixed;
    bottom: 100px;
    right: 30px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 1rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    z-index: 999;
    display: none;
  `;

  actions.forEach(action => {
    const button = document.createElement('button');
    button.className = 'btn btn-outline-primary d-block w-100 mb-2';
    button.innerHTML = `<i class='${action.icon}'></i> ${action.text}`;
    button.addEventListener('click', action.action);
    menu.appendChild(button);
  });

  document.body.appendChild(menu);
  
  // Show menu
  menu.style.display = 'block';
  
  // Hide menu after 3 seconds
  setTimeout(() => {
    menu.remove();
  }, 3000);
}

// Initialize logout functionality
function initLogout() {
  const logoutBtn = document.querySelector('.btn-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (confirm('Are you sure you want to logout?')) {
        showMessage('Logging out...', 'success');
        setTimeout(() => {
          // Add logout logic here
          alert('Logged out successfully');
          // window.location.href = 'login.html';
        }, 1000);
      }
    });
  }
}

// Initialize action buttons on ride cards
function initActionButtons() {
  // Accept buttons
  document.querySelectorAll('.btn-accept').forEach(btn => {
    btn.addEventListener('click', function() {
      const requestId = this.getAttribute('data-request-id');
      const card = this.closest('.ride-card');
      
      if (confirm(`Accept ride request #${requestId}?`)) {
        // Simulate API call
        showLoading(card);
        
        setTimeout(() => {
          hideLoading(card);
          showMessage(`Ride request #${requestId} accepted successfully!`, 'success');
          
          // Update card appearance
          card.style.borderColor = '#28a745';
          card.querySelector('.card-header').style.background = 'linear-gradient(45deg, #28a745, #20c997)';
          
          // Disable buttons
          card.querySelectorAll('.btn-accept, .btn-reject').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
          });
          
          // Add accepted indicator
          const indicator = document.createElement('div');
          indicator.className = 'accepted-indicator';
          indicator.innerHTML = '<i class="bx bx-check-circle"></i> Accepted';
          indicator.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
          `;
          card.style.position = 'relative';
          card.appendChild(indicator);
        }, 2000);
      }
    });
  });

  // Reject buttons
  document.querySelectorAll('.btn-reject').forEach(btn => {
    btn.addEventListener('click', function() {
      const requestId = this.getAttribute('data-request-id');
      const card = this.closest('.ride-card');
      
      if (confirm(`Reject ride request #${requestId}?`)) {
        // Simulate API call
        showLoading(card);
        
        setTimeout(() => {
          hideLoading(card);
          showMessage(`Ride request #${requestId} rejected.`, 'info');
          
          // Fade out card
          card.style.transition = 'opacity 0.5s ease';
          card.style.opacity = '0.5';
          
          // Disable buttons
          card.querySelectorAll('.btn-accept, .btn-reject').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
          });
        }, 1500);
      }
    });
  });
}

// Initialize current ride functionality
function initCurrentRide() {
  const completeRideBtn = document.querySelector('.current-ride-card .btn-success');
  const callPassengerBtn = document.querySelector('.current-ride-card .btn-outline-primary');
  
  if (completeRideBtn) {
    completeRideBtn.addEventListener('click', function() {
      if (confirm('Complete this ride?')) {
        showMessage('Ride completed successfully!', 'success');
        
        // Update progress bar
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
          progressBar.style.width = '100%';
          progressBar.textContent = '100% Complete';
        }
        
        // Disable button
        this.disabled = true;
        this.innerHTML = '<i class="bx bx-check-circle"></i> Completed';
        this.style.background = '#6c757d';
      }
    });
  }
  
  if (callPassengerBtn) {
    callPassengerBtn.addEventListener('click', function() {
      showMessage('Calling passenger...', 'info');
      // Add actual call functionality here
    });
  }
}

// Show loading state
function showLoading(element) {
  const loading = document.createElement('div');
  loading.className = 'loading-overlay';
  loading.innerHTML = `
    <div class="spinner"></div>
    <p>Processing...</p>
  `;
  loading.style.cssText = `
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
    border-radius: 15px;
  `;
  
  element.style.position = 'relative';
  element.appendChild(loading);
}

// Hide loading state
function hideLoading(element) {
  const loading = element.querySelector('.loading-overlay');
  if (loading) {
    loading.remove();
  }
}

// Show message
function showMessage(text, type = 'success') {
  const messageElement = document.getElementById('successMessage');
  const messageText = document.getElementById('messageText');
  
  if (messageElement && messageText) {
    messageText.textContent = text;
    
    // Update icon based on type
    const icon = messageElement.querySelector('i');
    if (icon) {
      switch (type) {
        case 'success':
          icon.className = 'bx bx-check-circle';
          messageElement.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
          break;
        case 'error':
          icon.className = 'bx bx-error-circle';
          messageElement.style.background = 'linear-gradient(45deg, #dc3545, #c82333)';
          break;
        case 'info':
          icon.className = 'bx bx-info-circle';
          messageElement.style.background = 'linear-gradient(45deg, #17a2b8, #138496)';
          break;
        default:
          icon.className = 'bx bx-check-circle';
          messageElement.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
      }
    }
    
    messageElement.style.display = 'block';
    
    // Hide message after 3 seconds
    setTimeout(() => {
      messageElement.style.display = 'none';
    }, 3000);
  }
}

// Auto-update progress bar
function updateProgressBar() {
  const progressBar = document.querySelector('.progress-bar');
  if (progressBar) {
    let progress = parseInt(progressBar.style.width) || 65;
    
    setInterval(() => {
      if (progress < 100) {
        progress += Math.random() * 5;
        progress = Math.min(progress, 100);
        progressBar.style.width = progress + '%';
        progressBar.textContent = Math.round(progress) + '% Complete';
      }
    }, 5000); // Update every 5 seconds
  }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initDriverApp();
  updateProgressBar();
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Ctrl/Cmd + Enter to accept first pending request
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const firstAcceptBtn = document.querySelector('.btn-accept:not([disabled])');
    if (firstAcceptBtn) {
      firstAcceptBtn.click();
    }
  }
  
  // Escape to close any open modals/menus
  if (e.key === 'Escape') {
    const quickMenu = document.querySelector('.quick-actions-menu');
    if (quickMenu) {
      quickMenu.remove();
    }
  }
}); 