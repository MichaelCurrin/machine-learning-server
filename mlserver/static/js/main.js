function previewImage() {
    $('#imagePreview').html("<img src='" + URL.createObjectURL(event.target.files[0])+"' height='90'><br>");
}
