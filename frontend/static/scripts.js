$(document).ready(function() {
    $('#submitData').on('click', function() {
        console.log("started listening");
        const data = $('#editableTable tbody tr').map(function() {
            const $row = $(this);
            return {
                name: $row.find('td:eq(0)').text(), // eq(0) gets the first <td>
                email: $row.find('td:eq(1)').text(), // eq(1) gets the second <td>
                title: $row.find('td:eq(2)').text(), // eq(2) gets the third <td>
            };
        }).get(); // .get() converts the jQuery object into a regular array

        // Send the data to the Flask route
        $.ajax({
            url: '/submit-table-data',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({leads: data}),
            success: function(data) {
                console.log("successful AJAX")
                if(data.redirect) {
                    // Redirect to the URL provided by Flask
                    window.location.href = data.redirect;
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Now, place your existing code that adds event listeners inside here.
    document.querySelectorAll('.form-control').forEach(function(textArea) {
        textArea.style.height = textArea.scrollHeight + 'px';
        textArea.style.overflowY = 'hidden';
        textArea.addEventListener('input', function() {
            textArea.style.height = 'auto';
            textArea.style.height = textArea.scrollHeight + 'px';
        });
    });
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('tr').remove();
        });
    });

    document.querySelectorAll('.confirm-btn').forEach(button => {
        button.addEventListener('click', function() {
            let row = this.closest('tr');
            Array.from(row.querySelectorAll('td[contenteditable]')).forEach(cell => {
                cell.contentEditable = "false";
            });
            // Perform any additional confirmation actions here
        });
    });
    document.getElementById('confirmAll').addEventListener('click', function() {
        document.querySelectorAll('td[contenteditable="true"]').forEach(cell => {
            cell.contentEditable = "false";
            // Perform any additional confirmation actions for all rows here
        });
    });
});

document.getElementById('file-upload').addEventListener('change', function() {
    let fileName = this.files && this.files.length ? this.files[0].name : "No file chosen...";
    document.getElementById('file-upload-name').textContent = fileName;
});



/*
$(document).ready(function() {
    $('#product-form').submit(function(e) {
        e.preventDefault(); // Stop the form from submitting traditionally.

        // Corrected: Access the native form element from the jQuery object
        let formData = new FormData($('#product-form')[0]);

        $.ajax({
            url: 'http://localhost:8000/generate_emails', // Update this URL to where you want to send the form data.
            type: 'POST',
            data: formData,
            processData: false, // Important: Don't process the files
            contentType: false, // Important: Set content type to false as jQuery will tell the server its a query string request
            success: function(response) {
                console.log(response);
                // Handle success here (e.g., display a success message).
            },
            error: function(xhr, status, error) {
                console.log(error);
                // Handle error here (e.g., display an error message).
            }
        });
    });
});
*/



