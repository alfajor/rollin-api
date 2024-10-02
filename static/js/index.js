const form = document.getElementById('form');
const emailField = document.querySelector('.email-field');
const validationMessage = document.querySelector('.validation-message');

const formHandler = (e) => {
    const re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    const isValidEmail = re.test(String(emailField.value).toLowerCase())

    validationMessage.style.color = 'red';

    if(emailField.value == '') {
        e.preventDefault();
        validationMessage.textContent = '* Email is required';
    } else if(!isValidEmail) {
        e.preventDefault();
        validationMessage.textContent = '* Invalid email';
    } else {
        // we're posting
        validationMessage.textContent = '';
    }
}
form.addEventListener('submit', formHandler)

// alt to post redirect
if(window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href + '')
}
