<template>
  <section>
    <!-- MAIN ITEM -->
    <div :class="{'border rounded p-3 shadow-xs mt-3 tour-single-items': true, 'sticky-item': show}">
      <div class="row align-items-center">
        <!-- HOTEL NAME -->
        <div class="col-12 col-md-4">
          <h5>{{ hotel_name }} ({{ hotel_star }} &starf;)</h5>
          <h5 class="mt-2">{{ providers[0].room_name }}</h5>
        </div>
        <!-- GO FLIGHT -->
        <div class="col-6 col-md-2 mt-3 mt-md-0">
          <h5>{{ providers[0].go_flight_airline }}</h5>
          <h5 class="mt-2">{{ providers[0].go_flight_arrive_time }}</h5>
          <h5 class="mt-2">{{ start_date }}</h5>
        </div>
        <!-- RETURN FLIGHT -->
        <div class="col-6 col-md-2 mt-3 mt-md-0">
          <h5>{{ providers[0].return_flight_airline }}</h5>
          <h5 class="mt-2">{{ providers[0].return_flight_arrive_time }}</h5>
          <h5 class="mt-2">{{ end_date }}</h5>
        </div>
        <!-- PRICE -->
        <div class="col-12 col-md-4 mt-3 mt-md-0">
          <div class="d-flex algin-items-center justify-content-between">
            <h5>قیمت هر نفر:</h5>
            <h5 class="text-center">{{ pricePerPerson(total_price) }} تومان</h5>
          </div>
          <hr>
          <div class="d-flex algin-items-center justify-content-between">
            <h5>قیمت کل:</h5>
            <h5 class="text-center">{{ priceFilter(total_price) }} تومان</h5>
          </div>
        </div>
        <!-- MORE -->
        <div class="col-12 mt-3 ">
          <div class="row align-items-center">
            <div class="col-12 col-md-3 d-flex justify-content-between align-items-center">
              <h5 class="">{{ providers[0].provider_name }}</h5>
              <p :class="{'text-danger': providers[0].status !== 'تایید شده', 'm-0': true}">{{ providers[0].status }}</p>
            </div>
            <div class="col-12 col-md-3 mt-3 mt-md-0">
              <button :disabled="loading_analysis" class="btn btn-info w-100" v-on:click="showAnalysis('click')">
                <span v-if="!show_analysis">
                  <i class="fa fa-spinner fa-spin" v-if="loading_analysis"></i>
                  نمایش آنالیز
                </span>
                <span v-else>بستن آنالیز</span>
              </button>
            </div>
            <div class="col-12 col-md-3 mt-3 mt-md-0">
              <button class="btn btn-primary w-100" v-on:click="showProviders">
                <span v-if="show">بستن</span>
                <span v-else>سایر ({{ providers.length }})</span>
              </button>
            </div>
            <div class="col-12 col-md-3 mt-3 mt-md-0">
              <a target="_blank" :href="providers[0].redirect_link" class="btn btn-success w-100">نمایش در سایت</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- COlLAPSE CHART -->
    <div :class="{'collapse': true, 'show': show_analysis}" :id="`analysis_${unique_id}`">
      <apexchart class="px-3 mt-4" type="bar" height="550" :options="options"
                 :series="series" v-if="show_analysis"></apexchart>
    </div>
    <!-- COlLAPSE PROVIDER -->
    <div :class="{'collapse': true, 'show': show}" :id="unique_id">
      <div class="row">
        <div class="col-12 col-md-4 mt-4" v-for="(provider, index) in providers" :key="index">
          <div class="border p-3 rounded">
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ provider.room_name }}</h5>
              <h5>{{ provider.provider_name }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ provider.go_flight_airline }}</h5>
              <h5 class="mt-2">{{ provider.go_flight_arrive_time }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ provider.return_flight_airline }}</h5>
              <h5 class="mt-2">{{ provider.return_flight_arrive_time }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>هر نفر :</h5>
              <h5>
                <span>{{ pricePerPerson(provider.price) }}</span>
                <span> تومان </span>
              </h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>قیمت کل :</h5>
              <h5>
                <span>{{ priceFilter(provider.price) }}</span>
                <span> تومان </span>
              </h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>کمیسیون :</h5>
              <h5>{{ priceFilter(provider.commission) }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>وضعیت :</h5>
              <h5 :class="{'text-danger': provider.status !== 'تایید شده'}">{{ provider.status }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <a target="_blank" :href="provider.redirect_link" class="btn btn-success w-100">نمایش در سایت</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import moment_jalali from "moment-jalaali";

export default {
  name: "TourComponent",
  props: {
    hotel_name: String,
    total_price: Number,
    providers: Array,
    index: Number,
    hotel_star: Number,
    start_date: String,
    end_date: String,
    redirect_link: String,
    analysis_data: Object,
    loading_analysis: Boolean,
    adults: Number
  },

  // created() {
  //   this.$parent.$on('analysis-size-changed', this.showAnalysis);
  // },

  data() {
    return {
      previousSize: 0,  // To track the previous size of the data
      show: false,
      unique_id: `collapse_${Math.floor(Math.random() * 999999999)}_${this.index}`,
      show_analysis: false,
      options: {
        bar: {
          borderRadius: "5px",
        },
        chart: {
          id: 'chart',
          toolbar: {
            show: false,
            autoSelected: 'selection'
          }
        },
        colors: ['#006600'],
        xaxis: {
          categories: [1, 2, 3, 4, 5]
        },
        yaxis: {
          show: false,
        },
        tooltip: {
          custom: this.customTooltip
        }
      },
      series: [{
        name: 'قیمت',
        data: []
      }]
    }
  },

  mounted() {
    // Set interval to check the size of analysis_data every 1000ms (1 second)
    this.checkDataSizeInterval = setInterval(() => {
      const currentSize = Object.keys(this.analysis_data).length;
      // console.log(this.analysis_data)
      // Check if the size has changed
      if (currentSize !== this.previousSize) {
        this.previousSize = currentSize;
        this.showAnalysis('NoClick');  // Call showAnalysis if the size changes
      }
    }, 1000);  // Check every second
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    if (this.checkDataSizeInterval) {
      clearInterval(this.checkDataSizeInterval);
    }
  },

  methods: {
    priceFilter(price) {
      return Number(price).toLocaleString();
    },
    pricePerPerson(price) {
      return Number(Math.round(price / parseInt(this.adults))).toLocaleString();
    },
    showProviders() {
      this.show_analysis = false;
      this.show = !this.show;
    },
    showAnalysis(parameter) {
      this.options.xaxis.categories = [];
      this.series[0].data = [];
      const keys = Object.keys(this.analysis_data);
      //  = keys;

      // console.log(this.analysis_data)
      for (let date of keys) {
        const persian_date = moment_jalali(date).format("jYYYY/jMM/jDD");
        console.log(date +' -----> '+ persian_date)
        this.options.xaxis.categories.push(persian_date);
        let price = 0;
        let provider_name = "";
        let room_name = "";
        for (let hotel of this.analysis_data[date]) {
          if (hotel.hotel_name === this.hotel_name) {
            price = (hotel.providers[0].price / parseInt(this.adults));
            provider_name = hotel.providers[0].provider_name;
            room_name = hotel.providers[0].room_name;
            break;
          }
        }

        // // change color for min price
        // let minPrice = Infinity;
        // let minPriceIndex = -1;

        // // First, determine the minimum price
        // keys.forEach((date) => {
        //   for (let hotel of this.analysis_data[date]) {
        //     if (hotel.hotel_name === this.hotel_name) {
        //       const price = hotel.providers[0].price / parseInt(this.adults);
        //       if (price < minPrice) {
        //         minPrice = price;
        //         minPriceIndex = this.series[0].data.length; // Index in the final series data
        //       }
        //     }
        //   }
        // });


        //------------------------------------

        this.series[0].data.push({
          x: date,
          y: price,
          provider_name: provider_name,
          room_name: room_name,
          // fillColor: this.series[0].data.length === minPriceIndex ? '#0000FF' : '#FF0000' // Blue for min price, red otherwise

        });
      }
      if (parameter=='click'){
        this.show_analysis = !this.show_analysis;
        this.show = false;
      }

    },
    customTooltip({dataPointIndex}) {
      return '<div class="arrow_box p-3">' +
          '<p class="text-truncate">' + this.series[0].data[dataPointIndex].room_name + '</p>' +
          '<p class="text-truncate">' + this.series[0].data[dataPointIndex].provider_name + '</p>' +
          '<p class="text-truncate"> هر نفر (نت) : ' + this.priceFilter(this.series[0].data[dataPointIndex].y) + '</p>' +
          '</div>'
    },


  },

}
</script>

<style scoped>
.sticky-item {
  position: sticky;
  top: 5px;
  background: var(--background);
  z-index: 5;
}

.tour-single-items, .tour-single-items button {
  transition: all .35s;
}

.tour-single-items:hover {
  /*background: rgb(235, 235, 235) !important;*/
  /*transform: scale(1.01);*/
  background: #fafafa !important;
  box-shadow: rgb(204, 219, 232) 3px 3px 6px 0 inset, rgba(255, 255, 255, 0.5) -3px -3px 6px 1px inset;
}

.tour-single-items:hover button {
  box-shadow: rgba(50, 50, 93, 0.25) 0 2px 5px -1px, rgba(0, 0, 0, 0.3) 0 1px 3px -1px;
}

@media (max-width: 766px) {
  .sticky-item {
    position: relative !important;
  }
}
</style>