/**
 * Venues Page Functionality
 * 
 * This script handles:
 * 1. Search functionality with debounce
 * 2. File upload display and validation
 * 3. Delete confirmation dialogs
 */

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  setupSearch();
  setupFileUpload();
  setupDeleteButtons();
});

/**
* Sets up the search functionality with debounce
*/
function setupSearch() {
  const searchInput = document.getElementById('search');
  
  // Search as you type with debounce (300ms delay)
  let searchTimeout;
  searchInput.addEventListener('input', function() {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(performSearch, 300);
  });

  /**
   * Filters venues based on search input
   */
  function performSearch() {
      const searchValue = searchInput.value.toLowerCase().trim();
      const venueCards = document.querySelectorAll('.venue-card');
      
      venueCards.forEach(card => {
          const venueName = card.querySelector('h3').textContent.toLowerCase();
          card.style.display = venueName.includes(searchValue) ? 'block' : 'none';
      });
  }
}

/**
* Sets up file upload display and validation
*/
// Log that the script is loaded
console.log("Venues script loaded");

// Run setup after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded");

    if (typeof setupFileUpload === 'function') {
        console.log("setupFileUpload function exists");
        setupFileUpload();
    } else {
        console.error("setupFileUpload function NOT FOUND");
    }
});


/**
 * FILE UPLOAD HANDLER
 * Provides visual feedback when user selects a file
 */

function setupFileUpload() {
    // 1. Get DOM elements
    const fileInput = document.getElementById('image');
    const fileLabel = document.querySelector('.file-label');
    const fileNameSpan = document.getElementById('file-name');

    // 2. Check if elements exist
    if (!fileInput || !fileLabel || !fileNameSpan) return;

    // 3. When file is selected
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const file = this.files[0];
            
            // 4. Update UI to show selected file
            fileNameSpan.textContent = file.name;
            fileNameSpan.style.color = '#4CAF50'; // Green text
            
            // 5. Change button appearance
            fileLabel.innerHTML = `
                <i class="fas fa-check-circle" style="color:#4CAF50"></i>
                <span>File Selected</span>
            `;
            fileLabel.style.backgroundColor = '#e8f5e9'; // Light green
            fileLabel.style.borderColor = '#4CAF50'; // Green border
            
            // 6. Basic validation (optional)
            validateFile(file);
        } else {
            // 7. Reset if no file selected
            resetFileInput();
        }
    });

    // Helper function for file validation
    function validateFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const maxSizeMB = 5;
        
        if (!validTypes.includes(file.type)) {
            showError('Invalid file type (use JPEG/PNG)');
        } else if (file.size > maxSizeMB * 1024 * 1024) {
            showError(`File too large (max ${maxSizeMB}MB)`);
        }
    }

    // Helper function to show errors
    function showError(message) {
        fileNameSpan.textContent = message;
        fileNameSpan.style.color = '#dc3545'; // Red text
        
        fileLabel.innerHTML = `
            <i class="fas fa-exclamation-circle" style="color:#dc3545"></i>
            <span>Try Again</span>
        `;
        fileLabel.style.backgroundColor = '#fde8e8'; // Light red
        fileLabel.style.borderColor = '#dc3545'; // Red border
    }

    // Helper function to reset the input
    function resetFileInput() {
        fileNameSpan.textContent = 'No file chosen';
        fileNameSpan.style.color = '#666'; // Gray text
        
        fileLabel.innerHTML = `
            <i class="fas fa-cloud-upload-alt"></i>
            <span>Choose a file</span>
        `;
        fileLabel.style.backgroundColor = '#f5f5f5'; // Original color
        fileLabel.style.borderColor = '#aaa'; // Original border
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload();
    // Your other initialization code...
});