<template>
  <section>
    <div class="row">
      <!-- --- FILTER --- -->
      <div class="col-12 col-md-3">
        <div class="sticky-top">
          <div class="row align-items-center bg-white p-3 rounded">
            <!-- --- تحلیل هتل --- -->
            <div class="col-12">
              <div class="d-flex flex-column">
                <label for="analysis_star" class="text-muted mb-2">تحلیل هتل ها</label>
                <div class="d-flex gap-2 align-items-center">
                  <v-select multiple 
                          :options="['1', '2','3','4','5']" 
                          v-model="filter.hotelstarAnalysis"
                          class="flex-grow-1 hotel-select"
                          placeholder="انتخاب ستاره هتل">
                    <template v-slot:option="{ label, value }">
                      <span :title="getStarErrorMessage(value)" :style="{ cursor: getStarErrorMessage(value) ? 'help' : 'default' }">
                        {{ label }}
                      </span>
                    </template>
                  </v-select>
                  <button class="btn btn-success px-3 analysis-btn" @click="extractAnalysis">
                    <i class="bi bi-search me-1"></i>
                    تحلیل
              </button>
                </div>
              </div>
            </div>

            <!-- --- NAME --- -->
            <div class="col-12 mt-3">
              <label for="filter_name" class="text-muted mb-2">هتل</label>
              <v-select multiple 
                      :options="hotelOptions" 
                      v-model="filter.hotel" 
                      :reduce="hotel => hotel.value"
                      label="label"
                      placeholder="انتخاب هتل"
                      class="hotel-select">
              </v-select>
            </div>

            <!-- --- SORT --- -->
            <div class="col-12 mt-3">
              <label for="order_by_filter" class="text-muted mb-2">مرتب سازی</label>
              <select class="form-select" id="order_by_filter" v-model="filter.orderBy" @change="sortHotels">
                <option value="price_a">قیمت - کم به زیاد</option>
                <option value="price_d">قیمت - زیاد به کم</option>
                <option value="go_time_a">ساعت پرواز رفت - کم به زیاد</option>
                <option value="go_time_d">ساعت پرواز رفت - زیاد به کم</option>
                <option value="return_time_a">ساعت پرواز برگشت - کم به زیاد</option>
                <option value="return_time_d">ساعت پرواز برگشت - زیاد به کم</option>
              </select>
            </div>

            <!-- --- ANALYSE BUTTON --- -->
            <div class="col-12 mt-3">
              <button class="btn btn-primary w-100" :disabled="analysis_loading" v-on:click="show_analysis = !show_analysis">
                <i class="fa fa-chart-line me-1"></i>
                <span>آنالیز هتلی</span>
                <i class="fa fa-spinner fa-spin ms-1" v-if="analysis_loading"></i>
              </button>
            </div>

            <build-tour-analyse v-if="show_analysis" @closeAnalysis="closeAnalysis"
                              :data="analysis_data" :adults="adults">
            </build-tour-analyse>
          </div>

          <!-- --- LAST UPDATE --- -->
          <div class="row mt-3 bg-white rounded p-3">
            <div class="col-6">
              <p class="m-0 text-muted">آخرین بروزرسانی:</p>
            </div>
            <div class="col-5">
              <p class="m-0">{{ last_search.minute }} {{ last_search.text }} پیش</p>
            </div>
            <div class="col-1 text-danger" v-if="last_search.warning">
              <i class="bi bi-exclamation-circle"></i>
            </div>
          </div>
        </div>
      </div>
      <!-- --- RESULT --- -->
      <div class="col-12 col-md-9 mt-3 mt-md-0">
        <div class="alert alert-warning text-center" v-if="!go_flight.length">
          <h5 class="m-0">پرواز رفت یافت نشد</h5>
        </div>
        <div class="alert alert-warning text-center" v-if="!return_flight.length">
          <h5 class="m-0">پرواز برگشت یافت نشد</h5>
        </div>
        <div class="alert alert-warning text-center" v-if="!hotels.length">
          <h5 class="m-0">هتل یافت نشد</h5>
        </div>
        <main>
          <build-component v-for="(tour, index) in hotels" :key="index" :index="index" :hotel="tour"
                           :adults="adults" :target="target" :source="source"
                           :analysis_data="analysis_data_here"
                           :analysis_loading="analysis_loading_here"
                           :go_flight="go_flight[go_flight_index]"
                           :go_flight_provider="go_flight_provider_index"
                           :return_flight="return_flight[return_flight_index]"
                           :return_flight_provider="return_flight_provider_index"
                           @show-analysis="handleShowAnalysis(tour.hotel_name)"></build-component>
        </main>
      </div>
    </div>
    <!-- --- GO FLIGHT MODAL --- -->
    <div class="modal modal-xl fade" id="build_tour_go_flight_modal" tabindex="-1"
         aria-labelledby="build_tour_go_flight_modal"
         aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">پرواز رفت</h1>
          </div>
          <div class="modal-body">
            <div v-for="(flight, index) in go_flight"
                 :key="index">
              <section :class="{'border rounded p-3 shadow-xs mt-3': true, 'flight-active': go_flight_index === index}">
                <div :class="{'row align-items-center': true}">
                  <!-- AIRLINE NAME -->
                  <div class="col-12 col-md-2">
                    <h5>{{ flight.airline_name }}</h5>
                    <h5 class="mt-2">{{ flight.flight_number }}</h5>
                  </div>
                  <!-- GO FLIGHT -->
                  <div class="col-5 col-md-3 mt-3 mt-md-0 text-center">
                    <h5 class="mt-2">{{ flight.go_time }}</h5>
                    <h5 class="mt-2">{{ flight.go_date }}</h5>
                  </div>
                  <!-- ICON -->
                  <div class="col-2 col-md-1 mt-3 mt-md-0 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor"
                         class="bi bi-airplane rotate-left" viewBox="0 0 16 16" data-v-12fb0470="">
                      <path
                          d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Zm.894.448C7.111 2.02 7 2.569 7 3v4a.5.5 0 0 1-.276.447l-5.448 2.724a.5.5 0 0 0-.276.447v.792l5.418-.903a.5.5 0 0 1 .575.41l.5 3a.5.5 0 0 1-.14.437L6.708 15h2.586l-.647-.646a.5.5 0 0 1-.14-.436l.5-3a.5.5 0 0 1 .576-.411L15 11.41v-.792a.5.5 0 0 0-.276-.447L9.276 7.447A.5.5 0 0 1 9 7V3c0-.432-.11-.979-.322-1.401C8.458 1.159 8.213 1 8 1c-.213 0-.458.158-.678.599Z"
                          data-v-12fb0470=""></path>
                    </svg>
                  </div>
                  <!-- RETURN FLIGHT -->
                  <div class="col-5 col-md-3 mt-3 mt-md-0 text-center">
                    <h5 class="mt-2">{{ flight.return_time }}</h5>
                    <h5 class="mt-2">{{ flight?.return_date }}</h5>
                  </div>
                  <!-- PRICE -->
                  <div class="col-12 col-md-3 mt-3 mt-md-0">
                    <div class="d-flex algin-items-center justify-content-between">
                      <h5>هر نفر:</h5>
                      <h5 class="text-center">{{ Number(flight.min_price).toLocaleString() }} تومان</h5>
                    </div>
                    <div class="mt-3 d-flex justify-content-between align-items-center">
                      <h5 class="text-center text-danger" v-if="calcGoFlightDif(flight.min_price) > 0">
                        <span :title="flight.providers[0]?.message || ''" :style="{ cursor: flight.providers[0]?.message ? 'help' : 'default' }">
                          {{ Number(Math.abs(calcGoFlightDif(flight.min_price))).toLocaleString() }}
                        </span>
                        <i class="fa fa-angle-up me-1"></i>
                      </h5>
                      <h5 class="text-center" v-else-if="calcGoFlightDif(flight.min_price) === 0">
                        <span :title="flight.providers[0]?.message || ''" :style="{ cursor: flight.providers[0]?.message ? 'help' : 'default' }">0</span>
                      </h5>
                      <h5 class="text-center text-success" v-else>
                        <span :title="flight.providers[0]?.message || ''" :style="{ cursor: flight.providers[0]?.message ? 'help' : 'default' }">
                          {{ Number(Math.abs(calcGoFlightDif(flight.min_price))).toLocaleString() }}
                        </span>
                        <i class="fa fa-angle-down me-1"></i>
                      </h5>
                      <button class="btn btn-primary w-50 " data-bs-toggle="collapse"
                              type="button" aria-expanded="false" v-on:click="showMoreGo(index)">
                        سایر ({{ flight.providers.length }})
                      </button>
                    </div>
                  </div>
                </div>
              </section>
              <div class="collapse show fade active" :id="`go_flight_modal_collapse_${index}`"
                   v-if="show_more_go_flight_index === index">
                <div :class="{'row': true}">
                  <div
                      :class="{'col-12 col-md-4 mt-4': true}"
                      v-for="(provider, providerIndex) in flight.providers" :key="providerIndex">
                    <div
                        :class="{'border p-3 rounded': true, 'flight-active': go_flight_index === index && providerIndex === go_flight_provider_index}"
                        :title="provider.message || ''"
                        :style="{
                          backgroundColor: provider.message ? '#ffebee' : 'transparent',
                          cursor: provider.message ? 'help' : 'default'
                        }"
                    >
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>{{ provider.provider_name }}</h5>
                        <img :src="provider.provider_logo" :alt="provider.provider_name" width="35" height="35">
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>{{ provider.go_date }}</h5>
                        <h5 class="mt-2">{{ provider.go_time }}</h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>{{ provider?.return_date }}</h5>
                        <h5 class="mt-2">{{ provider?.return_time }}</h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>تعداد صندلی</h5>
                        <h5 class="mt-2">{{ provider.seat }}</h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center mt-2">
                        <h5>هر نفر :</h5>
                        <h5 :title="provider.message || ''" :style="{ cursor: provider.message ? 'help' : 'default' }">
                          <span>{{ Number(provider.price).toLocaleString() }}</span>
                          <span> تومان </span>
                        </h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center mt-2">
                        <h5>قیمت کل :</h5>
                        <h5 :title="provider.message || ''" :style="{ cursor: provider.message ? 'help' : 'default' }">
                          <span>{{ Number(provider.price * adults).toLocaleString() }}</span>
                          <span> تومان </span>
                        </h5>
                      </div>
                      <hr>
                      <div class="">
                        <button v-if="go_flight_index === index && providerIndex === go_flight_provider_index"
                                class="btn btn-success w-100">انتخاب شده
                        </button>
                        <button v-on:click="setGoFlight(index, providerIndex)" class="btn btn-success w-100" v-else>
                          انتخاب
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
    <!-- --- RETURN FLIGHT MODAL --- -->
    <div class="modal modal-xl fade" id="build_tour_return_flight_modal" tabindex="-1"
         aria-labelledby="build_tour_return_flight_modal"
         aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">پرواز برگشت</h1>
          </div>
          <div class="modal-body">
            <div v-for="(flight, index) in return_flight"
                 :key="index">
              <section
                  :class="{'border rounded p-3 shadow-xs mt-3': true, 'flight-active': return_flight_index === index}">
                <div :class="{'row align-items-center': true}">
                  <!-- AIRLINE NAME -->
                  <div class="col-12 col-md-2">
                    <h5>{{ flight.airline_name }}</h5>
                    <h5 class="mt-2">{{ flight.flight_number }}</h5>
                  </div>
                  <!-- GO FLIGHT -->
                  <div class="col-5 col-md-3 mt-3 mt-md-0 text-center">
                    <h5 class="mt-2">{{ flight.go_time }}</h5>
                    <h5 class="mt-2">{{ flight.go_date }}</h5>
                  </div>
                  <!-- ICON -->
                  <div class="col-2 col-md-1 mt-3 mt-md-0 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor"
                         class="bi bi-airplane rotate-left" viewBox="0 0 16 16" data-v-12fb0470="">
                      <path
                          d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Zm.894.448C7.111 2.02 7 2.569 7 3v4a.5.5 0 0 1-.276.447l-5.448 2.724a.5.5 0 0 0-.276.447v.792l5.418-.903a.5.5 0 0 1 .575.41l.5 3a.5.5 0 0 1-.14.437L6.708 15h2.586l-.647-.646a.5.5 0 0 1-.14-.436l.5-3a.5.5 0 0 1 .576-.411L15 11.41v-.792a.5.5 0 0 0-.276-.447L9.276 7.447A.5.5 0 0 1 9 7V3c0-.432-.11-.979-.322-1.401C8.458 1.159 8.213 1 8 1c-.213 0-.458.158-.678.599Z"
                          data-v-12fb0470=""></path>
                    </svg>
                  </div>
                  <!-- RETURN FLIGHT -->
                  <div class="col-5 col-md-3 mt-3 mt-md-0 text-center">
                    <h5 class="mt-2">{{ flight.return_time }}</h5>
                    <h5 class="mt-2">{{ flight?.return_date }}</h5>
                  </div>
                  <!-- PRICE -->
                  <div class="col-12 col-md-3 mt-3 mt-md-0">
                    <div class="d-flex algin-items-center justify-content-between">
                      <h5>هر نفر:</h5>
                      <h5 class="text-center">{{ Number(flight.min_price).toLocaleString() }} تومان</h5>
                    </div>
                    <div class="mt-3 d-flex justify-content-between align-items-center">
                      <h5 class="text-center text-danger" v-if="calcReturnFlightDif(flight.min_price) > 0">
                        <span :title="flight.providers[0]?.message || ''" :style="{ cursor: flight.providers[0]?.message ? 'help' : 'default' }">
                          {{ Number(Math.abs(calcReturnFlightDif(flight.min_price))).toLocaleString() }}
                        </span>
                        <i class="fa fa-angle-up me-1"></i>
                      </h5>
                      <h5 class="text-center" v-else-if="calcReturnFlightDif(flight.min_price) === 0">
                        <span :title="flight.providers[0]?.message || ''" :style="{ cursor: flight.providers[0]?.message ? 'help' : 'default' }">0</span>
                      </h5>
                      <h5 class="text-center text-success" v-else>
                        <span :title="flight.providers[0]?.message || ''" :style="{ cursor: flight.providers[0]?.message ? 'help' : 'default' }">
                          {{ Number(Math.abs(calcReturnFlightDif(flight.min_price))).toLocaleString() }}
                        </span>
                        <i class="fa fa-angle-down me-1"></i>
                      </h5>
                      <button class="btn btn-primary w-50 " data-bs-toggle="collapse"
                              type="button" aria-expanded="false" v-on:click="showMoreReturn(index)">
                        سایر ({{ flight.providers.length }})
                      </button>
                    </div>
                  </div>
                </div>
              </section>
              <div class="collapse show fade active" :id="`return_flight_modal_collapse_${index}`"
                   v-if="show_more_return_flight_index === index">
                <div :class="{'row': true}">
                  <div
                      :class="{'col-12 col-md-4 mt-4': true}"
                      v-for="(provider, providerIndex) in flight.providers" :key="providerIndex">
                    <div
                        :class="{'border p-3 rounded': true, 'flight-active': return_flight_index === index && providerIndex === return_flight_provider_index}"
                        :title="provider.message || ''"
                        :style="{
                          backgroundColor: provider.message ? '#ffebee' : 'transparent',
                          cursor: provider.message ? 'help' : 'default'
                        }"
                    >
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>{{ provider.provider_name }}</h5>
                        <img :src="provider.provider_logo" :alt="provider.provider_name" width="35" height="35">
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>{{ provider.go_date }}</h5>
                        <h5 class="mt-2">{{ provider.go_time }}</h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>{{ provider?.return_date }}</h5>
                        <h5 class="mt-2">{{ provider?.return_time }}</h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <h5>تعداد صندلی</h5>
                        <h5 class="mt-2">{{ provider.seat }}</h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center mt-2">
                        <h5>هر نفر :</h5>
                        <h5 :title="provider.message || ''" :style="{ cursor: provider.message ? 'help' : 'default' }">
                          <span>{{ Number(provider.price).toLocaleString() }}</span>
                          <span> تومان </span>
                        </h5>
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center mt-2">
                        <h5>قیمت کل :</h5>
                        <h5 :title="provider.message || ''" :style="{ cursor: provider.message ? 'help' : 'default' }">
                          <span>{{ Number(provider.price * adults).toLocaleString() }}</span>
                          <span> تومان </span>
                        </h5>
                      </div>
                      <hr>
                      <div class="">
                        <button v-if="return_flight_index === index && providerIndex === return_flight_provider_index"
                                class="btn btn-success w-100">انتخاب شده
                        </button>
                        <button v-on:click="setReturnFlight(index, providerIndex)" class="btn btn-success w-100" v-else>
                          انتخاب
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
  </section>
</template>

<script>
import BuildComponent from "@/components/BuildTour/BuildComponent";
import BuildTourAnalyse from "@/components/BuildTour/BuildTourAnalyse";

export default {
  name: "BuildResult",
  components: {BuildTourAnalyse, BuildComponent},
  props: {
    data: {
      type: Object,
      required: true,
      validator(value) {
        return value && (value.hotel || value.flight);
      }
    },
    analysis_data: {
      type: Object,
      default: () => ({})
    },
    analysis_loading: {
      type: Boolean,
      default: false
    },
    adults: {
      type: Number,
      required: true
    },
    target: {
      type: String,
      required: true
    },
    source: {
      type: String,
      required: true
    },
    body: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      datakey: 0,
      body_new: {
        "start_date": "",
        "end_date": "",
        "night_count": 0,
        "hotel_star": 5,
        "source": this.source,
        "target": this.target,
        "adults": this.adults,
        "use_cache": false,
        "hotelstarAnalysis": []
      },
      analysis_loading_here: false,
      analysis_data_here: {},
      go_flight_index: 0,
      go_flight_provider_index: 0,
      show_more_go_flight_index: -1,
      return_flight_index: 0,
      return_flight_provider_index: 0,
      show_more_return_flight_index: -1,
      static_hotels: [],
      hotels: [],
      go_flight: [],
      return_flight: [],
      show_analysis: false,
      last_search: {
        date: new Date(),
        minute: 0,
        text: "ثانیه",
        interval: null,
        warning: false
      },
      filter: {
        hotel: [],
        selected_star_analysis: [],
        orderBy: "price_a"
      }
    }
  },
  methods: {
    initializeData() {
      try {
        if (this.data?.hotel?.length) {
          this.static_hotels = [...this.data.hotel];
          this.hotels = [...this.data.hotel];
        } else {
          this.static_hotels = [];
          this.hotels = [];
        }
        
        this.go_flight = this.getGoFlights();
        this.return_flight = this.getReturnFlights();
        this.calc_last_search();
        
        if (this.hotels.length) {
          this.sortHotels();
        }
        
        this.datakey++;
      } catch (error) {
        console.error("Error initializing data:", error);
      }
    },
    extractAnalysis() {
      this.analysis_loading_here = true;
      
      this.body_new = {
        ...this.body,
        hotelstarAnalysis: this.filter.hotelstarAnalysis
      };

      console.log("Sending request with body:", this.body_new);

      this.$http.post('/build-tour-analyse/', this.body_new, { timeout: 600000000 })
        .then(res => {
          console.log("Received analysis data:", res.data);
          this.analysis_data_here = res.data;
          // Emit event to notify parent component
          this.$emit('update:analysis_data', res.data);
          this.analysis_loading_here = false;
          this.datakey++;
        })
        .catch((e) => {
          console.error("Error in analysis request:", e);
          if (e.response && e.response.status === 401) {
            return this.$router.push('/login');
          } else if (e.response && e.response.status === 504) {
            this.analysis_data_here = { message: "The server took too long to respond. Please try again later." };
          }
        })
        .finally(() => {
          this.analysis_loading_here = false;
        });
    },
    getGoFlights() {
      try {
        if (!this.data?.flight?.go_flight) {
          console.warn("No go flight data available");
          return [];
        }

        return this.data.flight.go_flight.reduce((result, flight) => {
          const providers = flight.providers.filter(flg => flg.seat >= this.adults);
          if (providers.length) {
            result.push({
              ...flight,
              providers
            });
          }
          return result;
        }, []);

    } catch (error) {
        console.error("Error in getGoFlights:", error);
        return [];
      }
    },
    getReturnFlights() {
      try {
        if (!this.data?.flight?.return_flight) {
          console.warn("No return flight data available");
          return [];
        }

        return this.data.flight.return_flight.reduce((result, flight) => {
          const providers = flight.providers.filter(flg => flg.seat >= this.adults);
          if (providers.length) {
            result.push({
              ...flight,
              providers
            });
          }
          return result;
        }, []);

    } catch (error) {
        console.error("Error in getReturnFlights:", error);
        return [];
    }
    },
    setGoFlight(index, provider_index) {
      this.go_flight_index = index;
      this.go_flight_provider_index = provider_index;
    },
    setReturnFlight(index, provider_index) {
      this.return_flight_index = index;
      this.return_flight_provider_index = provider_index;
    },
    showMoreGo(index) {
      this.show_more_go_flight_index = this.show_more_go_flight_index === index ? -1 : index;
    },
    showMoreReturn(index) {
      this.show_more_return_flight_index = this.show_more_return_flight_index === index ? -1 : index;
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
    calcGoFlightDif(price) {
      const current_price = this.go_flight[this.go_flight_index].providers[this.go_flight_provider_index].price;
      return price - current_price;
    },
    calcReturnFlightDif(price){
      const current_price = this.return_flight[this.return_flight_index].providers[this.return_flight_provider_index].price;
      return price - current_price;
    },
    closeAnalysis(val) {
      return this.show_analysis = val;
    },
    handleShowAnalysis(hotelName) {
      this.$emit('show-analysis', hotelName);
    },
    sortHotels() {
      if (!this.hotels.length) return;
      
      // Handle price sorting
      if (this.filter.orderBy === "price_a" || this.filter.orderBy === "price_d") {
        const sortedHotels = [...this.hotelPrices].sort((a, b) => {
          return this.filter.orderBy === "price_a" 
            ? a.totalPrice - b.totalPrice 
            : b.totalPrice - a.totalPrice;
        });
        
        this.hotels = sortedHotels.map(item => item.hotel);
        return;
      }
      
      // Handle flight time sorting
      const flightTimes = this.flightTimes;
      
      this.hotels.forEach(hotel => {
        const times = flightTimes.get(hotel.id);
        if (!times) return;
        
        if (this.filter.orderBy === "go_time_a" || this.filter.orderBy === "go_time_d") {
          const sortedGoTimes = [...times.goTimes].sort((a, b) => {
            const timeA = this.parseTime(a.time);
            const timeB = this.parseTime(b.time);
            return this.filter.orderBy === "go_time_a" ? timeA - timeB : timeB - timeA;
          });
          
          if (sortedGoTimes.length) {
            this.go_flight_index = sortedGoTimes[0].flightIndex;
            this.go_flight_provider_index = sortedGoTimes[0].providerIndex;
          }
        }
        
        if (this.filter.orderBy === "return_time_a" || this.filter.orderBy === "return_time_d") {
          const sortedReturnTimes = [...times.returnTimes].sort((a, b) => {
            const timeA = this.parseTime(a.time);
            const timeB = this.parseTime(b.time);
            return this.filter.orderBy === "return_time_a" ? timeA - timeB : timeB - timeA;
          });
          
          if (sortedReturnTimes.length) {
            this.return_flight_index = sortedReturnTimes[0].flightIndex;
            this.return_flight_provider_index = sortedReturnTimes[0].providerIndex;
          }
        }
      });
    },
    parseTime(time) {
      const [hours, minutes] = time.split(':').map(Number);
      return hours * 60 + minutes;
    },
    getStarErrorMessage(star) {
      if (!this.analysis_data_here || !this.analysis_data_here.hotel_star) return '';
      
      const starData = this.analysis_data_here.hotel_star.find(s => s.star === star);
      if (!starData || !starData.count) {
        return 'داده‌ای برای این ستاره موجود نیست';
      }
      return '';
    }
  },
  created() {
    this.initializeData();
  },
  watch: {
    data: {
      handler(newData) {
        if (newData && Object.keys(newData).length > 0) {
          this.initializeData();
        }
      },
      deep: true,
      immediate: true
    },
    analysis_data: {
      handler(newData) {
        console.log("Analysis Data in BuildResult:", newData);
        this.analysis_data_here = newData;
      },
      deep: true,
      immediate: true
    },
    "filter.hotel": {
      handler(val) {
      if (val.length) {
          this.hotels = this.static_hotels.filter(hotel => 
            val.includes(hotel.hotel_name)
          );
        } else {
          this.hotels = [...this.static_hotels];
        }
        this.sortHotels();
      }
    },
    "filter.orderBy": {
      handler() {
        this.sortHotels();
      }
    }
  },
  unmounted() {
    clearInterval(this.last_search.interval);
  },
  computed: {
    hotelOptions() {
      if (!this.data || !this.data.hotel) return [];
      return this.data.hotel.map(hotel => ({
        label: `${hotel.hotel_name} (${hotel.hotel_star} ستاره)`,
        value: hotel.hotel_name
      }));
    },
    hotelPrices() {
      if (!this.hotels.length) return [];
      
      return this.hotels.map(hotel => {
        const goFlight = this.go_flight[this.go_flight_index];
        const returnFlight = this.return_flight[this.return_flight_index];
        
        let goPrice = 0;
        let returnPrice = 0;
        
        if (goFlight?.providers) {
          const hotelProvider = goFlight.providers.find(p => p.hotel_id === hotel.id);
          if (hotelProvider) goPrice = hotelProvider.price;
        }
        
        if (returnFlight?.providers) {
          const hotelProvider = returnFlight.providers.find(p => p.hotel_id === hotel.id);
          if (hotelProvider) returnPrice = hotelProvider.price;
        }
        
        const flightPrice = (goPrice + returnPrice) * this.adults;
        const hotelPrice = hotel.min_price * this.adults;
        
        return {
          hotel,
          totalPrice: flightPrice + hotelPrice
        };
      });
    },
    flightTimes() {
      const times = new Map();
      
      this.hotels.forEach(hotel => {
        const goTimes = [];
        const returnTimes = [];
        
        this.go_flight.forEach((flight, flightIndex) => {
          flight.providers.forEach((provider, providerIndex) => {
            if (provider.hotel_id === hotel.id) {
              goTimes.push({
                time: provider.go_time || "00:00",
                flightIndex,
                providerIndex
              });
            }
          });
        });
        
        this.return_flight.forEach((flight, flightIndex) => {
          flight.providers.forEach((provider, providerIndex) => {
            if (provider.hotel_id === hotel.id) {
              returnTimes.push({
                time: provider.return_time || "00:00",
                flightIndex,
                providerIndex
              });
            }
          });
        });
        
        times.set(hotel.id, { goTimes, returnTimes });
      });
      
      return times;
    }
  }
}
</script>

<style scoped>
.flight-active {
  background: #c0e3ca !important;
  transition: all .5s;
}

.hotel-select {
  direction: rtl;
  text-align: right;
}

.hotel-select ::v-deep .vs__dropdown-toggle {
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #ced4da;
  background-color: #fff;
}

.hotel-select ::v-deep .vs__selected {
  margin: 0 2px;
  padding: 0 8px;
  background: #e9ecef;
  border-radius: 4px;
  font-size: 0.85rem;
}

.hotel-select ::v-deep .vs__dropdown-menu {
  text-align: right;
  font-size: 0.85rem;
}

.hotel-select ::v-deep .vs__dropdown-option {
  font-size: 0.85rem;
  padding: 8px 12px;
}

.hotel-select ::v-deep .vs__search {
  margin: 0;
  font-size: 0.85rem;
}

.analysis-btn {
  height: 38px;
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.btn {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-success {
  background-color: #198754;
  border-color: #198754;
}

.form-select {
  font-size: 0.85rem;
  padding: 0.5rem;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: none !important;
}

.form-select::-ms-expand {
  display: none;
}

.sticky-top {
  top: 1rem;
}
</style>