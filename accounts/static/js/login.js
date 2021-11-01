function myFunctions() {
    let x = document.getElementById("id_password");
    let y = document.getElementById("hide1");
    let z = document.getElementById("hide2");

    if (x.type === 'password') {
        x.type = "text";
        y.style.display = "block";
        z.style.display = "none";
    } else {
        x.type = "password";
        y.style.display = "none";
        z.style.display = "block";
    }
}

function login_func1() {
    var x = document.getElementById("id_new_password1");
    var y = document.getElementById("hide11");
    var z = document.getElementById("hide21");

    if (x.type === 'password') {
        x.type = "text";
        y.style.display = "block";
        z.style.display = "none";
    } else {
        x.type = "password";
        y.style.display = "none";
        z.style.display = "block";
    }
}

function login_func2() {
    let x = document.getElementById("id_new_password2");
    let y = document.getElementById("hide12");
    let z = document.getElementById("hide22");

    if (x.type === 'password') {
        x.type = "text";
        y.style.display = "block";
        z.style.display = "none";
    } else {
        x.type = "password";
        y.style.display = "none";
        z.style.display = "block";
    }
}