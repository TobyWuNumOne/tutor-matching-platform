<template>
    <div class="tt123">
        <div class="div1">
            <img src="../assets/customer-service-headset.png">
            <h2>家教媒合平台</h2>
        </div>
        <div class="carddiv">
        <div class="logincard">
            <form>
                <div>
                    <p>歡迎回來</p>
                </div>
                <div>
                    <p>請輸入帳號密碼</p>
                </div>
                <div>
                    <p>帳號</p>
                    <input type="email">
                    <p>密碼</p>
                    <input type="password">
                </div>
                <div>
                    <input type="checkbox">記住我
                    <Router-Link to="">忘記帳號密碼</Router-Link>
                </div>
                <div>
                    <button>登入</button>
                    <hr/>
                    <button>使用Google登入</button>
                </div>
                <div>
                    <p>
                        還沒有帳戶嗎？
                        <Router-Link to="/register">註冊一個吧！</Router-Link>
                    </p>
                </div>
            </form>
        </div>
    </div>  
    </div>
    
</template>

<script>
import { RouterLink } from 'vue-router';

</script>

<style scoped>
    .tt123{
        position: relative;
    }
    .div1{
        width: 270px;
        height: 100px;
        display: flex;
        gap: 20px;
        align-items: center;
        /* 定位 */
        position: absolute;
        top: 0;
        left: 0;
    }
/* logo樣式 */
    img{
        width:  90px;
        height: 90px;
    }
    .carddiv{
        width: 100vw;
        height: 50vw;
        background-color: aqua;
        display: flex;
        justify-content: center;
    }
    .logincard{
        width: 500px;
        height: 550px;
        border: 1px solid black;
        background-color: rgba(213, 213, 213, 0.63) ;
    }
</style>