function showModule(id) {
  document.querySelectorAll('.module').forEach(m => m.classList.add('d-none'));
  document.getElementById(id).classList.remove('d-none');
}

function toggleUpload() {
  const mode = document.getElementById("modeSelect").value;
  const uploadBlock = document.getElementById("uploadBlock");
  if (mode === "mutated") {
    uploadBlock.style.display = "block";
  } else {
    uploadBlock.style.display = "none";
  }
}