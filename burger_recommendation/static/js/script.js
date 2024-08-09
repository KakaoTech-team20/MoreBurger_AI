document.getElementById('userSelect').addEventListener('change', function() {
    const userId = this.value;
    if (userId) {
        fetch(`/recommend/${userId}`)
            .then(response => response.json())
            .then(data => {
                const recommendationsDiv = document.getElementById('recommendations');
                recommendationsDiv.innerHTML = '';

                // 사용자 정보 표시
                const userInfoDiv = document.createElement('div');
                userInfoDiv.className = 'user-info';
                userInfoDiv.innerHTML = `
                    <h2>사용자 정보</h2>
                    <p>사용자 ID: ${data.user.UserID}</p>
                    <p>성별: ${data.user.Gender}</p>
                    <p>연령대: ${data.user['Age Group']}</p>
                    <p>매운맛 선호: ${data.user['Spicy Preference']}</p>
                    <p>알레르기: ${data.user.Allergies}</p>
                    <p>선호 섭취량: ${data.user['Consumption Size']}</p>
                    <p>이전 주문: ${data.user['Previous Orders'].join(', ')}</p>
                `;
                recommendationsDiv.appendChild(userInfoDiv);

                // 햄버거 추천 목록 표시
                const burgersDiv = document.createElement('div');
                burgersDiv.className = 'burgers-list';
                data.burgers.forEach(burger => {
                    const burgerCard = document.createElement('div');
                    burgerCard.className = 'burger-card';
                    burgerCard.innerHTML = `
                        <h3>${burger.rank}. ${burger.Name}</h3>
                        <img src="${burger.image}" alt="${burger.Name}" onerror="this.src='/static/images/burger_images/default.webp'">
                        <p>금액: ${burger.Price}원</p>
                        <p>유사도: ${burger.Similarity.toFixed(4)}</p>
                        <p>우선순위: ${burger.Priority}</p>
                        <p>이전 주문 횟수: ${burger.order_count}</p>
                        <p>매운 맛: ${burger.spicy}</p>
                    `;
                    burgersDiv.appendChild(burgerCard);
                });
                recommendationsDiv.appendChild(burgersDiv);
            });
    }
});