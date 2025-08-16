import App from './App.vue';
import * as Vue from 'vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vue3PersianDatetimePicker from 'vue3-persian-datetime-picker'
import vSelect from 'vue-select';
import {router} from "@/routes";
import VueApexCharts from "vue3-apexcharts";
import {store} from "@/store";
const app = Vue.createApp(App);

const access_token = localStorage.getItem("access_token");
axios.defaults.timeout = 1000 * 60 * 3;   // 2 minutes
// axios.defaults.baseURL = "https://tour-collector-api.sepehrsmart.ir/";
// axios.defaults.baseURL = "https://smarttravelback.iotstream.ir/";
axios.defaults.baseURL = "http://185.252.30.120:8000/";
// axios.defaults.baseURL = "http://127.0.0.1:8765/";
// 
// axios.defaults.baseURL = "http://94.74.182.183:8585/";

axios.defaults.headers.post['Authorization'] = access_token;
axios.defaults.headers.get['Authorization'] = access_token;

app.use(VueAxios, axios);
app.use(router);
app.use(VueApexCharts);
app.use(store)
app.component('v-select', vSelect);

app.use(Vue3PersianDatetimePicker, {
    name: 'DatePicker',
    props: {
        format: 'YYYY-MM-DD',
        displayFormat: 'jYYYY-jMM-jDD', 
        editable: false,
        inputClass: 'form-control my-custom-class-name',
        placeholder: 'تاریخ',
        altFormat: 'YYYY-MM-DD HH:mm',
        color: '#0dcaf0',
        autoSubmit: true,
    }
})

app.mount('#app');
