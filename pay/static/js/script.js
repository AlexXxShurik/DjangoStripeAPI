document.addEventListener("DOMContentLoaded", function () {
    const buyButton = document.getElementById("buy-button");

    if (buyButton) {
        buyButton.addEventListener("click", function () {
            fetch(`/buy/${buyButton.dataset.itemId}/`)
                .then(response => response.json())
                .then(data => {
                    var stripe = Stripe(buyButton.dataset.stripeKey);
                    stripe.redirectToCheckout({ sessionId: data.session_id });
                })
                .catch(error => console.error("Error:", error));
        });
    }
});
