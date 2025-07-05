<template>
    <div class="footer row">
        <div class="footer-links">
            <Router-link to="/about">關於我們</Router-link>
            <Router-link to="">幫助中心／常見問題</Router-link>
            <Router-link to="">服務條款</Router-link>
            <Router-link to="">隱私權政策</Router-link>
            <Router-link to="">Cookie 使用政策</Router-link>
            <Router-link to="">無障礙瀏覽／無障礙設計</Router-link>
            <Router-link to="">用戶回饋</Router-link>
        </div>
    </div>
</template>

<script>
    export default {}
</script>

<style scoped> 
    .footer {
        width: 100vw;
        height: 80px;
        background-color: #3F3FF0;
        position: fixed;
        bottom: 0;
        border-radius: 10px 10px 0 0;
        display: flex;
        justify-content: center;   /* 讓內部水平置中 */
        align-items: center;       /* 讓內部垂直置中 */
    }

    .footer-links {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
        width: 90vw;               /* 設定寬度 */
    }

    .footer-links a{
        font-size: 16px;           /* 文字大小 */
        color: white;            /* 文字顏色 */
        text-decoration: none;     /* 移除底線 */
    }
</style>