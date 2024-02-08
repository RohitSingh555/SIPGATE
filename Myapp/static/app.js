



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

        // function pollForIncomingCall() {
        //   setInterval(function () {
        //     axios
        //       .get("/check-incoming-call/")
        //       .then(function (response) {
        //         if (response.data.incomingCall) {
        //           $("#incomingCallModal").modal("show");
    
        //           if (response.data.message === 'In contacts') {
        //             $("#incomingCallModal .modal-body").html(
        //               '<h5 class="font-weight-bold">You have an incoming call from</h5>' +
        //               '<div class="d-flex align-items-center">' +
        //               '<h4 class="me-3"><i class="fas fa-user"></i>' + ' ' + response.data.ContactName + '</h4>' +
        //               '<h6 class="fw-bold">' + '&nbsp;' + response.data.contactNumber + '</h6>' +
        //               '</div>'
        //             );
        //           } else {
        //             $("#incomingCallModal .modal-body").html(
        //               '<h4 class="font-weight-bold">Incoming call from an Unknown Number!</h4>' +
        //               '<h6 class="fw-bold">Contact Number: ' + response.data.contactNumber + '</h6>'
        //             );
        //           }
    
        //         }
        //       })
        //       .catch(function (error) {
        //         console.error("Error polling for incoming call:", error);
        //       });
        //   }, 5000);
        // }
    
        // // Rest of your existing JavaScript code remains unchanged
    
    
        // function snoozeModal() {
        //   $("#incomingCallModal").modal("hide");
        // }
    
        // $(document).ready(function () {
        //   pollForIncomingCall();
        // });
    
        // function redirectToCall() {
        //   window.location.href = "/incoming-call";
        // }