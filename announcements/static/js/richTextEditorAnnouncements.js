let script = document.createElement('script');
script.type = 'text/javascript';
script.referrerpolicy = "origin";
script.src = "https://cdn.tiny.cloud/1/wkonu98q7yoznsn5d3j5ike8ilcconld1jp1v4klmana1ml5/tinymce/5/tinymce.min.js";
document.head.appendChild(script);

script.onload = function() {
    tinymce.init({
        selector: "#id_announncement_message",
        height: 656,
        plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'table emoticons template paste help'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | link image | print preview media fullpage | ' +
            'forecolor backcolor emoticons | help',
        menu: {
            favs: { title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons' }
        },
        menubar: 'favs file edit view insert format tools table help',
        content_css: 'css/content.css'
    });
}