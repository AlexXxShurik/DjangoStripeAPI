document.addEventListener("DOMContentLoaded", function () {
    const buyButton = document.getElementById("buy-button");

    if (buyButton) {
        buyButton.addEventListener("click", function () {
            const objectType = buyButton.dataset.objectType; // "item" или "order"
            const objectId = buyButton.dataset.objectId;     // ID товара или заказа
            const stripeKey = buyButton.dataset.stripeKey;  // Публичный ключ Stripe

            // Проверяем, что objectId определён
            if (!objectId) {
                console.error("Object ID is undefined.");
                return;
            }

            // Определяем URL для запроса
            let url;
            if (objectType === "item") {
                url = `/buy/${objectId}/`;  // Для оплаты товара
            } else if (objectType === "order") {
                url = `/buy_order/${objectId}/`;  // Для оплаты заказа
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