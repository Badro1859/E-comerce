

/******************** manage the update buttons  **********************/
updateBtns = document.getElementsByClassName('update-cart');

for (i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('product:',productId, 'action:', action);
        if (user == "AnonymousUser"){
            console.log("User is not athenticated");
            addCookieItem(productId, action);
        }else{
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log("User is athenticated, sending data...");

    var url = '/update-item/';
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'productId':productId,
            'action':action,
        }),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        if (data['remove']){
            location.reload();
        }
        else{
            // for the nav cart icon
            document.getElementById('cart-total').textContent = data['total-items'];
            
            // in the cart page 
            document.getElementById('total-price').textContent = '$'+ data['total-price'];
            document.getElementById('total-items').textContent = data['total-items'];
            var id = data['item-id'];
            document.getElementById('qte-'+id).textContent = data['item-quantity'];
            document.getElementById('price-'+id).textContent = '$'+ data['item-price'];
        }
    });
}

function addCookieItem(productId, action) {

    if(action == 'add') {
       if(cart[productId] == undefined) {
            cart[productId] = {'quantity':1};
       }else{
            cart[productId]['quantity'] += 1
       }
    }

    if(action == 'remove') {
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0) {
            delete cart[productId]   
        }
    } 
    console.log('cart', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/;';
}

/******************** manage the cart cookie for not logged user  **********************/

var cart = JSON.parse(getCookie('cart'));
if (cart == undefined) {
    cart = {};
    console.log('Cart Created!', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/;';
}
console.log('cart', cart);


function getCookie(name) {
    // split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(';');
    
    // loop through the array elements
    for (var i=0; i<cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split('=');
        
        // removing whitespace at the beginning of the cookie
        // name and compare it with the given name
        if (name == cookiePair[0].trim()) {
            // decode the value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    // return null if not found
    return null;
}