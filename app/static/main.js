const dropArea = document.getElementById('uploadBox');
dragText = dropArea.querySelector('header');
button = dropArea.querySelector('button');
input = document.getElementById('uploadImage');

const resultBox = document.getElementById('resultBox');
button.onclick = () => {
    input.click();
}

input.addEventListener('change', function() {
    uploadFile = this.files[0];
    dropArea.classList.add('active');
    resultBox.innerHTML = "<div class='icon'><i class='fas fa-grin-wink'></i></div>";
    showFile();
    
});

dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropArea.classList.add('active');
    dragText.textContent = 'Release to upload';
});

dropArea.addEventListener("dragleave", ()=>{
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

dropArea.addEventListener("drop", (event)=>{
    event.preventDefault(); //preventing from default behaviour
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    uploadFile = event.dataTransfer.files[0];
    resultBox.innerHTML = "<div class='icon'><i class='fas fa-grin-wink'></i></div>";
    showFile(); //calling function
});

function showFile(){
    let fileType = uploadFile.type; //getting selected file type
    let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
    if(validExtensions.includes(fileType)){ //if user selected file is an image file
      let fileReader = new FileReader(); //creating new FileReader object
      fileReader.onload = ()=>{
        let fileURL = fileReader.result; //passing user file source in fileURL variable
          // UNCOMMENT THIS BELOW LINE. I GOT AN ERROR WHILE UPLOADING THIS POST SO I COMMENTED IT
        console.log(fileURL);
        let imgTag = `<img src="${fileURL}" name="image">`; //creating an img tag and passing user selected file source inside src attribute
        dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
      }
      
      fileReader.readAsDataURL(uploadFile);
    }else{
      alert("This is not an Image File!");
      dropArea.classList.remove("active");
      dragText.textContent = "Drag & Drop to Upload File";
    }
  }