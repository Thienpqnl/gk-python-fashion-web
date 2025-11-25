/* Simple mock cart API stored in localStorage
   Exports functions: addToCart(product, qty=1), removeFromCart(productId), updateQuantity(productId, qty), getCart(), renderCart(container)
   product shape: {id, title, price, image}
*/
(function(){
  const KEY = 'fe_cart';
  function read(){
    try{ return JSON.parse(localStorage.getItem(KEY)||'{"items":[],"total":0}'); }catch(e){ return {items:[],total:0}; }
  }
  function write(cart){ localStorage.setItem(KEY, JSON.stringify(cart)); }
  function recalc(cart){ cart.total = cart.items.reduce((s,i)=>s + (i.price||0)*(i.qty||1),0); }

  window.getCart = function(){ return read(); }

  window.addToCart = function(product, qty=1){
    const cart = read();
    const idx = cart.items.findIndex(i=>i.id===product.id);
    if(idx===-1){ cart.items.push(Object.assign({qty:qty}, product)); } else { cart.items[idx].qty += qty; }
    recalc(cart); write(cart);
    // dispatch event for UI hooks
    window.dispatchEvent(new CustomEvent('cart-updated',{detail:cart}));
    return cart;
  }

  window.removeFromCart = function(productId){
    const cart = read(); cart.items = cart.items.filter(i=>i.id!==productId); recalc(cart); write(cart); window.dispatchEvent(new CustomEvent('cart-updated',{detail:cart})); return cart;
  }

  window.updateQuantity = function(productId, qty){
    const cart = read(); const it = cart.items.find(i=>i.id===productId); if(it) it.qty = Math.max(1, parseInt(qty||1,10)); recalc(cart); write(cart); window.dispatchEvent(new CustomEvent('cart-updated',{detail:cart})); return cart;
  }

  window.clearCart = function(){ localStorage.removeItem(KEY); window.dispatchEvent(new CustomEvent('cart-updated',{detail:{items:[],total:0}})); }

  window.renderCart = function(container){
    const cart = read();
    if(!container) container = document.body;
    if(cart.items.length===0){ container.innerHTML = '<div class="p-4">Giỏ hàng trống.</div>'; return; }
    const html = [`<div class="space-y-4">`];
    cart.items.forEach(i=>{
      html.push(`<div class="flex items-center gap-4"><img src="${i.image||'assets/images/product-001.svg'}" class="w-20 h-20 object-cover rounded" /><div class="flex-1"><div class="font-semibold">${i.title}</div><div class="text-sm text-gray-600">₫${i.price}</div></div><div class="flex items-center gap-2"><input type="number" value="${i.qty}" min="1" data-id="${i.id}" class="w-16 p-1 border rounded qty-input" /></div><div><button data-id="${i.id}" class="remove-btn text-red-600 text-sm">Xóa</button></div></div>`);
    });
    html.push(`<div class="pt-4 border-t flex justify-between items-center"><div class="text-lg">Tổng</div><div class="text-xl font-extrabold">₫${cart.total}</div></div>`);
    html.push('</div>');
    container.innerHTML = html.join('');
    // attach handlers
    container.querySelectorAll('.remove-btn').forEach(b=>b.addEventListener('click', e=>{ removeFromCart(e.currentTarget.dataset.id); renderCart(container); }));
    container.querySelectorAll('.qty-input').forEach(inp=>inp.addEventListener('change', e=>{ updateQuantity(e.currentTarget.dataset.id, e.currentTarget.value); renderCart(container); }));
  }

  // Listen for external add events to update storage
  window.addEventListener('add-sample', e=>{ const p=e.detail; addToCart(p,1); });

})();