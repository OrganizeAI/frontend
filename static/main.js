// @ts-check

// selecting all required elements

/**
 * @type HTMLDivElement
 */
// @ts-ignore
const dropArea = document.querySelector(".drag-area");

/**
 * @type HTMLButtonElement
 */
// @ts-ignore
const button = dropArea.querySelector("button");

/**
 * @type HTMLButtonElement
 */
// @ts-ignore
const text = dropArea.querySelector(".ctext");

/**
 * @type HTMLInputElement
 */
// @ts-ignore
const input = dropArea.querySelector("input");

/**
 * @type File
 */
let file;

// button.onclick = () => {
//   input.click(); //if user click on the button then the input also clicked
// };

input.addEventListener("change", function () {
  console.log("change");
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  if (!this.files) {
    return;
  }
  file = this.files[0];
  dropArea.classList.add("active");
  showFile();
});

//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
  console.log("dragover");
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  // dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
  console.log("dragleave");
  dropArea.classList.remove("active");
  // dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
  console.log("drop");
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  if (!event.dataTransfer) {
    return;
  }
  file = event.dataTransfer.files[0];
  showFile();
});

function showFile() {
  input.classList.add("hidden");
  text.classList.add("hidden");
  let fileType = file.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
  if (validExtensions.includes(fileType)) {
    //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result;
      dropArea.style.backgroundImage = `url(${fileURL})`;
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    // dragText.textContent = "Drag & Drop to Upload File";
  }
}
