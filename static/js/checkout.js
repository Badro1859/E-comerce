

if (document.getElementById('form') != null) { 
    var form = document.getElementById('form');
    form.addEventListener('submit', function(e){
    e.preventDefault();
    console.log('Form submitted ...');
    document.getElementById('form-button').classList.add('hidden');
    document.getElementById('payment-info').classList.remove('hidden');
    });
}else{
    document.getElementById('payment-info').classList.remove('hidden');
}



function submitFormData() {
    console.log('payment btn clicked ...');

    var userFormData = {
        'name':null,
        'email':null,
    };

    var shippingInfo = {
        'address':null,
        'city':null,
        'state':null,
        'zipcode':null,
    };

    if (document.getElementById('user-info')) {
        userFormData.name = form.name.value;
        userFormData.email = form.name.value;
    }

    if(document.getElementById('shipping-info')) {
        shippingInfo.address = form.address.value;
        shippingInfo.city = form.city.value;
        shippingInfo.state = form.state.value;
        shippingInfo.zipcode = form.zipcode.value;
    }

    var url = "/process-order/";
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'form':userFormData,
            'shipping':shippingInfo,
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Successs:", data);
        alert('Transaction completed');

        // clear cart for unauthenticated users
        cart = {};
        document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/;';
        
        // redirect to home page
        window.location.href = "/";
    })

}