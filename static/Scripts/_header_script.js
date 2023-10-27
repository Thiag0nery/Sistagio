 var local_url =window.location.pathname;
var cadastro_header = document.getElementById("cadastro_header");
var login_header = document.getElementById("login_header");
var home_header = document.getElementById("home_header");
var logout_header = document.getElementById("logout_header");
var perfil_header = document.getElementById("perfil_header");
 document.addEventListener("DOMContentLoaded", function() {
   
if (local_url === "/cadastro/"){
                              cadastro_header.style.color = "Blue"
}
if (local_url === "/"){
   home_header.style.color = "Blue"
}
if (local_url === "/login/"){
   login_header.style.color = "Blue"
}
 if (local_url === "/perfil/"){
   perfil_header.style.color = "Blue"
   logout_header.style.visibility = 'visible'

}

});