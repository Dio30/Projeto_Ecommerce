var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var produtoId = this.dataset.product
        var action = this.dataset.action
        console.log('produtoId:', produtoId, 'action:', action)

        console.log('User:', user)
        if (user == 'AnonymousUser'){
            console.log('Usuario não está autenticado.')
        }else{
            updateUserPedido(produtoId, action)
        }
    })
}

function updateUserPedido(produtoId, action){
    console.log('Usuario está autenticado, enviando dados ...')
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'produtoId': produtoId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('Dados:', data)
        location.reload()
    })
}