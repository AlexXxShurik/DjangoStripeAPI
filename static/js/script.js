document.addEventListener("DOMContentLoaded", function () {
    const buyButton = document.getElementById("buy-button");

    if (buyButton) {
        buyButton.addEventListener("click", function () {
            const objectType = buyButton.dataset.objectType;
            const objectId = buyButton.dataset.objectId;
            const stripeKey = buyButton.dataset.stripeKey;

            if (!objectId) {
                console.error("Object ID is undefined.");
                return;
            }

            let url;
            if (objectType === "item") {
                url = `/buy/${objectId}/`;
            } else if (objectType === "order") {
                url = `/buy_order/${objectId}/`;
            } else {
                console.error("Invalid object type.");
                return;
            }

            fetch(url, {
                method: "GET",
            })
                .then((response) => response.json())
                .then((data) => {
                    const stripe = Stripe(stripeKey);
                    return stripe.redirectToCheckout({ sessionId: data.session_id });
                })
                .then((result) => {
                    if (result.error) {
                        alert(result.error.message);
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        });
    }
});