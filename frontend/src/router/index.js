import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import About from "../pages/About.vue";
import LoginPage from "../pages/LoginPage.vue";
import Register from "../pages/Register.vue";
import Search from "../pages/Search.vue";
import PersonalDashboard from "../pages/PersonalDashboard.vue";
import TeacherDashboard from "../pages/TeacherDashboard.vue";
import TeacherInfoPage from "../pages/TeacherInfoPage.vue";
import Booking from "../pages/Booking.vue";
import RegisterTeacher from "../pages/RegisterTeacher.vue";
import CourseForm from "../pages/CourseForm.vue";
import ReviewForm from "../pages/ReviewForm.vue";


const routes = [
    {
        path: "/",
        component: Home,
    },
    {
        path: "/about",
        component: About,
    },
    {
        path: "/login",
        component: LoginPage,
    },
    {
        path: "/register",
        component: Register,
    },
    {
        path: "/search",
        component: Search,
    },
    {
        path: "/personaldashboard",
        component: PersonalDashboard,
    },
    {
        path: "/teacherdashboard",
        component: TeacherDashboard,
    },
    {
        path: "/teacher/:teacherName",
        component: TeacherInfoPage,
    },
    {
        path: "/booking",
        component: Booking,
    },
    {

        path: "/register-teacher",
        component: RegisterTeacher,

        path: "/courseform",
        component: CourseForm,
    },
    {
        path: "/reviewform",
        component: ReviewForm,

    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
