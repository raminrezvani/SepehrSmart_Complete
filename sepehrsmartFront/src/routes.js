import {createRouter, createWebHistory} from 'vue-router'

import TourSingle from "@/components/Single/TourSingle";
import LoginPage from "@/components/LoginPage";
import TourAnalysis from "@/components/Analysis/TourAnalysis";
import FlightMain from "@/components/Flight/FlightMain";
import BuildTourMain from "@/components/BuildTour/BuildTourMain";
// import App from "@/App.vue";

const routes = [
    // {
    //     path: '/',
    //     component: App,
    //     name: "index"
    // },
    {
        path: "/login",
        component: LoginPage,
        name: "login_page"
    },
    {
        path: '/single',
        component: TourSingle,
        name: "tour_single"
    },
    {
        path: '/analysis',
        component: TourAnalysis,
        name: "tour_analysis"
    },
    {
        path: '/flight',
        component: FlightMain,
        name: "flight_main"
    },
    {
        path: '/build-tour',
        component: BuildTourMain,
        name: "build_tour"
    },
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})