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

function mostrarSenha(){

	var tipo = document.getElementById('senha');
	const btn = document.querySelector('.icon');

	if (tipo.type == 'password') 
	{
		tipo.type = 'text'
		btn.src = 'static/imagens/eye-off.svg'
	}
	else
	{
		tipo.type = 'password'
		btn.src = 'static/imagens/eye.svg'
	}
}

function mostrarSenha1(){

	var tipo1 = document.getElementById('senha1');
	const btn1 = document.querySelector('.icon1');

	if (tipo1.type == 'password') 
	{
		tipo1.type = 'text'
		btn1.src = '/static/imagens/eye-off.svg'
	}
	else
	{
		tipo1.type = 'password'
		btn1.src = '/static/imagens/eye.svg'
	}
}