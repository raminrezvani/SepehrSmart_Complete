<template>
  <section>
    <div class="border rounded p-3 bg-white build-tour-component shadow-xs mt-4">
      <div class="row align-items-center">
        <!-- ---- HOTEL ---- -->
        <div class="col-12 col-md-4">
          <h5 class="text-muted">تور شماره {{ index + 1 }}</h5>
          <h5 class="mt-5 fw-bold">{{ hotel.hotel_name }} ({{ hotel.hotel_star }} ستاره)</h5>
          <!-- <h5 class="mt-2">{{ hotel.rooms[0].name }}</h5> -->
          <h5 class="mt-2" v-if="hotel.rooms && hotel.rooms.length > 0">{{ hotel.rooms[0].name }}</h5>

        </div>
        <hr class="col-12 d-md-none mt-3">
        <!-- ---- FLIGHTS ---- -->
        <div class="col-12 col-md-8 border-end p-0">
          <!-- ---- GO FLIGHT ---- -->
          <div class="row align-items-center px-2">
            <div class="col-12 col-md-3 d-flex justify-content-between align-items-center d-md-block mt-3 mt-md-0">
              <h5>{{ go_flight.airline_name }}</h5>
              <h5>{{ go_flight.flight_number }}</h5>
            </div>
            <div class="col-5 col-md-2 text-center mt-3 mt-md-0">
              <p class="m-0 text-muted">{{getSource()}}</p>
              <h5>{{ go_flight.go_time }}</h5>
            </div>
            <div class="col-2 col-md-1 mt-3 mt-md-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor"
                   class="bi bi-airplane rotate-left"
                   viewBox="0 0 16 16">
                <path
                    d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Zm.894.448C7.111 2.02 7 2.569 7 3v4a.5.5 0 0 1-.276.447l-5.448 2.724a.5.5 0 0 0-.276.447v.792l5.418-.903a.5.5 0 0 1 .575.41l.5 3a.5.5 0 0 1-.14.437L6.708 15h2.586l-.647-.646a.5.5 0 0 1-.14-.436l.5-3a.5.5 0 0 1 .576-.411L15 11.41v-.792a.5.5 0 0 0-.276-.447L9.276 7.447A.5.5 0 0 1 9 7V3c0-.432-.11-.979-.322-1.401C8.458 1.159 8.213 1 8 1c-.213 0-.458.158-.678.599Z"/>
              </svg>
            </div>
            <div class="col-5 col-md-2 text-center mt-3 mt-md-0">
              <p class="m-0 text-muted">{{ getTarget() }}</p>
              <h5>{{ go_flight.return_time }}</h5>
            </div>
            <div class="col-6 col-md-2 mt-3 mt-md-0">
              <button class="btn btn-success w-100" data-bs-toggle="modal" data-bs-target="#build_tour_go_flight_modal">
                تغییر
              </button>
            </div>
            <div class="col-6 col-md-2 mt-3 mt-md-0">
              <a :href="go_flight.providers[go_flight_provider].buy_link" target="_blank" class="btn btn-warning w-100">ارجاع</a>
            </div>
          </div>
          <hr>
          <!-- ---- RETURN FLIGHT ---- -->
          <div class="row align-items-center px-2">
            <div class="col-12 col-md-3 d-flex justify-content-between align-items-center d-md-block mt-3 mt-md-0">
              <h5>{{ return_flight.airline_name }}</h5>
              <h5>{{ return_flight.flight_number }}</h5>
            </div>
            <div class="col-5 col-md-2 text-center mt-3 mt-md-0">
              <p class="m-0 text-muted">{{ getTarget() }}</p>
              <h5>{{ return_flight.go_time }}</h5>
            </div>
            <div class="col-2 col-md-1 mt-3 mt-md-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor"
                   class="bi bi-airplane rotate-right"
                   viewBox="0 0 16 16">
                <path
                    d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849Zm.894.448C7.111 2.02 7 2.569 7 3v4a.5.5 0 0 1-.276.447l-5.448 2.724a.5.5 0 0 0-.276.447v.792l5.418-.903a.5.5 0 0 1 .575.41l.5 3a.5.5 0 0 1-.14.437L6.708 15h2.586l-.647-.646a.5.5 0 0 1-.14-.436l.5-3a.5.5 0 0 1 .576-.411L15 11.41v-.792a.5.5 0 0 0-.276-.447L9.276 7.447A.5.5 0 0 1 9 7V3c0-.432-.11-.979-.322-1.401C8.458 1.159 8.213 1 8 1c-.213 0-.458.158-.678.599Z"/>
              </svg>
            </div>
            <div class="col-5 col-md-2 text-center mt-3 mt-md-0">
              <p class="m-0 text-muted">{{ getSource() }}</p>
              <h5>{{ return_flight.return_time }}</h5>
            </div>
            <div class="col-6 col-md-2 mt-3 mt-md-0">
              <button class="btn btn-success w-100" data-bs-toggle="modal"
                      data-bs-target="#build_tour_return_flight_modal">تغییر
              </button>
            </div>
            <div class="col-6 col-md-2 mt-3 mt-md-0">
              <a :href="return_flight.providers[return_flight_provider].buy_link" target="_blank"
                 class="btn btn-warning w-100">ارجاع</a>
            </div>
          </div>
        </div>
        <hr class="col-12 mt-3">
        <!-- ---- SERVICES ---- -->
        <div class="col-12 col-md-4">
          <div class="button-group d-flex gap-2 flex-wrap">
            <button :class="['btn flex-grow-1', {
              'btn-warning': analysis_loading,
              'btn-success': show_analysis && !analysis_loading,
              'btn-info': !show_analysis && !analysis_loading
            }]" 
            :disabled="false" 
            v-on:click="showAnalysis">
              <i class="fa fa-spinner fa-spin ms-1" v-if="analysis_loading"></i>
              <span v-if="show_analysis && !analysis_loading">بستن آنالیز</span>
              <span v-else-if="analysis_loading">در حال دریافت اطلاعات...</span>
              <span v-else>نمایش آنالیز</span>
            </button>

            <button class="btn btn-primary flex-grow-1" v-on:click="show_costs = !show_costs">
              <span v-if="show_costs">بستن هزینه‌ها</span>
              <span v-else>نمایش هزینه‌ها</span>
            </button>

            <button class="btn btn-info flex-grow-1" v-on:click="show_chart = !show_chart">
              <span v-if="show_chart">بستن نمودار</span>
              <span v-else>نمایش نمودار</span>
            </button>
          </div>

          <!-- هزینه ترانسفر -->
          <div class="mt-3" v-if="show_costs">
            <label class="form-label">هزینه ترانسفر</label>
            <div class="input-group">
              <input type="number" class="form-control" v-model="transfer_cost" min="0" placeholder="مبلغ ترانسفر">
              <span class="input-group-text">تومان</span>
            </div>
          </div>

          <!-- هزینه گشت -->
          <div class="mt-3" v-if="show_costs">
            <label class="form-label">هزینه گشت</label>
            <div class="input-group">
              <input type="number" class="form-control" v-model="tour_cost" min="0" placeholder="مبلغ گشت">
              <span class="input-group-text">تومان</span>
            </div>
          </div>

          
          <!--          <p class="m-0">خدمات :</p>-->
          <!--          <ul class="m-0 p-0 px-2">-->
          <!--            <li>استقبال فرودگاهی</li>-->
          <!--            <li>تخفیفات گردشگری</li>-->
          <!--            <li>صبحانه</li>-->
          <!--          </ul>-->
        </div>
        <!-- ---- MORE ---- -->
        <div class="col-12 col-md-8 align-items-center">
          <div class="row align-item-center">
            <!-- ---- PRICE PER PERSON ---- -->
            <div class="col-12 col-md-4">
              <div class="d-block text-center justify-content-between align-items-center">
                <p class="m-0">قیمت هر نفر :</p>
                <h5 class="m-0">{{ roomPersonPrice(hotel.rooms[room_index]?.price,hotel.rooms[room_index]?.capacity) }} تومان</h5>
                

              </div>
            </div>
            <!-- ---- PRICE TOTAL ---- -->
            <div class="col-12 col-md-4">
              <div
                  class="d-block text-center justify-content-between justify-content-md-end align-items-center mt-3 mt-md-0">
                <p class="m-0">قیمت کل :</p>
                <h5 class="m-0">{{ roomPrice(hotel.rooms[room_index]?.price,hotel.rooms[room_index]?.capacity) }} تومان</h5>
              </div>
            </div>
            <!-- ---- MORE ROOMS ---- -->
            <div class="col-12 col-md-2 mt-3 mt-md-0">
              <button class="btn btn-success w-100" v-on:click="showRooms">تغییر</button>
            </div>
            <!-- ---- BUY ---- -->
            <div class="col-12 col-md-2 mt-3 mt-md-0">
              <a :href="hotel.rooms[room_index]?.buy_link" target="_blank" class="btn btn-warning w-100">ارجاع</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- --- ROOMS --- -->
    <div class="p-3" v-if="show_rooms">
      <div :class="{'border rounded p-3 mt-3': true, 'room-active': index === room_index}"
           v-for="(room, index) in hotel.rooms" :key="index">
        <div class="row align-items-center">
          <div class="col-6 col-md-4">
            <h5>{{ room.name }}</h5>
            <p class="m-0 text-muted">{{ priceFilter(room.price) }}</p>
          </div>
          <div class="col-6 col-md-3 text-center">
            <p class="m-0 text-muted">قیمت هر نفر</p>
            <h5>{{ roomPersonPrice(room.price,room.capacity) }}</h5>
          </div>
          <div class="col-6 col-md-3 text-center mt-3 mt-md-0">
            <p class="m-0 text-muted">قیمت کل</p>
            <h5>{{ roomPrice(room.price,room.capacity) }}</h5>
          </div>
          <div class="col-6 col-md-2 mt-3 mt-md-0 text-center">
            <p class="m-0">{{ room.provider }}</p>
            <button class="btn btn-primary w-100" v-on:click="room_index = index" v-if="index === room_index">انتخاب شده
            </button>
            <button class="btn btn-primary w-100" v-on:click="room_index = index" v-else>انتخاب</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- --- CHART --- -->
    <div class="p-3" v-if="show_chart">
      <!-- Dropdown above the chart -->
      <div class="mb-3">
        <select v-model="selectedOption" @change="onSelectChange" class="form-select">
          <option value="all">همه</option>
          <option value="oneCapacity">یک نفر</option>
          <option value="twoCapacity">دو نفر</option>
          <option value="threeCapacity">سه نفر</option>
          <option value="fourCapacity">چهار نفر</option>
        </select>
      </div>

      <div v-if="analysis_loading" class="text-center">
        <i class="fa fa-spinner fa-spin fa-2x"></i>
      </div>

      <div v-else>
        <apexchart
          ref="chart"
          type="bar"
          height="550"
          :options="chartOptions"
          :series="series"
          :key="dataKey"
        ></apexchart>
      </div>
    </div>
  </section>
</template>

<script>
import moment_jalali from "moment-jalaali";

export default {
  name: "BuildComponent",
  props: {
    index: Number,
    hotel: Object,
    go_flight: Object,
    go_flight_provider: Number,
    return_flight: Object,
    return_flight_provider: Number,
    adults: Number,
    target: String,
    source:String,
    analysis_data: Object,
    analysis_loading: Boolean
  },
  data() {
    return {
      selectedOption:'',
      dataKey: 0, // Initialize a key for the component
      show_rooms: false,
      show_chart: false,  // Initialize show_chart as false
      room_index: 0,
      sorted_rooms: [],
      show_analysis: false,
      series: [],
      chartOptions: {
        chart: {
          height: 550,
          type: 'bar',
          toolbar: {
            show: false,
            autoSelected: 'selection'
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        colors: ['#006600'],
        xaxis: {
          type: 'category',
          categories: []
        },
        tooltip: {
          custom: this.customTooltip
        }
      },
      transfer_cost: 0,
      tour_cost: 0,
      show_costs: false,
    }
  },
  methods: {
    onSelectChange(){
      if (this.selectedOption=='oneCapacity'){
        this.callFuntion('1');
      }
      if (this.selectedOption=='twoCapacity'){
        this.callFuntion('2');
      }
      if (this.selectedOption=='threeCapacity'){
        this.callFuntion('3');
      }
      if (this.selectedOption=='fourCapacity'){
        this.callFuntion('4');
      }
      

      if (this.selectedOption=='all'){
        this.callFuntion('all');
      }
      this.updateChartData()
      console.log("update chart")
      
    },
    
    callFuntion(roomType) {
      console.log("Analysis Data:", this.analysis_data);
      
      if (!this.analysis_data || Object.keys(this.analysis_data).length === 0) {
        console.log("No analysis data available");
        return;
      }

      // Initialize series with current hotel
      this.series = [{
        name: this.hotel.hotel_name,
        data: []
      }];
      this.chartOptions.xaxis.categories = [];
      
      // Process each date in analysis_data
      Object.keys(this.analysis_data).forEach(date => {
        const hotel_date = moment_jalali(date).format("jYYYY/jMM/jDD");
        this.chartOptions.xaxis.categories.push(hotel_date);
        
        try {
          const dateData = this.analysis_data[date];
          if (dateData && dateData.hotel && Array.isArray(dateData.hotel)) {
            const hotelData = dateData.hotel.find(h => h.hotel_name === this.hotel.hotel_name);
            
            if (hotelData && hotelData.rooms) {
              let matchingRooms = hotelData.rooms.filter(room => {
                if (roomType === 'all') return true;
                return room.capacity === parseInt(roomType);
              });

              if (matchingRooms.length > 0) {
                let minRoom = matchingRooms.reduce((prev, curr) => (prev.price < curr.price ? prev : curr));
                
                this.series[0].data.push({
                  price: minRoom.price,
                  hotel_name: hotelData.hotel_name,
                  room_name: minRoom.name,
                  provider: minRoom.provider,
                  y: minRoom.price,
                  x: hotel_date
                });
              } else {
                // If no matching rooms found, use the cheapest room available
                let allRooms = hotelData.rooms;
                if (allRooms.length > 0) {
                  let cheapestRoom = allRooms.reduce((prev, curr) => (prev.price < curr.price ? prev : curr));
                  this.series[0].data.push({
                    price: cheapestRoom.price,
                    hotel_name: hotelData.hotel_name,
                    room_name: cheapestRoom.name,
                    provider: cheapestRoom.provider,
                    y: cheapestRoom.price,
                    x: hotel_date
                  });
                } else {
                  this.series[0].data.push({
                    price: 0,
                    hotel_name: this.hotel.hotel_name,
                    room_name: '',
                    provider: '',
                    y: 0,
                    x: hotel_date
                  });
                }
              }
            } else {
              this.series[0].data.push({
                price: 0,
                hotel_name: this.hotel.hotel_name,
                room_name: '',
                provider: '',
                y: 0,
                x: hotel_date
              });
            }
          } else {
            console.log("Invalid date data structure:", dateData);
            this.series[0].data.push({
              price: 0,
              hotel_name: this.hotel.hotel_name,
              room_name: '',
              provider: '',
              y: 0,
              x: hotel_date
            });
          }
        } catch (error) {
          console.error("Error processing date data:", error);
          this.series[0].data.push({
            price: 0,
            hotel_name: this.hotel.hotel_name,
            room_name: '',
            provider: '',
            y: 0,
            x: hotel_date
          });
        }
      });

      // Sort data points by date using moment_jalali
      this.series[0].data.sort((a, b) => moment_jalali(a.x, "jYYYY/jMM/jDD").valueOf() - moment_jalali(b.x, "jYYYY/jMM/jDD").valueOf());
      this.chartOptions.xaxis.categories.sort((a, b) => moment_jalali(a, "jYYYY/jMM/jDD").valueOf() - moment_jalali(b, "jYYYY/jMM/jDD").valueOf());

      console.log("Final series data:", this.series);

      // Force chart update
      this.$nextTick(() => {
        if (this.$refs.chart) {
          this.$refs.chart.updateOptions({
            xaxis: {
              categories: this.chartOptions.xaxis.categories
            }
          });
          this.$refs.chart.updateSeries(this.series);
        }
      });
      
      this.dataKey++;
    },
  
  

    customTooltip({seriesIndex, dataPointIndex}) {

      // console.log(this.series)
      return '<div class="arrow_box p-3">' +
          '<p class="text-truncate">' + this.series[seriesIndex].data[dataPointIndex].room_name + '</p>' +
          '<p class="text-truncate">' + this.series[seriesIndex].data[dataPointIndex].provider + '</p>' +
          '<p class="text-truncate">هر نفر (نت) : ' + this.pricePersonFilter(this.series[seriesIndex].data[dataPointIndex].price) + '</p>' +
          '<p class="text-truncate">کل (نت) : ' + this.priceFilter(this.series[seriesIndex].data[dataPointIndex].price) + '</p>' +
          // '<p class="text-truncate">کل (نت) : ' + this.priceFilter(this.series[seriesIndex].data[dataPointIndex].price) + '</p>' +
          '</div>'
    },
    showAnalysis() {
      this.show_rooms = false;
      this.show_analysis = !this.show_analysis;
      
      if (this.show_analysis) {
        console.log("Emitting show-analysis event with hotel name:", this.hotel.hotel_name);
        this.$emit('show-analysis', this.hotel.hotel_name);
        this.selectedOption = 'all';
        
        // Initialize empty chart
        this.series = [{
          name: "نام هتل",
          data: []
        }];
        this.chartOptions.xaxis.categories = [];
        
        // If we already have analysis data, update the chart
        if (this.analysis_data && Object.keys(this.analysis_data).length > 0) {
          console.log("Updating chart with existing analysis data:", this.analysis_data);
          this.$nextTick(() => {
            this.setAnalysis();
            this.callFuntion('all');
          });
        }
      }
      
      this.dataKey++;
    },
    showRooms() {
      this.show_rooms = !this.show_rooms;
      this.show_analysis = false;
    },
  roomPrice(price, capacity) {
    if (!price || !capacity) return 0;

    // تبدیل هزینه‌ها به عدد برای جلوگیری از خطا
    const transferCost = Number(this.transfer_cost) || 0;
    const tourCost = Number(this.tour_cost) || 0;

    // محاسبه قیمت پایه شامل قیمت اتاق، پروازها، ترانسفر و گشت به‌ازای هر نفر
    const resultPerPerson = (price / capacity) + 
      this.go_flight.providers[this.go_flight_provider].price + 
      this.return_flight.providers[this.return_flight_provider].price + 
      transferCost + 
      tourCost;

    // محاسبه قیمت کل با ضرب در تعداد مسافران
    return Number(Math.round(resultPerPerson * this.adults)).toLocaleString();
  },

    // roomPrice(price, capacity) {
    //   if (!price || !capacity) return 0;
      
    //   // محاسبه قیمت پایه شامل قیمت اتاق و پروازها
    //   const result = (price / capacity) + 
    //     this.go_flight.providers[this.go_flight_provider].price + 
    //     this.return_flight.providers[this.return_flight_provider].price;
      
    //   // محاسبه قیمت کل با ضرب در تعداد مسافران
    //   return Number(Math.round(result * this.adults)).toLocaleString();
    // },
    roomPersonPrice(price,capacity) {

      const result = (price / capacity) + this.go_flight.providers[this.go_flight_provider].price + this.return_flight.providers[this.return_flight_provider].price;

      if (isNaN(result)){
        console.log( capacity)

      }

      return Number(Math.round(result)).toLocaleString();

      // old code
      // const result = (price / this.adults) + this.go_flight.providers[this.go_flight_provider].price + this.return_flight.providers[this.return_flight_provider].price;
      // return Number(Math.round(result)).toLocaleString();
    },
    priceFilter(price) {
      // console.log(price)
      return Number(price).toLocaleString();
    },
    pricePersonFilter(price) {
      return Number(price / this.adults).toLocaleString();
      
    },
    getTarget() {
      const targets = {
        "KIH": "کیش",
        "GSM": "قشم",
        "MHD":"مشهد",
        "THR":"تهران",

        'SYZ': 'شیراز',
        'IFN': 'اصفهان',
        'AZD': 'یزد',
        'TBZ': 'تبریز',

      }
      return targets[this.target]
    },
    getSource() {
      const sources = {
        "KIH": "کیش",
        "GSM": "قشم",
        "MHD":"مشهد",
        "THR":"تهران",

        'SYZ': 'شیراز',
        'IFN': 'اصفهان',
        'AZD': 'یزد',
        'TBZ': 'تبریز',

      }
      // console.log("printttt "+this.source)
      return sources[this.source]
    },
    setAnalysis() {
      console.log("Setting analysis with data:", this.analysis_data);

      if (!this.analysis_data || Object.keys(this.analysis_data).length === 0) {
        console.log("No analysis data available");
        return;
      }

      // Get all unique hotel names from analysis data
      const allHotels = new Set();
      Object.values(this.analysis_data).forEach(dateData => {
        if (dateData.hotel && Array.isArray(dateData.hotel)) {
          dateData.hotel.forEach(hotel => {
            allHotels.add(hotel.hotel_name);
          });
        }
      });

      // Initialize series for all hotels
      this.series = Array.from(allHotels).map(hotelName => ({
        name: hotelName,
        data: []
      }));

      this.chartOptions.xaxis.categories = [];
      
      // Process each date in analysis_data
      Object.keys(this.analysis_data).forEach(date => {
        const hotel_date = moment_jalali(date).format("jYYYY/jMM/jDD");
        this.chartOptions.xaxis.categories.push(hotel_date);
        
        try {
          const dateData = this.analysis_data[date];
          if (dateData && dateData.hotel && Array.isArray(dateData.hotel)) {
            // Process each hotel's data
            allHotels.forEach(hotelName => {
              const hotelData = dateData.hotel.find(h => h.hotel_name === hotelName);
              const seriesIndex = this.series.findIndex(s => s.name === hotelName);
              
              if (hotelData && hotelData.rooms && hotelData.rooms.length > 0) {
                let cheapestRoom = hotelData.rooms.reduce((prev, curr) => (prev.price < curr.price ? prev : curr));
                this.series[seriesIndex].data.push({
                  price: cheapestRoom.price,
                  hotel_name: hotelData.hotel_name,
                  room_name: cheapestRoom.name,
                  provider: cheapestRoom.provider,
                  y: cheapestRoom.price,
                  x: hotel_date
                });
              } else {
                this.series[seriesIndex].data.push({
                  price: 0,
                  hotel_name: hotelName,
                  room_name: '',
                  provider: '',
                  y: 0,
                  x: hotel_date
                });
              }
            });
          } else {
            console.log("Invalid date data structure:", dateData);
            // Add empty data points for all hotels
            allHotels.forEach(hotelName => {
              const seriesIndex = this.series.findIndex(s => s.name === hotelName);
              this.series[seriesIndex].data.push({
                price: 0,
                hotel_name: hotelName,
                room_name: '',
                provider: '',
                y: 0,
                x: hotel_date
              });
            });
          }
        } catch (error) {
          console.error("Error processing hotel data:", error);
          // Add empty data points for all hotels
          allHotels.forEach(hotelName => {
            const seriesIndex = this.series.findIndex(s => s.name === hotelName);
            this.series[seriesIndex].data.push({
              price: 0,
              hotel_name: hotelName,
              room_name: '',
              provider: '',
              y: 0,
              x: hotel_date
            });
          });
        }
      });

      // Sort data points by date
      this.series.forEach(series => {
        series.data.sort((a, b) => moment_jalali(a.x, "jYYYY/jMM/jDD").valueOf() - moment_jalali(b.x, "jYYYY/jMM/jDD").valueOf());
      });
      this.chartOptions.xaxis.categories.sort((a, b) => moment_jalali(a, "jYYYY/jMM/jDD").valueOf() - moment_jalali(b, "jYYYY/jMM/jDD").valueOf());

      // Update chart colors for multiple series
      this.chartOptions.colors = ['#006600', '#FF0000', '#0000FF', '#FFA500', '#800080'];

      console.log("Final series data:", this.series);

      // Force chart update
      this.$nextTick(() => {
        if (this.$refs.chart) {
          this.$refs.chart.updateOptions({
            xaxis: {
              categories: this.chartOptions.xaxis.categories
            }
          });
          this.$refs.chart.updateSeries(this.series);
        }
      });
    }
  },
  watch: {
    analysis_data: {
      handler(newData) {
        console.log("Watch - Analysis Data in BuildComponent:", newData);
        if (this.show_analysis && newData && Object.keys(newData).length > 0) {
          console.log("Watch triggered - Updating chart");
          this.$nextTick(() => {
            this.setAnalysis();
            this.callFuntion('all');
          });
        }
      },
      deep: true,
      immediate: true
    }
  },
  created() {
    this.sorted_rooms = this.hotel.rooms;
    this.sorted_rooms = this.sorted_rooms.sort((a, b) => a.price - b.price);
  },
}
</script>

<style>
.rotate-right {
  transform: rotate(90deg);
}

.room-active {
  background: #c0e3ca !important;
}

.rotate-left {
  transform: rotate(-90deg);
}

.build-tour-component {
  transition: all .25s;
  transform: scale(1);
}

.build-tour-component:hover {
  background: rgb(240, 240, 240) !important;
  border-color: #c9c9c9 !important;
  border-width: 3px;
  box-shadow: 0 0 10px rgba(0, 0, 0, .15) !important;
  transform: scale(100.8%);
}

.button-group {
  margin-bottom: 1rem;
}

.button-group .btn {
  min-width: 120px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.button-group .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.button-group .btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
</style>