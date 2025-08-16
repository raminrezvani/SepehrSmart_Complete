import {createStore} from 'vuex';

export const store = createStore({
    state() {
        return {
            app_version: 1.06,
            user: {
                access_token: "",
                first_name: "",
                last_name: ""
            },
            disable_header_link: false,
            build_tour_data: {
                body: {
                    "start_date": '',
                    "end_date": "",
                    "night_count": 0,
                    "hotel_star": 5,
                    "source": "MHD",
                    "target": "KIH",
                    "adults": 2
                },
                data: {
                    flight: {
                        "go_flight": [],
                        "return_flight": [],
                    },
                    "hotel": []
                },
                loading: false,
                show_result: false,
                datepicker_min_date: "",
                minimum_date: ""
            },
            ready_tour_data: {
                show_analysis: false,
                loading_analysis: false,
                analysis_data: [],
                order_by: "price_a",
                show_provider: false,
                filter_provider: {
                    // alibaba: true,
                    // booking: true,
                    // Snapp:true,
                    // alwin: true,
                    // deltaban: true,
                    // sepid_parvaz: true,
                    // dayan: true,
                    // mehrab: true,
                    // rahbal: true,
                    // tak_setare: true,
                    // hrc: true,
                    // omid_oj: true,
                    // parmis: true,
                    // kimiya:true,
                    // Jimboo :true,
                    // eram2mhd:true,
                    // hamood:true,
                    // safiran:true,
                    // darvishi:true,
                    // moeindarbari:true,


                                    
                    "Mehrab Seir":true,
                    Eram2MHD:true,
                    eram2mhd:true,
                    
                    mehrab:true,
                    HRC:true,
                    hrc: true,
                    Kimiya:true,
                    kimiya: true,
                    "Tak Setare":true,
                    "Tak Setareh":true,
                    tak_setare:true,
                    Parmis:true,
                    parmis:true,
                    Rahbal:true,
                    rahbal:true,
                    Safiran:true,
                    safiran:true,
                    "Omid Oj":true,
                    omid_oj:true,
                    "Sepid Parvaz":true,
                    sepid_parvaz:true,
                    Hamood:true,
                    hamood:true,
                    Dayan:true,
                    dayan: true,
                    Darvishi:true,
                    darvishi: true,
                    Moeindarbari:true,
                    moeindarbari:true,
                    Deltaban:true,
                    deltaban: true,
                    Jimbo:true,
                    Jimboo: true,
                    Booking:true,
                    booking: true,
                    snapp:true,
                    Snapp: true,
                    alibaba: true,
                    Alibaba:true,
                    alwin: true,
                    Alwin:true,
                        

                    

                },
                provider_length: {},
                hotels_name: [],
                all_hotels_name: [],
                minimum_date: "",
                datepicker_min_date: "",
                filter_star: "all",
                filter_name: "",
                body: {
                    "target": "KIH",
                    "start_date": '',
                    "night_count": 3,
                    "hotel_star": 5,
                    "adults": 2
                },
                loading: false,
                search_start: "",
                search_end: "",
                search_night_count: 0,
                fixed_data: [],
                show_result: false,
                show_print: false,
                data: [],
                last_search: {
                    date: new Date(),
                    minute: 0,
                    text: "ثانیه",
                    interval: null,
                    warning: false
                },
                show_hotel_anaysis: false
            }
        }
    }
})
