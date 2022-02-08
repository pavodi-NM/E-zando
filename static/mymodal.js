
const card_products = document.getElementById('table-box')
$.ajax({
    type:'GET',
    url: 'vendor-form-enregistrement/',
    success:function(response){
        console.log(response)
        const data = JSON.parse(response.data)
        console.log(data)
        data.forEach(el => {
            console.log(el.fields)
            card_products.innerHTML += `
            <tr>
            <td>media/${el.fields.pk}</td>
            <td>media/${el.fields.imageProduit}</td>
            <td>media/${el.fields.tittreProduit}</td>
            </tr>
            `
        })
    },
    error:function(error){
        console.log(error)

    }
})