const container = document.querySelector('#codeContainer')
const inputs = document.querySelectorAll('.code')
const verify = document.querySelector('.btnn')

const isAllInputFilled = () => {
    return Array.from(inputs).every((input) => input.value);
};

const getOtpText = () => {
    let text = '';
    inputs.forEach(input => {
        text += input.value;
    });

    return text;
}

const verifyOTP = () => {
    if(isAllInputFilled()) {
        const OTP = getOtpText();
    }
};

const toggleFilledClass = (field) => {
    if (field.value) {
        field.classList.add("filled")
    }else {
        field.classList.remove("filled")
    }
}

container.addEventListener('input', (e) => {
    const target = e.target;
    const value = target.value;
    toggleFilledClass(target);
    if (target.nextElementSibling) {
        target.nextElementSibling.focus();
    }
    verifyOTP();
});

inputs.forEach((input, currentIndex) => {
    toggleFilledClass(input);


    //paste event
    input.addEventListener("paste", (e) => {
        e.preventDefault();
        const text = e.clipboardData.getData("text");
        inputs.forEach((item, index) => {
            //cl -> 2
            if (index >= currentIndex && text[index - currentIndex]) {
                item.focus();
                item.value = text[index - currentIndex] || "";
                toggleFilledClass(item);
                verifyOTP();
            }
        });
    });

    //backspace event
    input.addEventListener("keydown", (e) => {
        if (e.keyCode === 8) {
            e.preventDefault();
            input.value = "";
            toggleFilledClass(input);
            if (input.previousElementSibling) {
                input.previousElementSibling.focus();
            }else {
                if (input.value && input.nextElementSibling) {
                    input.nextElementSibling.focus();
                }
            }
        }
    });
});

