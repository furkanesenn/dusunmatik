const textArea = document.querySelector('textarea.idea'),
previewArea = document.querySelector('p.reason')

textArea.addEventListener('input', inputChange)

function inputChange() {
    textArea.value != '' ? previewArea.textContent = textArea.value: previewArea.innerHTML = 'Yorumunuzu yazmaya başladığınızda burada ön-görünüm bulunacak.'
}