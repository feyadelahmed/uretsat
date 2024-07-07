const imgInput = document.querySelector("#imginput");
const img = document.querySelector("img.preview");

imgInput.addEventListener("change", e => {
    if (imgInput.files.length > 0) {
        const fileReader = new FileReader();
        fileReader.onload = event => {
            img.setAttribute('src', event.target.result);
        }
        fileReader.readAsDataURL(imgInput.files[0]);
    }
});