async function cart_update(e) {
    const {data} = await axios(e.dataset.url)
    const {message, items_count} = data
    notyf.success({
            message,
            dismissible : true,
            icon : false,
        } 
    )
    document.getElementById('cart-items-count').innerHTML = items_count;
}

async function cart_remove_funcjs(e) {
    await axios(e.dataset.url)
    location.reload()
}