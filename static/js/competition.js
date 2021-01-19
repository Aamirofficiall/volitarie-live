$(document).ready(function () {



    $(".competition").change(function (event) {

        event.preventDefault();
        var formData = new FormData();
        console.log(event)
        var tk = document.getElementsByName('csrfmiddlewaretoken')
        tk = tk[0].defaultValue

        formData.append('file', $('#file')[0].files[0])
        formData.append('csrfmiddlewaretoken', tk)

        $.ajax({
            type: 'POST',
            url: '/competition/getCompetition/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (data) {
                console.log(data)
                var pom = document.createElement('a');
                var csvContent = data;
                var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                var url = URL.createObjectURL(blob);
                pom.href = url;
                pom.setAttribute('download', 'data.csv');
            }
            ,
            error: function (error) {
                console.log('error in hiring api for scrapp data', error)
            }
        });

    });

    
});