
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
  }


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
                }
            }
            }
            return cookieValue;
        }


function callPhoneNumber(button) {
  var phoneNumber = button.parentNode.textContent.trim();
  document.getElementById('phoneInput').value = phoneNumber;

  var callingMessage = document.getElementById('callingMessage');
  callingMessage.style.display = 'block';
  setTimeout(function() {
      callingMessage.style.display = 'none';
  }, 10000);
  document.getElementById('callButton').click();
}

function updateDOM(userData) {
  $('#userid').text(userData.id);
  $('#username').text(userData.name);
  $('#phone-number').text(userData.phone_number);
  $('#caller').text(userData.caller);
  $('#caller-id').text(userData.caller_id);
  $('#user-token').text(userData.user_token); 
}

