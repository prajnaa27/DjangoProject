document.getElementById('payNowBtn').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('guestInfoModal').style.display = 'flex';
  });

  function closeGuestModal() {
    document.getElementById('guestInfoModal').style.display = 'none';
  }