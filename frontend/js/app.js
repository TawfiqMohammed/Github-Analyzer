// Analyze repository
function analyzeRepo() {
    const repoUrl = document.getElementById('repoUrl').value;
    
    // Basic validation
    if (!repoUrl) {
        alert('Please enter a GitHub repository URL');
        return;
    }
    
    if (!repoUrl.includes('github.com')) {
        alert('Please enter a valid GitHub URL');
        return;
    }
    
    // For now, just show alert (we'll implement API call later)
    alert('Analysis starting! (Full implementation coming soon)\n\nRepo: ' + repoUrl);
}

// Handle Enter key
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('repoUrl');
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                analyzeRepo();
            }
        });
    }
});