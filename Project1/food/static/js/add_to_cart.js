// Main cart functionality for the food ordering system

function addToCart(button) {
  const itemName = button.getAttribute('data-name');
  const itemPrice = button.getAttribute('data-price');
  const itemSlug = itemName.toLowerCase().replace(/\s+/g, '-');

  fetch(`/add_to_cart/${itemName}/`, {
    method: 'POST',
    body: new URLSearchParams({
      'quantity': 1,
      'price': itemPrice
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      const controlsContainer = document.getElementById(`cart-controls-${itemSlug}`);
      
      // Replace with quantity controls
      controlsContainer.innerHTML = `
        <button class="cart-btn decrement-btn" onclick="decrement('${itemName}', this)" data-item="${itemName}">-</button>
        <span class="quantity-display" id="quantity-${itemSlug}">${data.quantity || data.cart[itemName].quantity}</span>
        <button class="cart-btn increment-btn" data-name="${itemName}" data-price="${itemPrice}" onclick="addToCart(this)">+</button>
      `;
    }
  })
  .catch(console.error);
}

function decrement(itemName, button) {
  const itemSlug = itemName.toLowerCase().replace(/\s+/g, '-');
  
  fetch(`/decrement_cart/${itemName}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      if (data.deleted) {
        // Item was completely removed, show "Add to cart" button
        const controlsContainer = document.getElementById(`cart-controls-${itemSlug}`);
        // const itemPrice = button.closest('.menu-content').querySelector('.cart-btn[data-price]')?.getAttribute('data-price') || '';
        const itemPrice = button.getAttribute('data-price') || '';
        
        controlsContainer.innerHTML = `
          <button class="add-to-cart-btn" data-name="${itemName}" data-price="${itemPrice}" onclick="addToCart(this)">
            Add to cart
          </button>
        `;
      } else {
        // Update quantity
        const quantityElement = document.getElementById(`quantity-${itemSlug}`);
        if (quantityElement) {
          quantityElement.innerText = data.quantity;
        }
      }
    }
  })
  .catch(console.error);
}

// Cart page specific functions
function incrementInCart(itemName, button) {
  const itemPrice = button.getAttribute('data-price');
  
  fetch(`/add_to_cart/${itemName}/`, {
    method: 'POST',
    body: new URLSearchParams({
      'quantity': 1,
      'price': itemPrice
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Reload the page to update all cart information
      location.reload();
    }
  })
  .catch(console.error);
}

function decrementInCart(itemName, button) {
  fetch(`/decrement_cart/${itemName}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      // Reload the page to update all cart information
      location.reload();
    }
  })
  .catch(console.error);
}

function removeFromCart(itemName) {
  if (confirm(`Are you sure you want to remove ${itemName} from your cart?`)) {
    fetch(`/remove_from_cart/${itemName}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        // Remove the entire row from the table
        const itemSlug = itemName.toLowerCase().replace(/\s+/g, '-');
        const row = document.getElementById(`cart-row-${itemSlug}`);
        if (row) {
          row.remove();
        }
        
        // Reload page to update totals and check if cart is empty
        location.reload();
      }
    })
    .catch(console.error);
  }
}

function clearCart() {
  if (confirm('Are you sure you want to clear your entire cart?')) {
    fetch('/clear_cart/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        // Don't show alert, just reload to show empty cart message
        location.reload();
      } else {
        alert('Error clearing cart. Please try again.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error clearing cart. Please try again.');
    });
  }
}