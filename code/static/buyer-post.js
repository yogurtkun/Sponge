function isNormalInteger(str) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
}

var image = new Vue({
    el: '#uploadImage',
    data: {
        imageName:"Select file..."
    },
    methods:{
        updateFile: function(event){
            let imageinput =  $('#InputImage').prop('files')

            if(imageinput.length !== 0)
                this.imageName = imageinput[0].name;
        }
    }
});

(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                let imageinput =  $('#InputImage').prop('files')

                if(imageinput.length !== 0 && imageinput[0].size >= 51200){
                    alert("Image too large");
                    event.preventDefault();
                    event.stopPropagation();
                }

                if (imageinput.length !== 0 &&imageinput[0].type !== 'image/jpeg' && imageinput[0].type !== 'image/png' && imageinput[0].type !== 'image/gif') {
                    alert('The type of file is incorrect!');
                    event.preventDefault();
                    event.stopPropagation();
                }

                let price = $('input[name=price]')[0].value;
                if( !isNormalInteger(price) && price !== ""){
                    alert("Price incorrect");
                    event.preventDefault();
                    event.stopPropagation();
                }

                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();