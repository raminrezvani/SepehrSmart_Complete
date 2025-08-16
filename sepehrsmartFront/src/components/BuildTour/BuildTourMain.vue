<template>
  <main class="container my-4">
    <!-- --- SEARCH --- -->
    <div class="search-section bg-white rounded-3 p-4 shadow-sm">
      <div class="row g-3">
        <!-- --- SOURCE --- -->
        <div class="col-12 col-md-6 col-lg-2">
          <div class="form-group">
            <label for="build_tour_source" class="text-muted mb-2">مبدا</label>
            <select name="build_tour_source" id="build_tour_source" 
                    class="form-select" 
                    v-model="body.source" 
                    v-on:change="getCalendarData">
              <option value="MHD">مشهد</option>
              <option value="THR">تهران</option>
              <option value="IFN">اصفهان</option>
              <option value="SYZ">شیراز</option>
              <option value="TBZ">تبریز</option>
              <option value="GSM">قشم</option>
              <option value="KIH">کیش</option>
              <option value="AZD">یزد</option>
              <option value="AWZ">اهواز</option>
              <option value="BND">بندرعباس</option>
              <option value="KER">کرمان</option>
              <option value="KSH">کرمانشاه</option>
              <option value="RAS">رشت</option>
              <option value="SRY">ساری</option>
              <option value="ZBR">چابهار</option>
              <option value="ABD">آبادان</option>
              <option value="BUZ">بوشهر</option>
              <option value="GBT">گرگان</option>
              <option value="OMH">ارومیه</option>
              <option value="ADU">اردبیل</option>
              <option value="HDM">همدان</option>
              <option value="RZR">رامسر</option>
              <option value="KHD">خرم آباد</option>
            </select>
          </div>
        </div>

        <!-- --- Target --- -->
        <div class="col-12 col-md-6 col-lg-2">
          <div class="form-group">
            <label for="build_tour_target" class="text-muted mb-2">مقصد</label>
            <select name="build_tour_target" id="build_tour_target" 
                    class="form-select" 
                    v-model="body.target" 
                    v-on:change="getCalendarData">
              <option value="MHD">مشهد</option>
              <option value="THR">تهران</option>
              <option value="IFN">اصفهان</option>
              <option value="SYZ">شیراز</option>
              <option value="TBZ">تبریز</option>
              <option value="GSM">قشم</option>
              <option value="KIH">کیش</option>
              <option value="AZD">یزد</option>
              <option value="AWZ">اهواز</option>
              <option value="BND">بندرعباس</option>
              <option value="KER">کرمان</option>
              <option value="KSH">کرمانشاه</option>
              <option value="RAS">رشت</option>
              <option value="SRY">ساری</option>
              <option value="ZBR">چابهار</option>
              <option value="ABD">آبادان</option>
              <option value="BUZ">بوشهر</option>
              <option value="GBT">گرگان</option>
              <option value="OMH">ارومیه</option>
              <option value="ADU">اردبیل</option>
              <option value="HDM">همدان</option>
              <option value="RZR">رامسر</option>
              <option value="KHD">خرم آباد</option>
            </select>
          </div>
        </div>

        <!-- --- GO DATE --- -->
        <div class="col-12 col-md-6 col-lg-2">
          <div class="form-group">
            <label class="text-muted mb-2">تاریخ رفت</label>
            <div class="date-input" @click="openDatePicker('go')">
              <input type="text" 
                     class="form-control" 
                     :value="formatDisplayDate(body.start_date)" 
                     readonly 
                     placeholder="تاریخ رفت">
            </div>
          </div>
        </div>

        <!-- --- BACK DATE --- -->
        <div class="col-12 col-md-6 col-lg-2">
          <div class="form-group">
            <div class="d-flex justify-content-between">
              <label class="text-muted mb-2">تاریخ برگشت</label>
              <span class="text-muted small">{{ body.night_count }} شب</span>
            </div>
            <div class="date-input" @click="openDatePicker('return')">
              <input type="text" 
                     class="form-control" 
                     :value="formatDisplayDate(body.end_date)" 
                     readonly 
                     placeholder="تاریخ برگشت">
            </div>
          </div>
        </div>

        <!-- --- STAR --- -->
        <div class="col-12 col-md-6 col-lg-2">
          <div class="form-group">
            <label for="filter_star" class="text-muted mb-2">ستاره هتل</label>
            <select v-model="filter_star" class="form-select" id="filter_star" @change="sortedData">
              <option value="all">همه</option>
              <option value="1">۱ ستاره</option>
              <option value="2">۲ ستاره</option>
              <option value="3">۳ ستاره</option>
              <option value="4">۴ ستاره</option>
              <option value="5">۵ ستاره</option>
            </select>
          </div>
        </div>

        <!-- --- PROVIDER --- -->
        <div class="col-12 col-md-6 col-lg-2">
          <div class="form-group">
            <label class="text-muted mb-2">تامین کنندگان</label>
            <div class="position-relative">
              <div class="provider-selector" @click="show_provider = !show_provider">
                <div class="d-flex justify-content-between align-items-center p-2 border rounded">
                  <span class="d-flex align-items-center">
                    <i class="bi bi-building me-2"></i>
                    {{ allProviderLength }} تامین کننده
                  </span>
                  <i class="bi" :class="show_provider ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                </div>
              </div>
              
              <!-- Provider Modal -->
              <div class="provider-modal" v-if="show_provider">
                <div class="provider-modal-overlay" @click="show_provider = false"></div>
                <div class="provider-modal-content">
                  <div class="provider-modal-header">
                    <h5 class="mb-0">تامین کنندگان</h5>
                    <button class="btn-close" @click="show_provider = false"></button>
                  </div>
                  
                  <div class="provider-modal-body">
                    <div class="provider-header mb-3">
                      <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                          <div class="custom-checkbox-container">
                            <input type="checkbox" 
                                   id="filter_provider_all" 
                                   class="custom-checkbox-input" 
                                   v-model="allProviderFilter" 
                                   @change="allProviderFilterMethod">
                            <label for="filter_provider_all" class="custom-checkbox-label ms-2 d-flex align-items-center">
                              <span class="custom-checkbox-visual"></span>
                              همه تامین کنندگان
                            </label>
                          </div>
                        </div>
                        <span class="badge bg-primary rounded-pill">{{ allProviderLength }}</span>
                      </div>
                    </div>
                    
                    <div class="provider-list">
                      <div v-for="(provider, index) in providerLength" :key="index" 
                           class="provider-item" 
                           :class="{'provider-loading': refreshingProvider === provider.name}">
                        <div class="d-flex justify-content-between align-items-center p-2">
                          <div class="d-flex align-items-center">
                            <div class="custom-checkbox-container">
                              <input type="checkbox" 
                                     :id="'provider_' + index" 
                                     v-model="filter_provider[provider.name]" 
                                     class="custom-checkbox-input">
                              <label :for="'provider_' + index" class="custom-checkbox-label d-flex align-items-center">
                                <span class="custom-checkbox-visual"></span>
                                <i class="bi bi-building-fill me-2 provider-icon"></i>
                                {{ provider.name }}
                              </label>
                            </div>
                          </div>
                          <div class="d-flex align-items-center gap-2">
                            <span :title="provider.message || ''" 
                                  :class="{'text-danger': provider.message}"
                                  class="provider-count">
                              {{ provider.count }}
                            </span>
                            <button class="btn btn-sm refresh-provider" 
                                    @click.stop="refreshProvider(provider.name)"
                                    :disabled="loading"
                                    :class="{
                                      'btn-outline-primary': !loading || refreshingProvider !== provider.name,
                                      'btn-primary': loading && refreshingProvider === provider.name,
                                      'loading': loading && refreshingProvider === provider.name
                                    }">
                              <div class="spinner-container">
                                <i class="bi bi-arrow-repeat" v-if="!loading || refreshingProvider !== provider.name"></i>
                                <div class="spinner" v-else></div>
                              </div>
                              <span v-if="loading && refreshingProvider === provider.name" class="ms-1">در حال بروزرسانی...</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- --- BUTTONS --- -->
        <div class="col-12 mt-3">
          <div class="d-flex gap-2">
            <button class="btn btn-primary flex-grow-1" :disabled="loading" @click="getData(true)">
              <i class="bi bi-search me-1"></i>
              جستجو
            </button>
            <button class="btn btn-outline-primary flex-grow-1" @click="getData(false)">
              <i class="bi bi-arrow-clockwise me-1"></i>
              بروزرسانی زنده
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- --- MAIN --- -->
    <section class="mt-4">
      <build-loading v-if="loading"></build-loading>
      <build-result v-if="show_result" 
                   :key="dataKey" 
                   :data="data" 
                   :adults="parseInt(this.body.adults)"
                   :target="body.target" 
                   :body="this.body" 
                   :source="body.source" 
                   :analysis_data="analyse_data" 
                   :analysis_loading="show_analyse_loading"
                   @show-analysis="handleShowAnalysis">
      </build-result>
    </section>
   


    <!-- Calendar Overlay -->
    <div class="calendar-overlay" v-if="show_datepicker_go || show_datepicker_return">
      <div class="calendar-wrapper">
        <div class="calendar-header">
          <h4 class="calendar-title">انتخاب تاریخ</h4>
          <button class="calendar-close" @click="closeDatePickers">&times;</button>
        </div>
        <div class="calendar-container">
          <!-- Departure Calendar -->
          <div class="calendar-box">
            <h5 class="text-center mb-3">تاریخ رفت</h5>
            <calender-index
              key="go_date"
              placeholder="تاریخ رفت"
              :show="true"
              :disable-old="true"
              :days_data="calendar_data.go"
              @submitted="goDateSubmit"
              @showing="(val) => datePickerShowing(val, 'departure')"
            />
          </div>
          
          <!-- Return Calendar -->
          <div class="calendar-box">
            <h5 class="text-center mb-3">تاریخ برگشت</h5>
            <calender-index
              key="back_date"
              placeholder="تاریخ برگشت"
              :show="true"
              :disable-old="true"
              :days_data="calendar_data.return"
              @submitted="returnDateSubmit"
              @showing="(val) => datePickerShowing(val, 'return')"
            />
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import moment from "moment";
import moment_jalali from "moment-jalaali";
import BuildLoading from "@/components/BuildTour/BuildLoading";
import BuildResult from "@/components/BuildTour/BuildResult";
import {toast} from "vue3-toastify";
import CalenderIndex from "@/components/DatePicker/CalendarIndex";
import {router} from "@/routes";

export default {
  name: "BuildTourMain",
  components: {CalenderIndex, BuildResult, BuildLoading},
  data() {
    return {
      dataKey: 0,
      show_provider: false,
      filter_provider: {
        Eghamat24: true,
        Expedia:true,
        Alaedin: true,
        alibaba: true,
        booking: true,
        Jimboo: true,
        Snapp:true,
        Stayforlong:true,
        "ZenHotels.com":true,
        "Trip.com":true,
        "Hotels.com":true,
        "Booking.com":true,


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
        tak_setareh: true,
        "Tak Setareh":true,
        hrc: true,
        hamood:true,
        safiran:true,
        FlyToday:true,
        darvishi:true,
        moeindarbari:true,

        hamsafar:true,
        iman:true,
        dolfin:true,
        flamingo:true,
        shayan_gasht:true,
        yegane_fard:true,
        alaedin:true,
      },
      provider_length: {},
      filter_star: "all",
      filter_name: "",
      body: {
        "start_date": "",
        "end_date": "",
        "night_count": 0,
        "hotel_star": 5,
        "source": "MHD",
        "target": "KIH",
        "adults": 2,
        "use_cache":true
      },
      calendar_data: {
        go: [],
        return: [],
      },
      show_datepicker_go: false,
      show_datepicker_return: false,
      show_datepicker: false,
      data: {},
      analyse_data: [],
      show_analyse_loading: false,
      loading: false,
      fixed_data: [],
      show_result: false,
      datepicker_min_date: "",
      minimum_date: "",
      refreshingProvider: null
    }
  },
  methods: {
    getSortedData(data) {

      return data;
      // switch (this.order_by) {
      //   case "price_a": {
      //     return data.hotel.sort((a, b) => parseFloat(a.min_price) - parseFloat(b.min_price));
      //   }
      //   case "price_d": {
      //     return data.hotel.sort((a, b) => parseFloat(b.min_price) - parseFloat(a.min_price));
      //   }
      //   // case "hour_d_a": {
      //   //   return data.hotel.sort((a, b) => parseInt(a.providers[0].go_flight_arrive_time.slice(0, 3)) - parseInt(b.providers[0].go_flight_arrive_time.slice(0, 3)));
      //   // }
      //   // case "hour_d_d": {
      //   //   return data.hotel.sort((a, b) => parseInt(b.providers[0].go_flight_arrive_time.slice(0, 3)) - parseInt(a.providers[0].go_flight_arrive_time.slice(0, 3)));
      //   // }
      //   // case "hour_a_a": {
      //   //   return data.hotel.sort((a, b) => parseInt(a.providers[0].return_flight_arrive_time.slice(0, 3)) - parseInt(b.providers[0].return_flight_arrive_time.slice(0, 3)));
      //   // }
      //   // case "hour_a_d": {
      //   //   return data.hotel.sort((a, b) => parseInt(b.providers[0].return_flight_arrive_time.slice(0, 3)) - parseInt(a.providers[0].return_flight_arrive_time.slice(0, 3)));
      //   // }
      //   default: {
      //     return data.hotel;
      //   }
      // }
    },
    sortedData() {
      const data = this.getSortedData(this.filterProvider());
      if (this.filter_name.length) {
        let valid_filter_name = Object.values(this.filter_name);
        const result = data.hotel.filter(item => valid_filter_name.includes(item.hotel_name));
        this.data.hotel = result;
        this.dataKey++;
        console.log( this.data)
        return result;
      } else {
        if (this.filter_star === "all") {
          const result = data;
          this.data = result;
          this.dataKey++;
          return result;
        } else {
          console.log('Filter Star');

          const result = data.hotel.filter(item => String(item.hotel_star) === String(this.filter_star));
          this.data.hotel = result;
          this.dataKey++;
          return this.data;
        }
      }
    },


    // filterProvider() {
    //   let hotel_provider = [];
    //   this.dataKey++; // Increment the key to trigger re-render



    //   // Make a deep copy of fixed_data to prevent modification of original data
    //   const fixedDataCopy = JSON.parse(JSON.stringify(this.fixed_data));


    //   // console.log(fixedDataCopy.hotel);
    //   console.log(this.filter_provider)



    //   for (let hotel of fixedDataCopy.hotel) {
    //     let hotel_item = {...hotel};
    //     let providers = [];



    //   // hotel_item.providers.forEach(provider => {

    //     if (this.filter_provider.Eghamat24 && hotel.provider === "Eghamat24") {
    //       providers.push({...hotel});
    //     }

    //     if (this.filter_provider.alibaba && hotel.provider === "alibaba") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.booking && hotel.provider === "booking") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.alwin && hotel.provider === "alwin") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.deltaban && hotel.provider === "deltaban") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.sepid_parvaz && hotel.providere === "sepid_parvaz") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.dayan && hotel.provider === "dayan") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.mehrab && hotel.provider=== "mehrab") {
    //       providers.push({...hotel});
    //     }

    //     //kimiya
    //     if (this.filter_provider.kimiya && hotel.provider === "kimiya") {
    //       providers.push({...hotel});
    //     }

    //     //eram2mhd
    //     if (this.filter_provider.eram2mhd && hotel.provider === "eram2mhd") {
    //       providers.push({...hotel});
    //     }
    //     //safiran
    //     if (this.filter_provider.safiran && hotel.provider === "safiran") {
    //       providers.push({...hotel});
    //     }
    //     //safiran
    //     if (this.filter_provider.hamood && hotel.provider === "hamood") {
    //       providers.push({...hotel});
    //     }

    //     //---------



    //     if (this.filter_provider.rahbal && hotel.provider === "rahbal") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.tak_setare && hotel.provider === "tak_setare") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.hrc && hotel.provider === "hrc") {
    //       providers.push({...hotel});
    //     }



    //     if (this.filter_provider.omid_oj && hotel.provider === "omid_oj") {
    //       providers.push({...hotel});
    //     }
    //     if (this.filter_provider.parmis && hotel.provider === "parmis") {
    //       providers.push({...hotel});
    //     }

    //     //
    //     if (providers.length) {
    //       hotel_item.providers = providers;
    //       hotel_provider.push(hotel_item);
    //     }
    //   }
    //   this.data.hotel = hotel_provider;
    //   // Use Vue's set method to update nested properties so that Vue's reactivity system can track the changes:

    //   // this.data = { ...this.data, hotel: hotel_provider };

    //   this.dataKey++; // Increment the key to trigger re-render
    //   // this.data ={}

    //   console.log(this.data);

    //   return this.data;
    // },

    // -- Created By CHATGPT -----------
    filterProvider() {
        let hotel_provider = [];
        this.dataKey++; // Increment the key to trigger re-render

        // Make a deep copy of fixed_data to prevent modification of original data
        const fixedDataCopy = JSON.parse(JSON.stringify(this.fixed_data));

        console.log(this.filter_provider);

        for (let hotel of fixedDataCopy.hotel) {
          const roomProvider = []; // Array to hold filtered rooms
          // Destructure to exclude rooms
          const { rooms, ...hotelWithoutRooms } = hotel;

          // Filter rooms based on provider
          for (let room of rooms) {
            if (
              (this.filter_provider.Eghamat24 && room.provider === "Eghamat24") ||
              (this.filter_provider.Expedia && room.provider === "Expedia") ||

              (this.filter_provider.alibaba && room.provider === "alibaba") ||
              (this.filter_provider.booking && room.provider === "booking") ||
              (this.filter_provider.Jimboo && room.provider === "Jimboo") ||


              (this.filter_provider.Snapp && room.provider === "Snapp") ||
              


              (this.filter_provider.Stayforlong && room.provider === "Stayforlong") ||
              (this.filter_provider["ZenHotels.com"] && room.provider === "ZenHotels.com") ||
              (this.filter_provider["Trip.com"] && room.provider === "Trip.com") ||
              (this.filter_provider["Hotels.com"] && room.provider === "Hotels.com") ||
              (this.filter_provider["Booking.com"] && room.provider === "Booking.com") ||




            


              (this.filter_provider.Alaedin && room.provider === "Alaedin") ||
              (this.filter_provider.alwin && room.provider === "alwin") ||
              (this.filter_provider.deltaban && room.provider === "deltaban") ||
              (this.filter_provider.sepid_parvaz && room.provider === "sepid_parvaz") ||
              (this.filter_provider.dayan && room.provider === "dayan") ||
              (this.filter_provider.mehrab && room.provider === "mehrab") ||
              (this.filter_provider.kimiya && room.provider === "kimiya") ||
              (this.filter_provider.eram2mhd && room.provider === "eram2mhd") ||
              (this.filter_provider.safiran && room.provider === "safiran") ||
              (this.filter_provider.hamood && room.provider === "hamood") ||
              (this.filter_provider.rahbal && room.provider === "rahbal") ||
              (this.filter_provider.tak_setareh && room.provider === "tak_setareh") ||

              (this.filter_provider.tak_setareh && room.provider === "tak_setareh") ||
              (this.filter_provider["Tak Setareh"] && room.provider === "tak_setareh") ||

              (this.filter_provider.FlyToday && room.provider === "FlyToday") ||
              (this.filter_provider.hrc && room.provider === "hrc") ||
              (this.filter_provider.omid_oj && room.provider === "omid_oj") ||
              (this.filter_provider.darvishi && room.provider === "darvishi") ||
              (this.filter_provider.moeindarbari && room.provider === "moeindarbari") ||



              (this.filter_provider.hamsafar && room.provider === "hamsafar") ||
              (this.filter_provider.iman && room.provider === "iman") ||
              (this.filter_provider.flamingo && room.provider === "flamingo") ||
              (this.filter_provider.shayan_gasht && room.provider === "shayan_gasht") ||
              (this.filter_provider.yegane_fard && room.provider === "yegane_fard") ||
              (this.filter_provider.dolfin && room.provider === "dolfin") ||
              (this.filter_provider.Alaedin && room.provider === "alaedin") ||




              (this.filter_provider.parmis && room.provider === "parmis")
            ) {
              roomProvider.push(room); // Add room to the filtered list
            }
          }

          // Create hotel_item without rooms and assign filtered rooms
          if (roomProvider.length) {
            const hotel_item = {
              ...hotelWithoutRooms,
              rooms: roomProvider // Assign only the filtered rooms to the hotel
            };
            hotel_provider.push(hotel_item); // Add to hotel provider list
          }
        }

        this.data.hotel = hotel_provider; // Update data with the new hotel list
        //-----------------------
        // Increment the key to trigger re-render 
        this.dataKey++; // Increment the key to trigger re-render
        //-----------------------

        console.log(this.data);

        return this.data;
      },

    allProviderFilterMethod() {
      const newState = this.allProviderFilter;
      Object.keys(this.filter_provider).forEach(key => {
        this.filter_provider[key] = newState;
      });
      this.filterProvider();
    },

    datePickerShowing(val, type) {
      if (type === 'departure') {
        this.show_datepicker_go = val;
        if (val) {
          this.show_datepicker_return = true;
        }
      } else if (type === 'return') {
        this.show_datepicker_return = val;
        if (val) {
          this.show_datepicker_go = true;
        }
      }
    },
    getCalendarData() {
      const body = {
        "source": this.body.source,
        "target": this.body.target,
        "skip_month": 0
      };
      this.calendar_data = {go: [], return: []}
      this.$http.post('/get-calendar/', body).then(r => {
        this.calendar_data = r.data;
      }).catch((e) => {
        if (e.response.status === 401) {
          return router.push('/login');
        }
      })
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
    getData(use_cache = true, hotel_name = null) {
      if (!this.body.start_date || !this.body.end_date) {
        toast.error("لطفا تاریخ هارا وارد کنید", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
        return false;
      }
      if (this.body.night_count < 0) {
        toast.error("تاریخ برگشت نمیتواند قبل از تاریخ رفت باشد", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
        return false;
      }
      if (this.body.night_count < 3) {
        toast.error("تور شما نمیتواند کمتر از ۳ شب باشد", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
        return false;
      }
      this.body.night_count = parseInt(this.body.night_count);
      this.body.use_cache = use_cache;
      
      // Add hotelstarAnalysis parameter if hotel_name is provided
      if (hotel_name) {
        this.body.hotelstarAnalysis = [hotel_name];
      } else {
        this.body.hotelstarAnalysis = null;
      }
      
      this.$store.state.disable_header_link = true;
      this.loading = true;
      this.show_result = false;
      console.log("this.body == "+this.body);

      this.$http.post('/build-tour/', this.body).then(res => {
        console.log(res);

        this.data = res.data;
        this.provider_length = res.data.providers;
        this.filter_name = "";
        this.fixed_data = JSON.parse(JSON.stringify(res.data));

        this.show_result = true;
        this.sortedData();
        this.datakey++;
      }).catch((e) => {
        if (e.response.status === 401) {
          return router.push('/login');
        }
        else if (e.response.status === 504) {
          console.log("Error 504: Gateway Timeout. The server took too long to respond.");
          this.data = { message: "The server took too long to respond. Please try again later." }; 
        }
      }).finally(() => {
        this.$store.state.disable_header_link = false;
        this.loading = false;
        this.show_result = true;
      })
    },
    getAnalyseData(use_cache = true) {
      this.body.night_count = parseInt(this.body.night_count);
      this.show_analyse_loading = true;
      this.$store.state.disable_header_link = true;
      this.body.range = 7;
      this.body.use_cache = use_cache;
      console.log("Request Body:", this.body);
      this.dataKey++;

      this.$http.post('/build-tour-analyse/', this.body).then(res => {
        console.log("Analysis Response:", res.data);
        
        // Initialize analyse_data if it doesn't exist
        if (!this.analyse_data) {
          this.analyse_data = {};
        }

        // For each date in the new data
        Object.keys(res.data).forEach(date => {
          if (!this.analyse_data[date]) {
            // If date doesn't exist in current data, add it
            this.analyse_data[date] = res.data[date];
          } else {
            // If date exists, merge hotel data
            if (res.data[date].hotel && Array.isArray(res.data[date].hotel)) {
              res.data[date].hotel.forEach(newHotel => {
                const existingHotelIndex = this.analyse_data[date].hotel.findIndex(
                  h => h.hotel_name === newHotel.hotel_name
                );
                if (existingHotelIndex === -1) {
                  // If hotel doesn't exist for this date, add it
                  this.analyse_data[date].hotel.push(newHotel);
                } else {
                  // If hotel exists, update its data
                  this.analyse_data[date].hotel[existingHotelIndex] = newHotel;
                }
              });
            }
          }
        });

        // Force update of the analysis data
        this.$nextTick(() => {
          this.dataKey++;
        });
      }).catch(error => {
        console.error("Error fetching analysis data:", error);
        this.show_analyse_loading = false;
      }).finally(() => {
        this.$store.state.disable_header_link = false;
        this.show_analyse_loading = false;
      });
    },
    calcNighCount() {
      if (!this.body.start_date || !this.body.end_date) {
        this.body.night_count = 0;
        return false;
      }
      
      // Convert dates to moment objects for better date handling
      let startDate = moment(this.body.start_date);
      let endDate = moment(this.body.end_date);
      
      // Calculate the difference in days
      let total_days = endDate.diff(startDate, 'days');
      
      // If the difference is negative, make it positive
      if (total_days < 0) {
        total_days = Math.abs(total_days);
      }
      
      // Set the night count (number of days)
      this.body.night_count = total_days;
      
      return true;
    },
    goDateSubmit(value) {
      const date = value.georgian;
      this.body.start_date = `${date.gy}-${date.gm < 9 ? '0' : ''}${date.gm}-${date.gd < 9 ? '0' : ''}${date.gd}`;
      this.dataKey++;
      this.calcNighCount();
      if (!value.data) {
        toast.warning("در این تاریخ پروازی وجود ندارد.", {
          autoClose: 6000,
          position: "top-left",
          rtl: false,
          closeOnClick: true
        });
      }
    },
    returnDateSubmit(value) {
      const date = value.georgian;
      this.body.end_date = `${date.gy}-${date.gm < 9 ? '0' : ''}${date.gm}-${date.gd < 9 ? '0' : ''}${date.gd}`;
      this.dataKey++;
      this.calcNighCount();
      if (!value.data) {
        toast.warning("در این تاریخ پروازی وجود ندارد.", {
          autoClose: 6000,
          position: "top-left",
          rtl: false,
          closeOnClick: true
        });
      }
      if (this.body.start_date && this.body.end_date) {
        this.closeDatePickers();
      }
    },
    closeDatePickers() {
      this.show_datepicker_go = false;
      this.show_datepicker_return = false;
    },
    formatDisplayDate(date) {
      if (!date) return '';
      return moment_jalali(date).format('jYYYY/jMM/jDD');
    },
    openDatePicker(type) {
      if (type === 'go') {
        this.show_datepicker_go = true;
        this.show_datepicker_return = true;
      } else {
        this.show_datepicker_return = true;
        this.show_datepicker_go = true;
      }
    },
    handleShowAnalysis(hotelName) {
      // Set the hotelstarAnalysis parameter with the hotel name
      this.body.hotelstarAnalysis = [hotelName];
      // Call getAnalyseData to fetch the analysis data
      this.getAnalyseData(true);
    },
    refreshProvider(providerName) {
      if (this.loading) return;
      
      this.refreshingProvider = providerName;
      const refreshBody = {
        ...this.body,
        provider: providerName,
        use_cache: false
      };

      this.$http.post('/build-tour/', refreshBody).then(res => {
        // Update only the specific provider's data
        if (res.data && res.data.providers && res.data.providers[providerName]) {
          this.provider_length[providerName] = res.data.providers[providerName];
        }
        toast.success(`اطلاعات ${providerName} با موفقیت بروزرسانی شد`, {
          autoClose: 3000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
      }).catch((e) => {
        if (e.response.status === 401) {
          return router.push('/login');
        }
        toast.error(`خطا در بروزرسانی ${providerName}`, {
          autoClose: 3000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
      }).finally(() => {
        this.refreshingProvider = null;
      });
    },
  },
  computed: {
    isValidDate() {
      return !moment(this.body.start_date, "YYYY-MM-DD").isAfter(new Date());
    },
    backDate() {
      return moment(this.body.start_date, "YYYY-MM-DD").add(this.body.night_count, 'd').format("YYYY-MM-DD");
    },

    allProviderFilter: {
      get() {
        return Object.values(this.filter_provider).every(value => value === true);
      },
      set(value) {
        Object.keys(this.filter_provider).forEach(key => {
          this.filter_provider[key] = value;
        });
        this.filterProvider();
      }
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

      console.log(result);

      return result;
    },
    allProviderLength() {
      let result = 0;
      this.providerLength.forEach(pv => {
        result += pv.count;
      })
      return result
    },
  },
  

  watch: {
    filter_name() {
      this.sortedData();
    },

    filter_provider: {
    handler() {
      this.filterProvider();
    },
    deep: true, // watch for deep changes
  },
  // fixed_data: {
  //   handler() {
  //     this.filterProvider();
  //   },
  //   deep: true,
  // },

  },
  created() {

    // // this.show_analysis = this.$store.state.build_tour_data.show_analysis;
    // // this.loading_analysis = this.$store.state.build_tour_data.loading_analysis;
    // // this.analysis_data = this.$store.state.build_tour_data.analysis_data;
    // // this.order_by = this.$store.state.build_tour_data.order_by;
    // this.show_provider = this.$store.state.build_tour_data.show_provider;
    // this.filter_provider = this.$store.state.build_tour_data.filter_provider;
    // this.provider_length = this.$store.state.build_tour_data.provider_length;
    // // this.hotels_name = this.$store.state.build_tour_data.hotels_name;
    // // this.all_hotels_name = this.$store.state.build_tour_data.all_hotels_name;
    // // this.minimum_date = this.$store.state.build_tour_data.minimum_date;
    // // this.datepicker_min_date = this.$store.state.build_tour_data.datepicker_min_date;
    // this.filter_star = this.$store.state.build_tour_data.filter_star;
    // this.filter_name = this.$store.state.build_tour_data.filter_name;
    // this.body = this.$store.state.build_tour_data.body;
    // this.loading = this.$store.state.build_tour_data.loading;
    // // this.search_start = this.$store.state.build_tour_data.search_start;
    // // this.search_end = this.$store.state.build_tour_data.search_end;
    // // this.search_night_count = this.$store.state.build_tour_data.search_night_count;
    // this.fixed_data = this.$store.state.build_tour_data.fixed_data;
    // this.show_result = this.$store.state.build_tour_data.show_result;
    // // this.show_print = this.$store.state.build_tour_data.show_print;
    // this.data = this.$store.state.build_tour_data.data;
    // this.last_search = this.$store.state.build_tour_data.last_search;
    // this.show_hotel_anaysis = this.$store.state.build_tour_data.show_hotel_anaysis;

    // //
    // function formatDate(date) {
    //   var d = new Date(date),
    //       month = '' + (d.getMonth() + 1),
    //       day = '' + d.getDate(),
    //       year = d.getFullYear();

    //   if (month.length < 2)
    //     month = '0' + month;
    //   if (day.length < 2)
    //     day = '0' + day;

    //   return [year, month, day].join('-');
    // }

    // this.calc_last_search();
    // this.body.start_date = formatDate(new Date());
    // this.datepicker_min_date = formatDate(new Date());
    // const today = moment(this.body.start_date, "YYYY-MM-DD");
    // this.minimum_date = moment(today).subtract(1, 'd').format("YYYY-MM-DD");

    //
    // const data = this.$store.state.build_tour_data;
    // this.body = data.body;
    // this.data = {};
    // this.loading = data.loading;
    // this.show_result = data.show_result;
    // this.datepicker_min_date = data.datepicker_min_date;
    // this.minimum_date = data.minimum_date;
    //
    this.getCalendarData();
  },
  

  beforeUnmount() {
    
    this.$store.state.build_tour_data = this.$data;
  },
  
}
</script>

<style scoped>
.search-section {
  border: 1px solid #e9ecef;
}

.form-group {
  margin-bottom: 0;
}

.form-select {
  font-size: 0.9rem;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ced4da;
  background-color: #fff;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: none !important;
}

.form-select::-ms-expand {
  display: none;
}

.date-picker {
  position: relative;
}

/* Reset existing calendar styles */
.date-picker .c-datepicker-box {
  position: static !important;
  transform: none !important;
  width: 100% !important;
  max-width: none !important;
  min-width: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
  display: block !important;
  background: transparent !important;
}

.date-picker {
  width: 100%;
}

/* Calendar overlay container */
.calendar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  backdrop-filter: blur(3px);
}

.calendar-wrapper {
  background: white;
  border-radius: 10px;
  width: 98%;
  max-width: 1100px;
  height: 88vh;
  display: flex;
  flex-direction: column;
  position: relative;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.calendar-header {
  position: sticky;
  top: 0;
  background: white;
  padding: 10px 16px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
  border-radius: 10px 10px 0 0;
  background: linear-gradient(to right, #f8f9fa, #fff);
}

.calendar-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.calendar-close {
  width: 28px;
  height: 28px;
  border: none;
  background: #f8f9fa;
  border-radius: 50%;
  color: #666;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.calendar-close:hover {
  background: #e9ecef;
  color: #333;
  transform: rotate(90deg);
}

.calendar-container {
  display: flex;
  gap: 12px;
  padding: 12px;
  justify-content: center;
  align-items: flex-start;
  flex: 1;
  overflow: auto;
  background: linear-gradient(to bottom, #fff, #f8f9fa);
}

.calendar-box {
  flex: 1;
  max-width: 520px;
  min-width: 480px;
  background: #fff;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.calendar-box h5 {
  margin-bottom: 8px;
  font-size: 0.95rem;
  color: #2c3e50;
  text-align: center;
  font-weight: 600;
  padding-bottom: 6px;
  border-bottom: 1px solid #e9ecef;
}

/* Calendar Grid */
.date-picker .c-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
  margin-top: 6px;
}

/* Calendar Buttons */
.date-picker .c-button {
  width: 48px;
  height: 48px;
  margin: 0 auto;
  font-size: 0.85rem;
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 2px;
}

.date-picker .c-button:hover:not(.disable) {
  background: #f8f9fa;
  border-color: #dee2e6;
  transform: translateY(-1px);
}

.date-picker .c-button.active {
  background: #007bff;
  color: white;
  border-color: #0056b3;
}

.date-picker .c-button.active .c-price {
  color: rgba(255, 255, 255, 0.9);
}

.date-picker .c-button.disable {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f8f9fa;
}

.date-picker .c-button-title {
  width: 48px;
  height: 48px;
  margin: 0 auto;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #495057;
  font-size: 0.85rem;
}

.date-picker .c-day {
  font-size: 0.9rem;
  margin-bottom: 1px;
  font-weight: 500;
}

.date-picker .c-price {
  font-size: 0.75rem;
  color: #666;
}

/* Responsive Design */
@media (max-width: 1400px) {
  .calendar-box {
    min-width: 460px;
  }
  
  .date-picker .c-button,
  .date-picker .c-button-title {
    width: 45px;
    height: 45px;
  }
}

@media (max-width: 1200px) {
  .calendar-container {
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
  
  .calendar-box {
    max-width: 560px;
    width: 100%;
  }
  
  .date-picker .c-button,
  .date-picker .c-button-title {
    width: 50px;
    height: 50px;
  }
}

@media (max-width: 768px) {
  .calendar-wrapper {
    height: 92vh;
    width: 100%;
  }

  .calendar-box {
    min-width: auto;
    padding: 10px;
  }
  
  .date-picker .c-button,
.date-picker .c-button-title {
    width: 38px;
    height: 38px;
    font-size: 0.8rem;
  }
  
  .date-picker .c-day {
    font-size: 0.75rem;
    margin-bottom: 1px;
  }
  
  .date-picker .c-price {
    font-size: 0.65rem;
  }

  .calendar-container {
    padding: 8px;
    gap: 10px;
  }
}

/* Scrollbar Styling */
.calendar-container::-webkit-scrollbar {
  width: 6px;
}

.calendar-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.calendar-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.calendar-container::-webkit-scrollbar-thumb:hover {
  background: #bbb;
}

.provider-selector {
  cursor: pointer;
  transition: all 0.3s ease;
}

.provider-selector:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.provider-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
}

.provider-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.provider-modal-content {
  position: relative;
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: modalFadeIn 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.provider-modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  border-radius: 12px 12px 0 0;
}

.provider-modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.provider-list {
  max-height: calc(80vh - 200px);
  overflow-y: auto;
}

.provider-item {
  padding: 0.75rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  margin-bottom: 0.5rem;
  border: 1px solid #e9ecef;
  background-color: #fff;
}

.provider-item:hover {
  background-color: #f8f9fa;
  transform: translateX(4px);
  border-color: #dee2e6;
}

.provider-item.provider-loading {
  background-color: #fff3cd;
  border-color: #ffecb5;
}

.spinner-container {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.refresh-provider {
  padding: 0.35rem 0.75rem;
  font-size: 0.875rem;
  line-height: 1;
  border-radius: 0.25rem;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  border: 1px solid #0d6efd;
  background: transparent;
  color: #0d6efd;
}

.refresh-provider:hover:not(:disabled) {
  background: #0d6efd;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(13, 110, 253, 0.3);
}

.refresh-provider:disabled {
  cursor: not-allowed;
  opacity: 0.65;
  transform: none;
  box-shadow: none;
}

.refresh-provider.loading {
  background: #0d6efd;
  color: white;
  cursor: wait;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Custom scrollbar for provider list */
.provider-list::-webkit-scrollbar {
  width: 6px;
}

.provider-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.provider-list::-webkit-scrollbar-thumb {
  background: #0d6efd;
  border-radius: 3px;
}

.provider-list::-webkit-scrollbar-thumb:hover {
  background: #0b5ed7;
}

/* Form check styling */
.form-check-input {
  width: 1.1rem;
  height: 1.1rem;
  margin-top: 0;
  cursor: pointer;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.form-check-label {
  cursor: pointer;
  user-select: none;
}

/* Badge styling */
.badge {
  font-size: 0.85rem;
  padding: 0.35rem 0.65rem;
}

.provider-count {
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background: #f8f9fa;
  min-width: 40px;
  text-align: center;
}

.provider-icon {
  color: #0d6efd;
  font-size: 1.1rem;
}

/* Custom checkbox styling */
.custom-checkbox-container {
  position: relative;
  display: inline-flex;
  align-items: center;
  vertical-align: middle;
  cursor: pointer;
}

.custom-checkbox-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: 1;
}

.custom-checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-right: 25px;
  margin-bottom: 0;
}

.custom-checkbox-visual {
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  height: 18px;
  width: 18px;
  background-color: #eee;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.custom-checkbox-input:checked + .custom-checkbox-label .custom-checkbox-visual {
  background-color: #0d6efd;
  border-color: #0d6efd;
  transform: translateY(-50%) scale(1.05);
}

.custom-checkbox-visual::after {
  content: '';
  position: absolute;
  display: none;
  left: 5px;
  top: 1px;
  width: 6px;
  height: 12px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.custom-checkbox-input:checked + .custom-checkbox-label .custom-checkbox-visual::after {
  display: block;
}
</style>