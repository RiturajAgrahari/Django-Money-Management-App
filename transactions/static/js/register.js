var usernameField = document.getElementById("usernameField");
var emailField = document.getElementById("emailField");
var feedbackArea = document.getElementById("feedbackField");
var emailfeedbackArea = document.getElementById("emailfeedbackField");
var usernameSuccessOutput = document.getElementById("usernameSuccessOutput")
var emailSuccessOutput = document.getElementById("emailSuccessOutput")
var showPasswordToggle = document.getElementById("showPasswordToggle")
var passwordField = document.getElementById("passwordField")
var submitBtn = document.getElementById('submitButton')


showPasswordToggle.addEventListener("click", function(e) {
    console.log('working')
    if (showPasswordToggle.textContent==="SHOW") {
        showPasswordToggle.textContent = "HIDE"
        passwordField.setAttribute("type", "text");
    }
    else {
        showPasswordToggle.textContent = "SHOW"
        passwordField.setAttribute("type", "password");
    }
});



usernameField.addEventListener("keyup", function(e) {
    var usernameVal = e.target.value;

    usernameSuccessOutput.style.display= "block"

    usernameSuccessOutput.textContent=`Checking  ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";

    if (usernameVal.length > 0) {
    fetch('/authentication/validate-username',{
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
    }).then(res=>res.json()).then(data=>{
        usernameSuccessOutput.style.display= "none"
        if (data.username_error) {
            submitBtn.setAttribute('disabled', 'disabled');
            submitBtn.disabled = true;
            usernameField.classList.add("is-invalid");
            feedbackArea.style.display = "block";
            feedbackArea.innerHTML=`<p>${data.username_error}<p>`;
        }
        else {
            submitBtn.removeAttribute('disabled');

        }
    });
    }
    console.log('usernameVal', usernameVal);
});

emailField.addEventListener("keyup", function(e) {

    var emailVal = e.target.value;

    emailSuccessOutput.style.display= "block"

    emailSuccessOutput.textContent=`Checking  ${emailVal}`

    emailField.classList.remove("is-invalid");
    emailfeedbackArea.style.display = "none";

    if (emailVal.length > 0) {
    fetch('/authentication/validate-email',{
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
    }).then(res=>res.json()).then(data=>{
        emailSuccessOutput.style.display= "none"
        if (data.email_error) {
            submitBtn.setAttribute('disabled', 'disabled');
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            emailfeedbackArea.style.display = "block";
            emailfeedbackArea.innerHTML=`<p>${data.email_error}<p>`;
        }
        else {
            submitBtn.removeAttribute('disabled');
        }
    });
    }
    console.log('emailVal', emailVal);
});


