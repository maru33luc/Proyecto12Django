$(function() {
    // Hide the doctor availability form by default
    $('#doctor-availability-form').hide();
  
    // Show the doctor availability form when a doctor is selected
    $('select#id_doctor').change(function() {
      var doctor_id = $(this).val();
      if (doctor_id) {
        $('#doctor-availability-form').show();
      } else {
        $('#doctor-availability-form').hide();
      }
    });
  
    // Submit the doctor availability form via AJAX and display the available slots
    $('#doctor-availability-form form').submit(function(e) {
      e.preventDefault();
      var form = $(this);
      $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: form.serialize(),
        success: function(response) {
          if (response.available_slots.length > 0) {
            var slots_html = '<ul>';
            $.each(response.available_slots, function(i, slot) {
              slots_html += '<li>' + slot + '</li>';
            });
            slots_html += '</ul>';
            $('#doctor-availability-form').append(slots_html);
          } else {
            $('#doctor-availability-form').append('<p>No available slots for the selected date.</p>');
          }
        },
        error: function() {
          $('#doctor-availability-form').append('<p>An error occurred while checking availability.</p>');
        }
      });
    });
  });
  