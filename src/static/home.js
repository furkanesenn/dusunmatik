const link = document.querySelector('div.comments > a.material-symbols-outlined')

function shareIdea() {
    navigator.clipboard.writeText(link);
    
}