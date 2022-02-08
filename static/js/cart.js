var updateBtns = document.getElementsByClassName("update-cart")


for(var i = 0; i < updateBtns.length; i++){
        updateBtns[i].addEventListener('click', function (){
            var productId = this.dataset.product
            var action = this.dataset.action
            console.log('productId',productId, 'action', action)

            console.log('USER:', user)
            if (user==='AnonymousUser'){
                console.log('Not logged in')
            }else{
                updateUserCart(productId, action)
            }
        })
}

function updateUserCart(productId, action){
    console.log('User is logged in....')
    var url = '/update-cart/'

    fetch(url, {
        method: 'POST',
        headers:{
            'content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response)=>{
            return response.json()
        })

        .then((data)=>{
            console.log('data:',data)
        })
}