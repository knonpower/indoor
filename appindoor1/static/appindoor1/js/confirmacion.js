function confirmarEliminacion(id) {
    
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
            window.location.href="/eliminar/"+id+"/";
            console.log(window.location.href);

        }
    })
}