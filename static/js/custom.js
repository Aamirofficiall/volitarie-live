var $ = jQuery.noConflict();

// deleteDataFromCSV
var csvDATA=''
function convertWholeDataToCSV(data){
    html_data=``
    try{

        if (data['data'].length>0)
        {
            for( var i in data['data'])
            {
                console.log(data['data'][i]['id'])
                html_data+=`
                <tr class='mb-3' id='hiring${data['data'][i]['id']}'>
                    <td>${data['data'][i]['id']}</td>
                    <td>${data['data'][i]['company_name']}</td>
                    <td>${data['data'][i]['location']}</td>
                    <td><i class='far fa-trash-alt text-danger deleteDataFromCSV' onclick=" onDeleteEvent(${data['data'][i]['id']})" dataID='${data['data'][i]['id']}'  style='font-size: 20px;'></i></td>
                </tr> `

                
            }
            const csvString = [
                [
                "ID",
                "title",
                "Title",
                "Location",
                "url",
                "company_name",
                "company_rating",
                "company_date",
                "keywords",

                ],
                ...data['data'].map(item => [
                item.id,
                item.title,
                item.location,
                item.url,
                item.company_name,
                item.company_rating,
                item.creation_date,
                item.keywords,
                ])
            ]
            .map(e => e.join(",")) 
            .join("\n");
            
            localStorage.setItem("csvDATA", csvString);
            
            console.log(data)
            document.getElementById('loader').style.display = "none";
        
            var table=document.getElementById('csvTable')

            table.innerHTML=html_data


            // var pom = document.createElement('a');

            var blob = new Blob([localStorage.getItem('csvDATA')],{type: 'text/csv;charset=utf-8;'});
            var url = URL.createObjectURL(blob);

            var downloadTag=`<a  href='${url}' download='data.csv'> 
            &nbsp;
            <i class="fas fa-download text-info "></i>
            </a>`

            document.getElementById('FileLink').innerHTML=''
            $('#FileLink').append(downloadTag)

        }
    }
    catch(err) {
        document.getElementById('loader').style.display = "none";
        document.getElementById('noHiringRechord').style.display = "none";

        document.getElementById('noHiringRechordFound').style.display = "block";
}

}

function convertWholeDataToCSVlinkdIn(data){

    const csvString = [
        [
        "name",
        "profile_url",
        "school",
        "job_position",
        "company",
        "location",
        "city",
        "weather",
        "university",
        "news",
        "summay",
        "CTA",
        "signature_outro",

        ],
        ...data['data'].map(item => [
        item.name,
        item.profile_url,
        item.school,
        item.job_position,
        item.company,
        item.location,
        item.city,
        item.weather,
        item.university,
        item.news,
        item.summay,
        item.CTA,
        item.signature_outro,
        ])
    ]
    .map(e => e.join(",")) 
    .join("\n");

    var blob = new Blob([csvString],{type: 'text/csv;charset=utf-8;'});
    var url = URL.createObjectURL(blob);

    var downloadTag=`<a href='${url}' download='data.csv' class="btn btn-primary " style='border-radius: 10px !important; min-width: 120px;'>
    Download <i class="fas fa-download  "></i>
    </a>`


    
    document.getElementById('launch-button').innerHTML=''
    $('#launch-button').append(downloadTag)

}

function onDeleteEvent(idToSearchFor)
{
  
    data=localStorage.getItem('csvDATA')
    let linesExceptFirst = data.split('\n').slice(1);
    let linesArr = linesExceptFirst.map(line=>line.split(','));

    console.log(idToSearchFor)
    let output = linesArr.filter(line=>parseInt(line[0]) !== parseInt(idToSearchFor)).join("\n");
    localStorage.setItem("csvDATA", output);
    document.getElementById('hiring'+idToSearchFor).style.display = "none";
    var pom = document.createElement('a');

    console.log(localStorage.getItem("csvDATA"))
    var blob = new Blob([localStorage.getItem("csvDATA")],{type: 'text/csv;charset=utf-8;'});
    var url = URL.createObjectURL(blob);

    var downloadTag=`<a  href='${url}' download='data.csv'> 
                        &nbsp;
                        <i class="fas fa-download text-info "></i>
                        </a>`

    document.getElementById('FileLink').innerHTML=''
    $('#FileLink').append(downloadTag)


    

}

function objToCsv(data) {
    const headers = Object.keys(data[0]).join();
    const content = data.map(r => Object.values(r).join());
    return [headers].concat(content).join("\n");
}

try{
document.getElementById("hiring-form").addEventListener("submit", function(event){
    event.preventDefault()
    var keyword=event.target.keyword.value
    var token=event.target.csrfmiddlewaretoken.value
    document.getElementById('loader').style.display = "block";
    document.getElementById('noHiringRechord').style.display = "none";
    document.getElementById('noHiringRechordFound').style.display = "none";

    var formData = new FormData();
    formData.append('csrfmiddlewaretoken',token)
    formData.append('keyword',keyword)
    console.log(token)
    var table=document.getElementById('csvTable')

    table.innerHTML=''
    if (keyword !='')
    {
        $.ajax({
            type: 'POST',
            url: '/hiring/getHiringByTextInput/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (data) {

                convertWholeDataToCSV(data)
            }
            ,
            error: function (error) {
                console.log('error in hiring api for scrapp data',error)
            }
        });
        
    }

  });


}
catch {
    console.log('hiring error')

}



$(document).ready(function () {
try{

    // hiring form
    $(".hiring").change(function (event) {
        document.getElementById('loader').style.display = "block";
        document.getElementById('noHiringRechord').style.display = "none";
        document.getElementById('noHiringRechordFound').style.display = "none";

        event.preventDefault();
        var formData = new FormData();
        console.log(event)
        var tk = document.getElementsByName('csrfmiddlewaretoken')
        tk=tk[0].defaultValue

        formData.append('file', $('#file')[0].files[0])
        formData.append('csrfmiddlewaretoken',tk)
        var table=document.getElementById('csvTable')

        table.innerHTML=''

        $.ajax({
            type: 'POST',
            url: '/hiring/getHiring/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (data) {

                convertWholeDataToCSV(data)

            }
            ,
            error: function (error) {
                console.log('error in hiring api for scrapp data',error)
            }
        });

    });
}
catch {
    console.log('hiring error')

}


    
});

var inputs = document.querySelectorAll('.inputfile');
Array.prototype.forEach.call(inputs, function (input) {
    var label = input.nextElementSibling,
        labelVal = label.innerHTML;
    try{

    input.addEventListener('change', function (e) {
        var fileName = '';
        if (this.files && this.files.length > 1)
            fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
        else
            fileName = e.target.value.split('\\').pop();

        if (fileName)
            label.querySelector('strong').innerHTML = fileName;
        else
            label.innerHTML = labelVal;
    });
}
catch{
    
}

});


// linkdin part (personlization)

$(document).ready(function () {

    // hiring form
    $(".linkdin").change(function (event) {
        document.getElementById('loader').style.display = "block";
        document.getElementById('noLinkedInRechord').style.display = "none";
        document.getElementById('noLinkedInRechordFound').style.display = "none";

        event.preventDefault();
        var formData = new FormData();
        console.log(event)
        var tk = document.getElementsByName('csrfmiddlewaretoken')
        tk=tk[0].defaultValue

        formData.append('file', $('#file')[0].files[0])
        formData.append('csrfmiddlewaretoken',tk)
    

        $.ajax({
            type: 'POST',
            url: '/linkdin/getLinkdin/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (data) {
                
                document.getElementById('loader').style.display = "none";
                
                var results=''
                var header = "name,profile_url,school,job_position,company,location,city,weather,university,news,summay,CTA,signature_outro"
                // results = results+header+'\n'

                convertWholeDataToCSVlinkdIn(data)


    
                
            }
            ,
            error: function (error) {
                console.log('error in hiring api for scrapp data',error)
                
                document.getElementById('loader').style.display = "none";
                document.getElementById('noLinkedInRechord').style.display = "none";
                document.getElementById('noLinkedInRechordFound').style.display = "block";
        
            }
        });

    });



    
});

