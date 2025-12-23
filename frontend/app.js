const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewContainer = document.getElementById('previewContainer');
const loadingOverlay = document.getElementById('loadingOverlay');
const tagsContainer = document.getElementById('tagsContainer');
const resultsContent = document.getElementById('resultsContent');
const emptyState = document.getElementById('emptyState');
const timeTaken = document.getElementById('timeTaken');

// Role Switcher Logic
const roleSelector = document.getElementById('roleSelector');
const userView = document.getElementById('userView');
const adminView = document.getElementById('adminView');
const removeBtn = document.getElementById('removeBtn');

// Reset/Remove Image Logic
removeBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent triggering upload zone click if needed, though this is separate
    resetState();
});

function resetState() {
    fileInput.value = ''; // Clear file input
    imagePreview.src = '';
    previewContainer.style.display = 'none';
    resultsContent.style.display = 'none';
    emptyState.style.display = 'block';
    // Clear tags
    tagsContainer.innerHTML = '';
}

roleSelector.addEventListener('change', (e) => {
    if (e.target.value === 'admin') {
        userView.style.display = 'none';
        adminView.style.display = 'grid'; // Maintain grid layout
    } else {
        userView.style.display = 'grid';
        adminView.style.display = 'none';
    }
});

// Drag & Drop Events
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
});

dropZone.addEventListener('drop', handleDrop, false);
fileInput.addEventListener('change', (e) => handleFiles(e.target.files), false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            uploadAndAnalyze(file);
        } else {
            alert("Please upload an image file.");
        }
    }
}

async function uploadAndAnalyze(file) {
    // Show Preview
    const reader = new FileReader();
    reader.onload = function (e) {
        imagePreview.src = e.target.result;
        previewContainer.style.display = 'block';
    }
    reader.readAsDataURL(file);

    // Show Loading
    loadingOverlay.style.display = 'flex';
    emptyState.style.display = 'none';
    resultsContent.style.display = 'none';

    // Prepare FormData
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis.');
    } finally {
        loadingOverlay.style.display = 'none';
    }
}

function displayResults(data) {
    resultsContent.style.display = 'block';
    tagsContainer.innerHTML = '';

    // Animate tags entry
    data.tags.forEach((tag, index) => {
        const tagEl = document.createElement('div');
        tagEl.className = 'tag';
        // Add style for animation delay
        tagEl.style.animationDelay = `${index * 0.1}s`;
        tagEl.textContent = `${tag.label} (${Math.round(tag.confidence * 100)}%)`;
        tagsContainer.appendChild(tagEl);
    });

    timeTaken.textContent = data.processing_time.toFixed(3);
}

// 3D Tilt Effect Logic
const cards = document.querySelectorAll('.card');

cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -5; // Max rotation 5deg
        const rotateY = ((x - centerX) / centerX) * 5;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        // Re-apply slideUp animation preference if needed, or just reset to flat
        card.style.transition = 'transform 0.5s ease';
    });

    // Reset transition after mouse enter to make movement responsive
    card.addEventListener('mouseenter', () => {
        card.style.transition = 'none';
    });
});

