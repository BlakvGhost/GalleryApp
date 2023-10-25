"use script"

const allowDrop = (ev) =>  ev.preventDefault()

const dragStart = (ev) => {
    
    ev.dataTransfer.setData("text/plain", ev.target.id);
}

const dropIt = (ev, to) => {

    ev.preventDefault();  
    let sourceId = ev.dataTransfer.getData("text/plain");
    let sourceIdEl=document.getElementById(sourceId);
    let sourceIdParentEl=sourceIdEl.parentElement;

    let targetEl=document.getElementById(ev.target.id)
    let targetParentEl=targetEl.parentElement;
  

    
    if (targetParentEl.id!==sourceIdParentEl.id){

        if (targetEl.className === sourceIdEl.className ){

           targetParentEl.appendChild(sourceIdEl);
         
        } else{            
             targetEl.appendChild(sourceIdEl);
        }

        sourceIdEl.setAttribute('data-task-status', to)
        window.service.update(sourceIdEl, to)
       
    } 
    else{

        try {

            let holder = targetEl;

            let holderText = holder.outerHTML;

            targetEl.outerHTML = sourceIdEl.outerHTML;

            sourceIdEl.outerHTML = holderText;
            holderText='';

        } catch (e) {
            return;
        };
    }
    
}

document.querySelectorAll('.drag-card').forEach((e,i) => {
    e.addEventListener('ondragstart', dragStart)
})
