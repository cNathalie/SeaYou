
  const navbar = document.getElementById('navbar'); 
  const dropdown = document.getElementById('dropdownNavbar'); 
  
  const dropdownTrigger = document.getElementById('dropdownNavbarLink');
  dropdownTrigger.addEventListener('click', () =>{dropdown.classList.toggle("hidden")}); 
  
  const sandwich = document.getElementById('navbarSandwich'); 
  sandwich.addEventListener('click',() => {navbar.classList.toggle("hidden")})

  const ahoy = () => {
    const captain = document.getElementById("ahoy");
    captain.classList.toggle("hidden")
  }

