document.addEventListener ('DOMContentLoaded', function () {
let wrongButtons = document.querySelectorAll('.incorrect');
var rightButton = document.querySelector('.correct');
var example = document.querySelector('#option-1');
var check = document.querySelector('.check-button');
console.log(example);
var clicked = false;
var trigger;

for (var i = 0; i < wrongButtons.length; i++)
{

    wrongButtons[i].addEventListener('click', function (event) {
        if (clicked == true)
        {
            reset();
        }

         trigger = event.target;
        trigger.style.backgroundColor = 'red';
        document.querySelector('#feedback').innerText = 'Incorrect';
        clicked = true;
    })
}

rightButton.addEventListener('click', function () {
    if (clicked == true)
    {
        reset();
    }
    rightButton.style.backgroundColor = 'green';
    document.querySelector('#feedback').innerText = 'Correct!';
    clicked = true;
    trigger = rightButton;
})

function reset()
{ if (trigger.id == 'option-1')
{
trigger.style.backgroundColor = 'rgb(229, 143, 157)';
}
else if (trigger.id == 'option-3')
{
    trigger.style.backgroundColor = 'rgb(149, 184, 169)';
}
else if (trigger.id == 'option-4')
{
    trigger.style.backgroundColor = 'rgb(206, 188, 151)';
}
else if (trigger.id == 'option-5')
{
    trigger.style.backgroundColor = 'rgb(206, 151, 204)';
}
else
{
    rightButton.style.backgroundColor = 'rgb(140, 158, 191)';
}
}

check.addEventListener('click', function() {
    var input = document.querySelector('.check');
    console.log(input);
    var answer = input.value;
    console.log(answer);
    if (answer.toUpperCase() == 'WALTER MORRISON' || answer.toUpperCase() == 'WALTER FREDERICK MORRISON')
    {
        input.style.backgroundColor = 'green';
        document.querySelector('.free-response-feedback').innerText = 'Correct!';
    }
    else {
        input.style.backgroundColor = 'red';
        document.querySelector('.free-response-feedback').innerText = 'Incorrect';
    }
})
})
