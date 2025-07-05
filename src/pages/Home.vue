<script setup>
import Navbar from '../components/Navbar.vue'
</script>

<template>
    <Navbar/>
    <div class="motivation">
        <h1>"引導學生，成就未來"</h1>
    </div>
    <div class="div2">
       <div class="homefeedback" v-for="(item , i) in stdfeedbacks" :key="i">
            <h3>{{ item.title }}</h3>
            <p class="content">{{ item.content }}</p>

            <!-- 判斷式 -->
            <p class="students" v-if="item.role === 'std'">-- {{ item.student }} 同學</p>
            <p class="tutor" v-else>-- {{ item.tutor }} 家教</p>
       </div> 
    </div>
    <div class="div3">
        <Router-link to="">
            <button class="homebtn">立即開始，與你的專屬家教見面！</button>
        </Router-link>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                stdfeedbacks:[
                    {
                        title: '非常完美!!', 
                        content: '「這個平台幫我找到超合適的數學家教，才幾個禮拜，我的成績就大大進步了！」',
                        student: 'Cody',
                        role:'std'
                    },
                    {
                        title: '精準媒合!!', 
                        content: '「作為一位家教老師，我非常欣賞這個平台的便利性，能輕鬆與學生互動並追蹤他們的學習成果，值得推薦！',
                        tutor: 'Shen',
                        role:'teacher'
                    },
                    {
                        title: '有許多人受惠!!', 
                        content: '「互動式工具加上量身打造的課程，讓學習變得超有趣，真的是我做過最棒的決定！」',
                        student: 'Alex',
                        role:'std'
                    },
                ]
            }
        }
    };
</script>

<style scoped>
    .motivation{
        width: 100vw;
        height: 100px;
        display: flex;
        justify-content: center;
    }

    .div2 {
        width: 100vw;
        height: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
    } 
    .homefeedback{
        width: 300px;
        height: 200px;
        word-wrap: break-word;
        border: 1px solid black;
        border-radius: 25px;
        position: relative; 
        padding: 8px;
    }
    .homefeedback h3 {
        color: rgb(106, 31, 255);
        text-align: center;
        margin-bottom: 10px;
        font-size: 1.3rem;
    }
    .content{
        font-size: 1.1rem;
    }
    .students , .tutor{
        position: absolute;
        bottom: 10px;
        right: 15px;
        font-size: 1.05 rem;
    }
    /* 開始按鈕 */
    .div3{
        width: 100vw;
        height: 15% ;
        display: flex;
        justify-content: center;
        align-items: center ;
        gap: 30px;
        padding: auto;
    } 
    .homebtn{
        width: 600px;
        height: 90px;
        border: 0;
        background-color: #3F3FF0;
        border-radius: 15px;
        color: white;
    }
    .homebtn:hover{
       
        cursor: pointer;
    }
</style>