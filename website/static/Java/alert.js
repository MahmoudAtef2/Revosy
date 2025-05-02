/**
 * Handles flash message animations and removal
 * 
 * This script waits for the DOM to load, then sets a timeout to:
 * 1. Add fade-out animation to all alert messages
 * 2. Remove them from the DOM after animation completes
 */
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.animation = 'fadeOut 0.5s ease-in-out forwards';
            setTimeout(() => alert.remove(), 500);
        });
    }, 2000); // Messages disappear after 2 seconds
});