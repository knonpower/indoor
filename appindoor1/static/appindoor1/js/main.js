function crea_indoor(url){
    var $ = jQuery.noConflict();
    $("#crea_indoor").load(url, function (){
        $(this).modal('show');
    })
    
};

function plan(url){
    var $ = jQuery.noConflict();
    $("#plan").load(url, function (){
        $(this).modal('show');
    })
};

function modificar(pk){
    
    Swal.fire({
        "title":"¿Estas seguro?",
        "text":"Los datos no se podran recuperar",
        "icon":"question",
        "showCancelButton":true,
        "cancelButtonText":"No, Cancelar",
        "confirmButtonText":"Si, Eliminar",
        "confirmButtonColor":"#dc3545"
    }).then((result) => {
        if(result.value) {         
            window.location.href="/modificar/"+pk+"/";
            console.log(window.location.href);
            var $ = jQuery.noConflict();
            $("#modificar").load(url, function (){
                $(this).modal('show');
            })
        }
    })
};
