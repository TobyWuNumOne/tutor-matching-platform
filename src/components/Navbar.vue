<template>
    <nav>
        <div>
            <!-- logo -->
            <img src="../assets/customer-service-headset.png">
            <p class="title">家教媒合平台</p>
        </div> 
        <div></div>
        <div>
            <!-- 下拉式選單 -->
            <select>
                <option v-for="(item , i) in languages" :key="i">{{ item }}</option>
            </select>

            <!-- 登入登出按鈕(含判斷式'尚未建立') -->
            <Router-link to="/login">
                <button class="navbtn"v-if="login == false">登入</button>
                <button class="navbtn" v-else>登出</button>
            </Router-link>
            
            
        </div>
    </nav>
</template>

<script>
    export default{
        data(){
            return{
                // 語言陣列
                languages : [
                    '繁體中文(TW)',
                    '簡體中文(CN)',
                    '英文(ENG)',
                    '日文(JPN)',   
                ],
                login : false
            }   
        }   
    }
</script>

<style>
/* 導航欄 */
    nav{
        width: 100vw;
        height: 110px;
        background-color: #3F3FF0;
        position: sticky;
        top: 0;
        border-radius: 0 0 10px 10px ;
        display: flex;
        justify-content:space-between;   /* 讓內部水平置中 */
        align-items: center;       /* 讓內部垂直置中 */
    }
    nav div{
        display: flex;
        align-items: center;       /* 讓內部垂直置中 */
        gap: 20px;
        margin: 10px;
    }
/* 導航欄文字 */
    .title{
        color: white;
        font-size: 24px;
    }
/* logo樣式 */
    img{
        width:  90px;
        height: 90px;
        filter: invert(1);
    }
/* 下拉式選單 */
    select{
        border: 0;
        font-size: 18px;
        color: white;
        background-color: #3F3FF0;
    }
    select:hover{
        cursor: pointer;
    }
/* 按鈕樣式 */
    .navbtn{
        width: 98px;
        height: 40px    ;
        border: 1px solid white;
        background-color: #3F3FF0;
        color: white;
        border-radius: 8px;
    }
    .navbtn:hover{
        background-color: white;    
        color: #3F3FF0;
        cursor: pointer;
    }
</style>