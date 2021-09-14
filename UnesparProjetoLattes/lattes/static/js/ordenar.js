document.addEventListener('DOMContentLoaded', ()=>{
    const ordenar = document.querySelector('#ordenar');
    const url_str = window.location.href;
    const url = new URL(url_str);
    const param = url.searchParams.get('ordenar');
    ordenar.childNodes.forEach(option => {
        if (option.value === param) {
            ordenar.selectedIndex = option.index;
        }
    });
    ordenar.onchange = ()=>{
        const event = new Event('submit');
        document.querySelector('#filtro').dispatchEvent(event);
    };
});