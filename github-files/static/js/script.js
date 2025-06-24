// BestieAI Frontend JavaScript
// Handles interactive features and UI enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeFormValidation();
    initializeAnimations();
    initializeAccessibility();
    initializeJournalFeatures();
    
    console.log('BestieAI loaded successfully! 💕');
});

/**
 * Form validation and enhancement
 */
function initializeFormValidation() {
    // Name form validation
    const nameForm = document.querySelector('.name-form');
    if (nameForm) {
        const nameInput = nameForm.querySelector('input[name="name"]');
        const submitButton = nameForm.querySelector('button[type="submit"]');
        
        if (nameInput && submitButton) {
            nameInput.addEventListener('input', function() {
                const value = this.value.trim();
                
                // Real-time validation
                if (value.length < 2) {
                    this.classList.add('is-invalid');
                    submitButton.disabled = true;
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    submitButton.disabled = false;
                }
            });
            
            // Auto-focus on page load
            nameInput.focus();
        }
    }
    
    // Emotion form enhancement
    const emotionForm = document.querySelector('.emotion-form');
    if (emotionForm) {
        const emotionRadios = emotionForm.querySelectorAll('input[name="emotion"]');
        const customFeeling = emotionForm.querySelector('input[name="custom_feeling"]');
        const submitButton = emotionForm.querySelector('button[type="submit"]');
        
        // Handle emotion selection
        emotionRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked && customFeeling) {
                    customFeeling.value = ''; // Clear custom feeling when emotion is selected
                }
                enableSubmitButton();
            });
        });
        
        // Handle custom feeling input
        if (customFeeling) {
            customFeeling.addEventListener('input', function() {
                if (this.value.trim()) {
                    // Uncheck all emotion radios when custom feeling is entered
                    emotionRadios.forEach(radio => radio.checked = false);
                }
                enableSubmitButton();
            });
        }
        
        function enableSubmitButton() {
            const hasEmotion = Array.from(emotionRadios).some(radio => radio.checked);
            const hasCustom = customFeeling && customFeeling.value.trim();
            
            if (submitButton) {
                submitButton.disabled = !(hasEmotion || hasCustom);
            }
        }
        
        // Initial state
        enableSubmitButton();
    }
}

/**
 * Animation and visual enhancements
 */
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Floating heart animation for affirmation page
    if (document.querySelector('.affirmation-card')) {
        createFloatingHearts();
    }
    
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Create floating hearts animation for affirmation page
 */
function createFloatingHearts() {
    const heartsContainer = document.createElement('div');
    heartsContainer.className = 'floating-hearts';
    heartsContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    `;
    
    document.body.appendChild(heartsContainer);
    
    function createHeart() {
        const heart = document.createElement('div');
        heart.innerHTML = '💕';
        heart.style.cssText = `
            position: absolute;
            font-size: ${Math.random() * 20 + 15}px;
            left: ${Math.random() * 100}%;
            animation: floatUp ${Math.random() * 3 + 4}s linear infinite;
            opacity: 0.7;
        `;
        
        heartsContainer.appendChild(heart);
        
        // Remove heart after animation
        setTimeout(() => {
            if (heart.parentNode) {
                heart.parentNode.removeChild(heart);
            }
        }, 7000);
    }
    
    // Add CSS for floating animation
    if (!document.querySelector('#floating-hearts-style')) {
        const style = document.createElement('style');
        style.id = 'floating-hearts-style';
        style.textContent = `
            @keyframes floatUp {
                0% {
                    bottom: -50px;
                    transform: translateX(0px) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 0.7;
                }
                90% {
                    opacity: 0.7;
                }
                100% {
                    bottom: 100vh;
                    transform: translateX(${Math.random() * 200 - 100}px) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Create hearts periodically
    const heartInterval = setInterval(createHeart, 2000);
    
    // Stop creating hearts after 30 seconds
    setTimeout(() => {
        clearInterval(heartInterval);
    }, 30000);
}

/**
 * Accessibility enhancements
 */
function initializeAccessibility() {
    // Keyboard navigation for emotion buttons
    const emotionButtons = document.querySelectorAll('.btn-outline-emotion');
    emotionButtons.forEach((button, index) => {
        button.addEventListener('keydown', function(e) {
            let nextIndex;
            
            switch(e.key) {
                case 'ArrowRight':
                    e.preventDefault();
                    nextIndex = (index + 1) % emotionButtons.length;
                    emotionButtons[nextIndex].focus();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    nextIndex = (index - 1 + emotionButtons.length) % emotionButtons.length;
                    emotionButtons[nextIndex].focus();
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    nextIndex = Math.min(index + 4, emotionButtons.length - 1);
                    emotionButtons[nextIndex].focus();
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    nextIndex = Math.max(index - 4, 0);
                    emotionButtons[nextIndex].focus();
                    break;
            }
        });
    });
    
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'visually-hidden';
    skipLink.style.cssText = `
        position: absolute;
        top: 10px;
        left: 10px;
        z-index: 1000;
        padding: 10px;
        background: var(--accent-pink);
        color: white;
        text-decoration: none;
        border-radius: 5px;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.classList.remove('visually-hidden');
    });
    
    skipLink.addEventListener('blur', function() {
        this.classList.add('visually-hidden');
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add main content ID
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.id = 'main-content';
    }
}

/**
 * Journal page enhancements
 */
function initializeJournalFeatures() {
    const journalTextarea = document.querySelector('.journal-textarea');
    if (journalTextarea) {
        // Auto-save draft functionality
        const draftKey = 'bestieai_journal_draft';
        
        // Load draft on page load
        const savedDraft = localStorage.getItem(draftKey);
        if (savedDraft && !journalTextarea.value) {
            journalTextarea.value = savedDraft;
        }
        
        // Save draft as user types
        let saveTimeout;
        journalTextarea.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                if (this.value.trim()) {
                    localStorage.setItem(draftKey, this.value);
                } else {
                    localStorage.removeItem(draftKey);
                }
            }, 1000);
        });
        
        // Clear draft when form is submitted
        const journalForm = document.querySelector('.journal-form');
        if (journalForm) {
            journalForm.addEventListener('submit', function() {
                localStorage.removeItem(draftKey);
            });
        }
        
        // Word count display
        const wordCountDisplay = document.createElement('div');
        wordCountDisplay.className = 'word-count text-muted small mt-2';
        journalTextarea.parentNode.appendChild(wordCountDisplay);
        
        function updateWordCount() {
            const text = journalTextarea.value.trim();
            const wordCount = text ? text.split(/\s+/).length : 0;
            wordCountDisplay.textContent = `${wordCount} words`;
        }
        
        journalTextarea.addEventListener('input', updateWordCount);
        updateWordCount(); // Initial count
        
        // Auto-resize textarea
        function autoResize() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        }
        
        journalTextarea.addEventListener('input', autoResize);
        autoResize.call(journalTextarea); // Initial resize
    }
}

/**
 * Utility functions
 */

// Show loading state on form submission
document.addEventListener('submit', function(e) {
    const submitButton = e.target.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        
        // Re-enable button after 5 seconds in case of network issues
        setTimeout(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
        }, 5000);
    }
});

// Smooth scrolling for anchor links
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

// Add ripple effect to buttons
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');
    
    const ripple = button.querySelector('.ripple');
    if (ripple) {
        ripple.remove();
    }
    
    button.appendChild(circle);
}

// Apply ripple effect to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', createRipple);
});

// Add ripple CSS
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);