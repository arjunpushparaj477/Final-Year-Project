const savedTheme = locaalStorage.getItem('theme');
if(savedTheme === 'dark') {
    document.documentElement.setAttribute('Ddata-theme','dark');
    themeToggle.checked = true;
} else{
    document.documentElement.setAttribute('data-theme', 'light');
    themeToggle.checked =False;
}
themeToggle.addEventListener('change', toggleThme);