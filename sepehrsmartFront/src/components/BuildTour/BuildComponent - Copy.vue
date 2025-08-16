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
          <button class="btn btn-primary" :disabled="analysis_loading" v-on:click="showAnalysis">
            <i class="fa fa-spinner fa-spin ms-1" v-if="analysis_loading"></i>
            <span v-if="show_analysis">بستن آنالیز</span>
            <span v-else>نمایش آنالیز</span>
          </button>



          
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

    <div class="p-3" v-if="show_analysis">

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


      <apexchart type="bar" height="550" :options="chartOptions" :series="series"></apexchart>
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
      room_index: 0,
      sorted_rooms: [],
      show_analysis: false,
      series: [],
      chartOptions: {
        chart: {
          height: 550,
          type: 'area',
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
          type: 'date',
          categories: []
        },
        tooltip: {
          custom: this.customTooltip
        }
      }
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
    
    callFuntion(roomType){


      console.log(this.analysis_data)
      //
      let filtered_data = {};
      for (let hotel of Object.keys(this.analysis_data)) {
        filtered_data[hotel] = this.analysis_data[hotel]['hotel'].filter(h => h.hotel_name === this.hotel.hotel_name);
      }
      //
      // console.log(filtered_data)
      this.series = [{
        name: "نام هتل",
        data: []
      }];
      this.chartOptions.xaxis.categories = [];
      for (let hotel of Object.keys(filtered_data)) {
        let hotel_date = moment_jalali(hotel).format("jYYYY/jMM/jDD");
        this.chartOptions.xaxis.categories.push(hotel_date);
        

        // console.log(roomType)
        // check best room
        try {
          let matchingRooms = [];
          for (let room of filtered_data[hotel][0].rooms){
            if (
              (roomType=='1' && room.capacity==1) || 
              (roomType=='2' && room.capacity==2) ||
              (roomType=='3' && room.capacity==3) ||
              (roomType=='4' && room.capacity==4) ||
              roomType=='all'
              )

              matchingRooms.push(room);
            

          }
        // console.log(matchingRooms)
        // Find room with minimum price
        if (matchingRooms.length > 0) {
          let minRoom = matchingRooms.reduce((prev, curr) => (prev.price < curr.price ? prev : curr));
          // console.log(minRoom)
          
        
        // Push the room with minimum price into series
        this.series[0].data.push({
          price: minRoom.price, // Minimum price
          hotel_name: filtered_data[hotel][0]['hotel_name'], // Hotel name
          room_name: minRoom.name, // Room name of the minimum price
          provider: minRoom.provider, // Provider of the room with minimum price
          y: minRoom.price, // Value for the chart
          x: hotel_date, // Date
        });
      }
      } catch (error) {
        console.error("Error processing rooms:", error);
        this.series[0].data.push({
          price: 0,
          hotel_name: '',
          room_name: '',
          provider: '',
          y: 0,
          x: hotel_date,
        });
      }
    }

        //   // old 
        //   if (
        //     (roomType=='1' && ((filtered_data[hotel][0].room_name.includes('یک تخت') ||filtered_data[hotel][0].room_name.includes('یکتخت') || filtered_data[hotel][0].room_name.includes('یک نفر') || filtered_data[hotel][0].room_name.includes('یکنفر') ))) ||
        //     (roomType=='2' && ((filtered_data[hotel][0].room_name.includes('دو تخت') ||filtered_data[hotel][0].room_name.includes('دوتخت') || filtered_data[hotel][0].room_name.includes('دو نفر') || filtered_data[hotel][0].room_name.includes('دونفر') ))) ||
        //     (roomType=='3' && ((filtered_data[hotel][0].room_name.includes('سه تخت') ||filtered_data[hotel][0].room_name.includes('سهتخت') || filtered_data[hotel][0].room_name.includes('سه نفر') || filtered_data[hotel][0].room_name.includes('سهنفر') )))||
        //     (roomType=='4' && ((filtered_data[hotel][0].room_name.includes('چهار تخت') ||filtered_data[hotel][0].room_name.includes('چهارتخت') || filtered_data[hotel][0].room_name.includes('چهار نفر') || filtered_data[hotel][0].room_name.includes('چهارنفر') )))||
        //     roomType=='all')

        //   {
        //   this.series[0].data.push({
        //     price: filtered_data[hotel][0].price,
        //     hotel_name: filtered_data[hotel][0]['hotel_name'],
        //     room_name: filtered_data[hotel][0]['room_name'],
        //     provider: filtered_data[hotel][0]['provider'],
        //     y: filtered_data[hotel][0].price,
        //     x: hotel_date
        //   });
        // }
        // } catch {
        //   this.series[0].data.push({
        //     price: 0,
        //     hotel_name: '',
        //     room_name: '',
        //     provider: '',
        //     y: 0,
        //     x: hotel_date
        //   })
        // }
        
      // }
    // Update the chart after modifying the series
    this.chart.updateSeries(this.series);
    this.dataKey++;

      console.log("Option 1 create")
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
      
      this.dataKey++;

      this.setAnalysis();
    },
    showRooms() {
      this.show_rooms = !this.show_rooms;
      this.show_analysis = false;
    },
    roomPrice(price,capacity) {
      
      const result = (price / capacity) + this.go_flight.providers[this.go_flight_provider].price + this.return_flight.providers[this.return_flight_provider].price;
      // console.log(result * this.adults)
      return Number(Math.round(result * this.adults)).toLocaleString();

      // // old code
      // const result = (price / this.adults) + this.go_flight.providers[this.go_flight_provider].price + this.return_flight.providers[this.return_flight_provider].price;
      // // console.log(result * this.adults)
      // return Number(Math.round(result * this.adults)).toLocaleString();
    },
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
      //

      console.log(this.analysis_data)


      let filtered_data = {};
      for (let hotel of Object.keys(this.analysis_data)) {
        filtered_data[hotel] = this.analysis_data[hotel].filter(h => h.hotel_name === this.hotel.hotel_name);
      }
      //
      this.series = [{
        name: "نام هتل",
        data: []
      }];
      this.chartOptions.xaxis.categories = [];
      for (let hotel of Object.keys(filtered_data)) {
        let hotel_date = moment_jalali(hotel).format("jYYYY/jMM/jDD");
        this.chartOptions.xaxis.categories.push(hotel_date);
        try {
          this.series[0].data.push({
            price: filtered_data[hotel][0].price,
            hotel_name: filtered_data[hotel][0]['hotel_name'],
            room_name: filtered_data[hotel][0]['room_name'],
            provider: filtered_data[hotel][0]['provider'],
            y: filtered_data[hotel][0].price,
            x: hotel_date
          })
        } catch {
          this.series[0].data.push({
            price: 0,
            hotel_name: '',
            room_name: '',
            provider: '',
            y: 0,
            x: hotel_date
          })
        }
      }
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
</style>