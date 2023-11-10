function previewImage(event) {
  const image = document.getElementById('imagePreview');
  image.innerHTML = '';
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function () {
    const img = document.createElement('img');
    img.src = reader.result;
    image.appendChild(img);
  };

  if (file) {
    reader.readAsDataURL(file);
  }
}

async function predictImage() {
  const fileInput = document.getElementById('imageUpload');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Prediction request failed. Status: ' + response.status);
    }

    const data = await response.json();

    if (data.image) {
      const image = document.getElementById('imagePreview');
      image.innerHTML = `<img src="${data.image}" alt="Predicted Image" style="max-width:100%;">`;
    } else {
      throw new Error('No image returned');
    }
  } catch (error) {
    console.error('Error:', error.message);
    alert('Prediction failed. Please try again.');
  }
}
