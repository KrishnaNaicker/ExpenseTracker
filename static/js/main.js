// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Close flash messages
    const flashCloseButtons = document.querySelectorAll('.flash-close');
    flashCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(message => {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    }, 5000);
});

// Slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation
function validateTransactionForm() {
    const form = document.getElementById('transactionForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const amount = document.getElementById('amount').value;
        const category = document.getElementById('category').value;
        const date = document.getElementById('date').value;
        
        if (!amount || parseFloat(amount) <= 0) {
            e.preventDefault();
            alert('Please enter a valid amount greater than 0');
            return false;
        }
        
        if (!category) {
            e.preventDefault();
            alert('Please select a category');
            return false;
        }
        
        if (!date) {
            e.preventDefault();
            alert('Please select a date');
            return false;
        }
    });
}

// Budget form validation
function validateBudgetForm() {
    const form = document.querySelector('.budget-form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const category = document.getElementById('category').value;
        const amount = document.getElementById('amount').value;
        
        if (!category) {
            e.preventDefault();
            alert('Please select a category');
            return false;
        }
        
        if (!amount || parseFloat(amount) <= 0) {
            e.preventDefault();
            alert('Please enter a valid budget amount greater than 0');
            return false;
        }
    });
}

// Initialize validations
document.addEventListener('DOMContentLoaded', function() {
    validateTransactionForm();
    validateBudgetForm();
});

// Format currency inputs
document.addEventListener('DOMContentLoaded', function() {
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to buttons
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            }
        });
    });
});
