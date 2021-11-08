function showPassword() {
    var input = document.getElementById("inputPassword");
    if (input.type === "password") {
      input.type = "text";
    } else {
      input.type = "password";
    }
  }