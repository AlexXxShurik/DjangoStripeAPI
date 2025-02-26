document.addEventListener("DOMContentLoaded", function () {
    const buyButtonSession = document.getElementById("buy-button-session");
    const buyButtonIntent = document.getElementById("buy-button-payment-intent");

    // Логика для Stripe Checkout Session
    if (buyButtonSession) {
        buyButtonSession.addEventListener("click", function () {
            const objectType = buyButtonSession.dataset.objectType;
            const objectId = buyButtonSession.dataset.objectId;
            const stripeKey = buyButtonSession.dataset.stripeKey;

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

    // Логика для Stripe Payment Intent
    if (buyButtonIntent) {
        // Инициализация Stripe
        const stripe = Stripe(buyButtonIntent.dataset.stripeKey);

        // Создаем элементы Stripe для ввода карты
        const elements = stripe.elements();
        const cardElement = elements.create("card", {
            style: {
                base: {
                    fontSize: "16px",
                    color: "#32325d",
                    fontFamily: "Arial, sans-serif",
                    "::placeholder": {
                        color: "#aab7c4",
                    },
                },
                invalid: {
                    color: "#fa755a",
                },
            },
        });

        // Монтируем элемент для ввода карты
        cardElement.mount("#card-element");

        // Обработка ошибок ввода карты
        const cardErrors = document.getElementById("card-errors");
        cardElement.on("change", function (event) {
            if (event.error) {
                cardErrors.textContent = event.error.message;
            } else {
                cardErrors.textContent = "";
            }
        });

        // Обработка нажатия на кнопку "Купить" для Payment Intent
        buyButtonIntent.addEventListener("click", async function () {
            const objectType = buyButtonIntent.dataset.objectType;
            const objectId = buyButtonIntent.dataset.objectId;

            if (!objectId) {
                console.error("Object ID is undefined.");
                return;
            }

            let url;
            if (objectType === "item") {
                url = `/create-payment-intent/${objectId}/`;
            } else if (objectType === "order") {
                url = `/create-payment-intent-for-order/${objectId}/`;
            } else {
                console.error("Invalid object type.");
                return;
            }

            try {
                // Получаем client_secret от сервера
                const response = await fetch(url, {
                    method: "GET",
                });
                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                // Подтверждаем платеж
                const { paymentIntent, error } = await stripe.confirmCardPayment(data.client_secret, {
                    payment_method: {
                        card: cardElement,
                    },
                });

                if (error) {
                    // Показываем ошибку
                    cardErrors.textContent = error.message;
                } else if (paymentIntent.status === "succeeded") {
                    // Перенаправляем на страницу успешного платежа
                    window.location.href = "/success/";
                }
            } catch (error) {
                console.error("Error:", error);
                cardErrors.textContent = "An error occurred. Please try again.";
            }
        });
    }
});