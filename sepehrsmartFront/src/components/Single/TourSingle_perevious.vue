<template>
  <main class="container my-3">
    <print-component :data="data" v-if="show_print" :start_date="search_start" :end_date="search_end"></print-component>
    <div class="row align-items-end">




      <!-- NEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW -->
      <!-- --- Source --- -->
      <div class="col-12 col-md-2">
        <label for="single_source" class="text-muted mb-1">مبدا</label>
        <select name="single_source" id="single_source" class="form-select form-select-sm" v-model="body.source">
          <option value="KIH">کیش</option>
          <option value="MHD">مشهد</option>
          <option value="GSM">قشم</option>
          <option value="THR">تهران</option>
          <option value="SYZ">شیراز</option>
          <option value="IFN">اصفهان</option>
          <option value="AZD">یزد</option>
          <option value="TBZ">تبریز</option>

        </select>
      </div>





      <!-- --- TARGET --- -->
      <div class="col-12 col-md-2">
        <label for="single_target" class="text-muted mb-1">مقصد</label>
        <select name="single_target" id="single_target" class="form-select form-select-sm" v-model="body.target">
          <option value="KIH">کیش</option>
          <option value="MHD">مشهد</option>
          <option value="GSM">قشم</option>
          <option value="SYZ">شیراز</option>

          <option value="THR">تهران</option>
          <option value="IFN">اصفهان</option>
          <option value="AZD">یزد</option>
          <option value="TBZ">تبریز</option>

        </select>
      </div>





      <!-- --- DATE --- -->
      <div class="col-12 col-md-3 mt-3 mt-md-0">
        <div class="d-flex justify-content-between align-items-center">
          <label for="date" class="text-muted mb-1">تاریخ</label>
          <div class="d-flex">
            <button class="m-0 btn border-0" :disabled="isValidDate" v-on:click="prevDay">&lt; روز قبل
            </button>
            <button class="m-0 btn" v-on:click="nextDay">روز بعد &gt;</button>
          </div>
        </div>
        <!--        <input class="form-control mt-1" type="date" name="date" id="date" v-model="body.start_date">-->
        <date-picker id="date" class="mt-1 w-100 h-100" :min="datepicker_min_date" v-model="body.start_date"
                     :popover="true"></date-picker>
      </div>
      <!-- --- NIGHT COUNT --- -->
      <div class="col-12 col-md-3 mt-3 mt-md-0">
        <div class="d-flex justify-content-between align-items-center">
          <label for="night_count" class="text-muted">شب اقامت</label>
          <p class="m-0">{{ convertDate(backDate) }}</p>
        </div>
        <select class="form-select form-select-sm mt-2" name="night_count" id="night_count" v-model="body.night_count">
          <option :value="2">2</option>
          <option :value="3">3</option>
          <option :value="4">4</option>
          <option :value="5">5</option>
          <option :value="6">6</option>
          <option :value="7">7</option>
        </select>
      </div>
      <!-- --- ADULTS --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <label for="single_adults" class="text-muted mb-1">تعداد نفرات</label>
        <select name="single_adults" id="single_target" class="form-select form-select-sm" v-model="body.adults">
          <option :value="2">۲ نفر</option>
          <option :value="3">۳ نفر</option>
          <option :value="4">۴ نفر</option>
          <option :value="5">۵ نفر</option>
          <option :value="6">۶ نفر</option>
        </select>
      </div>
      <!-- --- SUBMIT --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <button class="btn btn-success w-100" :disabled="loading" v-on:click="getData(true)">جستجو</button>
      </div>
    </div>
    <hr>
    <!-- --- FILTER --- -->
    <section v-if="show_result">
      <div class="row">
        <div class="col-12 col-md-3 mt-3">
          <div class="sticky-top">
            <div class="row align-items-center bg-white py-3 rounded">
              <!-- --- STAR --- -->
              <div class="col-12">
                <label for="filter_star" class="text-muted mb-1">ستاره هتل</label>
                <select v-model="filter_star" class="form-select" id="filter_star" @change="sortedData">
                  <option value="all">همه</option>
                  <option value="1">۱ ستاره</option>
                  <option value="2">۲ ستاره</option>
                  <option value="3">۳ ستاره</option>
                  <option value="4">۴ ستاره</option>
                  <option value="5">۵ ستاره</option>
                </select>
              </div>
              <!-- --- NAME --- -->
              <div class="col-12 mt-3">
                <label for="filter_name" class="text-muted mb-1">نام هتل</label>
                <!--          <input type="text" class="form-control" placeholder="نام هتل ..." v-model="filter_name" id="filter_name">-->
                <v-select multiple :options="hotels_name" v-model="filter_name" id="filter_name" @input="sortedData"
                          @change="sortedData"></v-select>
              </div>
              <!-- --- SORT --- -->
              <div class="col-12 mt-3">
                <label for="order_by_filter" class="text-muted mb-1">مرتب سازی</label>
                <select v-model="order_by" class="form-select" id="order_by_filter" v-on:change="sortedData">
                  <option value="price_a">قیمت - کم به زیاد</option>
                  <option value="price_d">قیمت - زیاد به کم</option>
                  <option value="hour_d_a">پرواز رفت - صبح به شب</option>
                  <option value="hour_d_d">پرواز رفت - شب به صبح</option>
                  <option value="hour_a_a">پرواز برگشت - صبح به شب</option>
                  <option value="hour_a_d">پرواز برگشت - شب به صبح</option>
                </select>
              </div>

              <!-- --- PROVIDER --- -->
              <div class="col-12 mt-3 d-flex align-items-center justify-content-between">
                <div class="position-relative w-100 border rounded mt-4 p-2 bg-white">
                  <div class="cursor-pointer h-100 w-100" v-on:click="show_provider = !show_provider">
                    <p class="m-0">تامین کنندگان</p>
                  </div>
                  <div class="provider-overlay" v-if="show_provider" v-on:click="show_provider = false"></div>
                  <div class="position-absolute w-100 p-3 provider-item bg-white rounded border" v-if="show_provider">
                    <div class="d-flex justify-content-between align-items-center position-relative">
                      <div>
                        <input type="checkbox" id="filter_provider_all" class="form-check-input" :value="true"
                               v-model="allProviderFilter" v-on:change="allProviderFilterMethod">
                        <label for="filter_provider_all" class="form-check-label me-1">all</label>
                      </div>
                      <div class="m-0 d-flex justify-content-between align-items-center tooltip-custom-main">
                        {{ allProviderLength }}
                      </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-3 position-relative"
                         v-for="(provider, index) of providerLength" :key="index">
                      <div>
                        <input type="checkbox" :id="`filter_provider_${provider.name}`" class="form-check-input"
                               :value="true" :data-value="filter_provider[provider.name]"
                               v-model="filter_provider[provider.name]" v-on:change="sortedData">
                        <label :for="`filter_provider_${provider.name}`" class="form-check-label me-1">
                          <a :href="provider.url" target="_blank" class="m-0 link-dark">{{ provider.name }}</a>
                        </label>
                      </div>
                      <div class="m-0 d-flex justify-content-between align-items-center tooltip-custom-main">
                        <p>{{ provider.count }}</p>
                        <svg v-if="provider.count === 0" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                             fill="currentColor"
                             class="bi bi-exclamation-circle text-danger me-1" viewBox="0 0 16 16">
                          <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                          <path
                              d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
                        </svg>
                        <div v-if="provider.count === 0" class="position-absolute p-2 tooltip-custom">
                          {{ provider.message }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- --- ANALYSIS --- -->
              <div class="col-12 mt-3">
                <div class="row">
                  <div class="col-6">
                    <button class="btn btn-secondary w-100" v-on:click="printData">
                      <svg width="23" height="23" fill="currentColor" class="bi bi-printer"
                           viewBox="0 0 16 16">
                        <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
                        <path
                            d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
                      </svg>
                    </button>
                  </div>
                  <div class="col-6">
                    <button class="btn btn-warning w-100" data-bs-toggle="modal"
                            data-bs-target="#alertCustomModal">ملاحظات
                    </button>
                  </div>
                  <div class="col-6">
                    <button class="btn btn-primary w-100 mt-3" v-on:click="show_analysis = true"
                            :disabled="loading_analysis">
                      <i class="fa fa-spinner fa-spin" v-if="loading_analysis"></i>
                      آنالیز هتلی
                    </button>
                  </div>
                  <div class="col-6">
                    <button class="btn btn-info w-100 mt-3" v-on:click="show_hotel_anaysis = true"
                            :disabled="loading_analysis">
                      <i class="fa fa-spinner fa-spin" v-if="loading_analysis"></i>
                      بررسی هتلی
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="row mt-3 bg-white rounded p-3 align-items-center">
              <div class="col-6">
                <p class="m-0">آخرین بروزرسانی : </p>
              </div>
              <div class="col-5">
                <p class="m-0">{{ last_search.minute }} {{ last_search.text }} پیش</p>
              </div>
              <div class="col-1 text-danger" v-if="last_search.warning">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                     class="bi bi-exclamation-circle" viewBox="0 0 16 16">
                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                  <path
                      d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
                </svg>
              </div>
              <!-- --- NO CACHE BUTTON --- -->
              <div class="col-12 mt-3">
                <button class="btn btn-success w-100" v-on:click="getData(false)">بروزرسانی زنده</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-9">
          <!-- --- TOURS --- -->
          <section v-if="data.length">
            <TourComponent
                v-for="(hotel, index) in data"
                :key="index"
                :hotel_name="hotel.hotel_name"
                :total_price="Number(hotel.providers[0].price)"
                :providers="hotel.providers"
                :hotel_star="hotel.hotel_star"
                :redirect_link="hotel.redirect_link"
                :adults="body.adults"
                :index="index"
                :start_date="search_start"
                :end_date="search_end"
                :analysis_data="analysis_data"
                :loading_analysis="loading_analysis"
            />
          </section>
          <div class="alert alert-warning mt-3 text-center" v-else>
            <h5>توری یافت نشد</h5>
          </div>
        </div>
      </div>
    </section>
    <!-- --- LOADING --- -->
    <loading-component :loading="loading"></loading-component>
    <!-- --- TOUR ANALYSIS --- -->
    <tour-analysis :start_date="convertDateToGeorgian(search_start)" :loading="loading_analysis" :show="true"
                   @changeAnalysisStatus="changeAnalysisStatus" :data="analysis_data"
                   :night_count="search_night_count" :analysis_data="analysis_data"
                   v-if="show_analysis" :adults="body.adults"></tour-analysis>
    <!-- --- HOTEL ANALYSIS --- -->
    <hotel-analysis v-if="show_hotel_anaysis" @changeAnalysisStatus="changeAnalysisStatus"
                    :hotel_names="all_hotels_name" :data="analysis_data" :adults="body.adults"></hotel-analysis>
    <!-- --- ALERT --- -->
    <alert-component></alert-component>
  </main>
</template>

<script>

import 'vue-select/dist/vue-select.css';
import 'vue3-toastify/dist/index.css';
import TourComponent from "@/components/Single/TourComponent";
import {toast} from 'vue3-toastify';
import moment from 'moment';
import moment_jalali from 'moment-jalaali';
import TourAnalysis from "@/components/Analysis/TourAnalysis";
import LoadingComponent from "@/components/LoadingComponent";
import PrintComponent from "@/components/Print/PrintComponent";
import AlertComponent from "@/components/Alert/AlertComponent";
import HotelAnalysis from "@/components/HotelAnalysis/HotelAnalysis";
import {router} from "@/routes";

export default {
  name: 'TourSingle',
  components: {
    HotelAnalysis,
    AlertComponent,
    PrintComponent,
    LoadingComponent,
    TourComponent,
    TourAnalysis,
  },
  data() {
    return {
      dataKey: 0, // Initialize a key for the component
      show_analysis: false,
      loading_analysis: false,
      analysis_data: [],
      order_by: "price_a",
      show_provider: false,
      filter_provider: {
        alibaba: true,
        booking: true,
        Jimboo:true,
        alwin: true,
        deltaban: true,
        sepid_parvaz: true,
        dayan: true,
        omid_oj: true,
        parmis: true,
        mehrab: true,
        rahbal: true,
        kimiya:true,
        eram2mhd:true,
        tak_setare: true,
        hrc: true,
        hamood:true,
        safiran:true,
        darvishi:true,
        moeindarbari:true
      },
      provider_length: {},
      hotels_name: [],
      all_hotels_name: [],
      minimum_date: "",
      datepicker_min_date: "",
      filter_star: "all",
      filter_name: "",
      body: {
        "source":"MHD",
        "target": "KIH",
        "start_date": '',
        "night_count": 3,
        "hotel_star": 5,
        "use_cache": true,
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
  },
  methods: {
    getSortedData(data) {
      switch (this.order_by) {
        case "price_a": {
          return data.sort((a, b) => parseFloat(a.providers[0].price) - parseFloat(b.providers[0].price));
        }
        case "price_d": {
          return data.sort((a, b) => parseFloat(b.providers[0].price) - parseFloat(a.providers[0].price));
        }
        case "hour_d_a": {
          return data.sort((a, b) => parseInt(a.providers[0].go_flight_arrive_time.slice(0, 3)) - parseInt(b.providers[0].go_flight_arrive_time.slice(0, 3)));
        }
        case "hour_d_d": {
          return data.sort((a, b) => parseInt(b.providers[0].go_flight_arrive_time.slice(0, 3)) - parseInt(a.providers[0].go_flight_arrive_time.slice(0, 3)));
        }
        case "hour_a_a": {
          return data.sort((a, b) => parseInt(a.providers[0].return_flight_arrive_time.slice(0, 3)) - parseInt(b.providers[0].return_flight_arrive_time.slice(0, 3)));
        }
        case "hour_a_d": {
          return data.sort((a, b) => parseInt(b.providers[0].return_flight_arrive_time.slice(0, 3)) - parseInt(a.providers[0].return_flight_arrive_time.slice(0, 3)));
        }
        default: {
          return data;
        }
      }
    },
    sortedData() {
      const data = this.getSortedData(this.filterProvider());
      if (this.filter_name.length) {
        let valid_filter_name = Object.values(this.filter_name);
        const result = data.filter(hotel => valid_filter_name.includes(hotel.hotel_name));
        this.data = result;
        this.dataKey++;
        return result;
      } else {
        if (this.filter_star === "all") {
          const result = data;
          this.data = result;
          this.dataKey++;
          return result;
        } else {
          const result = data.filter(hotel => hotel.hotel_star === parseInt(this.filter_star));
          this.data = result;
          this.dataKey++;
          return result;
        }
      }
    },
    filterProvider() {
      let hotel_provider = [];

      console.log( this.fixed_data);


      for (let hotel of this.fixed_data) {
        let hotel_item = {...hotel};
        let providers = [];
        hotel_item.providers.forEach(provider => {
          if (this.filter_provider.alibaba && provider.provider_name === "alibaba") {
            providers.push({...provider});
          }
          if (this.filter_provider.booking && provider.provider_name === "booking") {
            providers.push({...provider});
          }

          if (this.filter_provider.Jimboo && provider.provider_name === "Jimboo") {
            providers.push({...provider});
          }


          if (this.filter_provider.alwin && provider.provider_name === "alwin") {
            providers.push({...provider});
          }
          if (this.filter_provider.deltaban && provider.provider_name === "deltaban") {
            providers.push({...provider});
          }
          if (this.filter_provider.sepid_parvaz && provider.provider_name === "sepid_parvaz") {
            providers.push({...provider});
          }
          if (this.filter_provider.dayan && provider.provider_name === "dayan") {
            providers.push({...provider});
          }
          if (this.filter_provider.mehrab && provider.provider_name === "mehrab") {
            providers.push({...provider});
          }

          //kimiya
          if (this.filter_provider.kimiya && provider.provider_name === "kimiya") {
            providers.push({...provider});
          }

          //eram2mhd
          if (this.filter_provider.eram2mhd && provider.provider_name === "eram2mhd") {
            providers.push({...provider});
          }
          //safiran
          if (this.filter_provider.safiran && provider.provider_name === "safiran") {
            providers.push({...provider});
          }
          //safiran
          if (this.filter_provider.hamood && provider.provider_name === "hamood") {
            providers.push({...provider});
          }

          if (this.filter_provider.darvishi && provider.provider_name === "darvishi") {
            providers.push({...provider});
          }

          if (this.filter_provider.moeindarbari && provider.provider_name === "moeindarbari") {
            providers.push({...provider});
          }

          //---------



          if (this.filter_provider.rahbal && provider.provider_name === "rahbal") {
            providers.push({...provider});
          }
          if (this.filter_provider.tak_setare && provider.provider_name === "tak_setare") {
            providers.push({...provider});
          }
          if (this.filter_provider.hrc && provider.provider_name === "hrc") {
            providers.push({...provider});
          }



          if (this.filter_provider.omid_oj && provider.provider_name === "omid_oj") {
            providers.push({...provider});
          }
          if (this.filter_provider.parmis && provider.provider_name === "parmis") {
            providers.push({...provider});
          }

          console.log(this.filter_provider)
        })
        //
        if (providers.length) {
          hotel_item.providers = providers;
          hotel_provider.push(hotel_item);
        }
      }
      this.data = hotel_provider;
      // console.log(hotel_item.providers)
      console.log(this.data );
      this.dataKey++;
      
      return hotel_provider;
    },


  async getAnalysisData(use_cache) {
    this.loading_analysis = true;
    this.analysis_data = []; // Initialize the data array

    const startDate = new Date(this.body.start_date); // Parse the initial start date
  const api_body_template = {
    source: this.body.source,
    target: this.body.target,
    night_count: this.body.night_count,
    adults: this.body.adults,
    range_number: 7,
    use_cache,
  };
  this.range_number=7;
  try {
    for (let i = 0; i < 1; i+=this.range_number) {
      // Calculate the current start_date for this iteration
      const currentDate = new Date(startDate.getTime() + i * 24 * 60 * 60 * 1000) // Increment by 1 day
        .toISOString()
        .split("T")[0];

      // Create the API body for this specific date
      const api_body = {
        ...api_body_template,
        start_date: currentDate // Use the calculated date
        
      };

      // Perform the POST request
      const res = await this.$http.post("get-analysis/", api_body);
      
      
      // Append the results to this.analysis_data
      const fetchedData = (res.data && res.data.data && res.data.data.data) || {};
      Object.entries(fetchedData).forEach(([key, value]) => {
        if (!this.analysis_data[key]) {
          // If the key doesn't exist, add it
          this.analysis_data[key] = value;
        } else {
          // If the key exists, concatenate the arrays
          this.analysis_data[key] = [...this.analysis_data[key], ...value];
        }
      });


      console.log(`Fetched data for ${currentDate}:`,this.analysis_data);

      this.loading_analysis = false;
      this.dataKey++;
    }
  } catch (e) {
    if (e.response && e.response.status === 401) {
      return router.push("/login");
    }

    toast.error("مشکلی پیش آمده است٬ لطفا دوباره امتحان کنید", {
      autoClose: 6000,
      position: "bottom-left",
      rtl: false,
      closeOnClick: true,
    });
  } finally {
    this.loading_analysis = false;
    this.$store.state.disable_header_link = false;
  }
},
    allProviderFilterMethod() {
      if (this.allProviderFilter) {
        for (let pv in this.filter_provider) {
          this.filter_provider[pv] = false;
        }
      } else {
        for (let pv in this.filter_provider) {
          this.filter_provider[pv] = true;
        }
        
      }

      
      this.filterProvider();
      this.dataKey++;
      console.log(this.filter_provider)
    },
    getData(use_cache = true) {
      this.$store.state.disable_header_link = true;
      const date = moment(this.body.start_date, "YYYY-MM-DD");
      this.show_result = false;
      if (date.isAfter(this.minimum_date)) {
        this.loading = true;
        this.data = [];
        this.search_start = this.convertDate(this.body.start_date);
        this.search_end = this.convertDate(this.backDate);
        this.search_night_count = this.body.night_count;
        this.body.use_cache = use_cache;
        this.body.adults = parseInt(this.body.adults);
        const link = "get-data/";
        this.$http.post(link, this.body, {timeout: 1000 * 60 * 10}).then(req => {
          console.log(req);
          this.getAnalysisData(use_cache);
          this.filter_name = "";
          this.data = req.data.data;
          this.provider_length = req.data.providers;
          this.fixed_data = this.data;
          this.show_result = true;
          this.hotels_name = this.data.sort((a, b) => a.hotel_star - b.hotel_star).map(hotel => hotel.hotel_name);
          this.sortedData();
          // this.getAnalysisData();
          this.calc_last_search();
          if (this.body.target === "KIH") {
            this.getHotelNames();
          } else {
            this.all_hotels_name = this.hotels_name;
          }
        }).catch((error) => {
          if (error.response.status === 401) {
            return router.push('/login');
          }
          toast.error(error.response.data.message, {
            autoClose: 6000,
            position: "bottom-left",
            rtl: false,
            closeOnClick: true
          });
          clearInterval(this.last_search.interval);
        }).finally(() => {
          this.loading = false;
        })
      } else {
        toast.error("لطفا تاریخ معتبر وارد کنید", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
      }
    },
    nextDay() {
      const today = moment(this.body.start_date, "YYYY-MM-DD");
      this.body.start_date = moment(today).add(1, 'd').format("YYYY-MM-DD")
    },
    prevDay() {
      const today = moment(this.body.start_date, "YYYY-MM-DD");
      this.body.start_date = moment(today).subtract(1, 'd').format("YYYY-MM-DD")
    },
    convertDate(date) {
      return moment_jalali(date).format("jYYYY/jMM/jDD");
    },
    convertDateToGeorgian(date) {
      return moment_jalali(date, 'jYYYY/jMM/jDD').format('YYYY-MM-DD');
    },
    changeAnalysisStatus(data) {
      this.show_analysis = data;
      this.show_hotel_anaysis = data;
    },
    printData() {
      this.show_result = false;
      this.show_print = true;
      setTimeout(() => {
        window.print();
      }, 200);
      setTimeout(() => {
        this.show_print = false;
        this.show_result = true;
      }, 600);
    },
    calc_last_search() {
      clearInterval(this.last_search.interval);
      this.last_search.date = new Date();
      this.last_search.minute = 0;
      this.last_search.text = "ثانیه";
      this.last_search.interval = setInterval(() => {
        let new_date = new Date();
        let dif = new_date - this.last_search.date;
        let result = Math.abs(dif / 1000);
        if (result < 60) {
          this.last_search.minute = Math.round(result);
          this.last_search.text = "ثانیه";
        } else {
          this.last_search.minute = parseFloat(result / 60).toFixed(1);
          this.last_search.text = "دقیقه";
        }
        this.last_search.warning = result > 75;
      }, 1000);
    },
    getHotelNames() {
      this.$http.get('https://tour-collector-api.sepehrsmart.ir/get-hotels/').then(val => {
        this.all_hotels_name = val.data;
      })
    }
  },
  computed: {
    isValidDate() {
      return !moment(this.body.start_date, "YYYY-MM-DD").isAfter(new Date());
    },
    backDate() {
      return moment(this.body.start_date, "YYYY-MM-DD").add(this.body.night_count, 'd').format("YYYY-MM-DD");
    },
    allProviderFilter() {
      for (let pv in this.filter_provider) {
        if (!this.filter_provider[pv]) {
          return false;
        }
      }
      return true
    },
    providerLength() {
      let result = [];
      for (let pv in this.provider_length) {
        result.push({
          "name": pv,
          "count": this.provider_length[pv]['length'],
          "message": this.provider_length[pv]['message'],
          "url": this.provider_length[pv]['url']
        })
      }
      return result;
    },
    allProviderLength() {
      let result = 0;
      this.providerLength.forEach(pv => {
        result += pv.count;
      })
      return result
    }
  },
  watch: {
    filter_name() {
      this.sortedData();
    }
  },
  created() {
    this.show_analysis = this.$store.state.ready_tour_data.show_analysis;
    this.loading_analysis = this.$store.state.ready_tour_data.loading_analysis;
    this.analysis_data = this.$store.state.ready_tour_data.analysis_data;
    this.order_by = this.$store.state.ready_tour_data.order_by;
    this.show_provider = this.$store.state.ready_tour_data.show_provider;
    this.filter_provider = this.$store.state.ready_tour_data.filter_provider;
    this.provider_length = this.$store.state.ready_tour_data.provider_length;
    this.hotels_name = this.$store.state.ready_tour_data.hotels_name;
    this.all_hotels_name = this.$store.state.ready_tour_data.all_hotels_name;
    this.minimum_date = this.$store.state.ready_tour_data.minimum_date;
    this.datepicker_min_date = this.$store.state.ready_tour_data.datepicker_min_date;
    this.filter_star = this.$store.state.ready_tour_data.filter_star;
    this.filter_name = this.$store.state.ready_tour_data.filter_name;
    this.body = this.$store.state.ready_tour_data.body;
    this.loading = this.$store.state.ready_tour_data.loading;
    this.search_start = this.$store.state.ready_tour_data.search_start;
    this.search_end = this.$store.state.ready_tour_data.search_end;
    this.search_night_count = this.$store.state.ready_tour_data.search_night_count;
    this.fixed_data = this.$store.state.ready_tour_data.fixed_data;
    this.show_result = this.$store.state.ready_tour_data.show_result;
    this.show_print = this.$store.state.ready_tour_data.show_print;
    this.data = this.$store.state.ready_tour_data.data;
    this.last_search = this.$store.state.ready_tour_data.last_search;
    this.show_hotel_anaysis = this.$store.state.ready_tour_data.show_hotel_anaysis;

    //
    function formatDate(date) {
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2)
        month = '0' + month;
      if (day.length < 2)
        day = '0' + day;

      return [year, month, day].join('-');
    }

    this.calc_last_search();
    this.body.start_date = formatDate(new Date());
    this.datepicker_min_date = formatDate(new Date());
    const today = moment(this.body.start_date, "YYYY-MM-DD");
    this.minimum_date = moment(today).subtract(1, 'd').format("YYYY-MM-DD");
  },
  beforeUnmount() {
    clearInterval(this.last_search.interval);
    this.$store.state.ready_tour_data = this.$data;
  }
}
</script>

<style>
input, select {
  box-shadow: none !important;
  outline: none !important;
}

.bg-white {
  background: #ffffff !important;
}

.cursor-pointer {
  cursor: pointer !important;
}

.provider-item {
  top: 50px;
  right: 0;
  z-index: 5;
}

.sticky-top {
  position: sticky;
  top: 10px;
  z-index: 3;
}

.provider-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 4;
}

.tooltip-custom-main:hover > .tooltip-custom {
  display: block;
}

.tooltip-custom {
  width: 150px;
  background: rgba(220, 53, 69);
  color: #fafafa;
  border-radius: 10px;
  text-align: center;
  left: 0;
  display: none;
  transition: all .3s;
}

@media (min-width: 1025px) {
  .h-custom-2 {
    height: 100%;
  }
}
</style>

