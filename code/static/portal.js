$(document).ready(()=>{
    let checkValue = $('#info-tab input');

    for( ele of checkValue ){
        if(ele.value === "None" || ele.value === ""){
            ele.value = "Still Empty";
        }
    }
});