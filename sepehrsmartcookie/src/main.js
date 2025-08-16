import {createApp} from 'vue';
import App from './App.vue';

import axios from 'axios'
import VueAxios from 'vue-axios'


axios.defaults.timeout = 1000 * 60 * 3;   // 2 minutes;
// axios.defaults.baseURL = "https://tour-collector-api.sepehrsmart.ir/";
// axios.defaults.baseURL = "http://94.74.182.183:8585/";
// axios.defaults.baseURL = "http://127.0.0.1:8585/";
// axios.defaults.baseURL = "http://188.121.102.104/";
axios.defaults.baseURL = "http://185.252.30.120:8000/";

const app = createApp(App);

app.use(VueAxios, axios);
app.mount('#app')
