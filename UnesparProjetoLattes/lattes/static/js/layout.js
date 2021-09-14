function Limpar(){
    window.location.href = '?';
}

function menuCurrentOption(){
    const pathname = window.location.pathname;
    document.querySelectorAll('.links a').forEach( link =>{
        if( pathname == link.pathname){
            link.style.background = 'darkgray';
            link.style.margin = '0 10px 0';
            link.style.borderRadius = '5px';
            return;
        }
    });
}

document.addEventListener('DOMContentLoaded', ()=>{
    const btn_sidebar = document.querySelector('.drop-btn-sidebar');
    const sidebar = document.querySelector('.sidebar'); 
    const wrapper = document.querySelectorAll(".wrapper");
    
    menuCurrentOption();
    
    document.querySelectorAll('.fa-plus-circle').forEach(plus=>{
        plus.addEventListener('clik', ()=>{
            plus.dataset.icon = 'minus-circle'
        });
    });

    document.querySelectorAll('.fa-minus-circle').forEach(plus=>{
        plus.addEventListener('clik', ()=>{
            plus.dataset.icon = 'plus-circle'
        });
    });
    
    document.querySelectorAll('.drop-bnt').forEach((button, index)=>{

        if (wrapper[index].style.display == 'none') {
            wrapper[index].style.display = 'block'
        } else {
            wrapper[index].style.display = 'none'
        }

        button.onclick = (() => {
            if (wrapper[index].style.display == 'none') {
                wrapper[index].style.display = 'block'
                if (button.innerHTML.search('fa-plus-circle') != -1) {
                    button.children[0].children[0].dataset.icon = 'minus-circle';
                }
            } else {
                wrapper[index].style.display = 'none'
                if (button.innerHTML.search('fa-minus-circle') != -1) {
                    button.children[0].children[0].dataset.icon = 'plus-circle';
                }
            }
            button.classList.toggle("rotate");
        });
    });


    btn_sidebar.onclick = (() => {
        sidebar.classList.toggle("hide");
    });
});