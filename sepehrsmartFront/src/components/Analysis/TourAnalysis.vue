<template>
  <div id="chart" class="p-3 chart-main show">
    <!-- --- TITLE --- -->
    <div class="row justify-content-between pb-2 border-bottom">
      <div class="col-12 col-md-9 mt-3 mt-md-0 d-flex justify-content-between order-1 order-md-0">
        <label for="analysis_filter_star" class="text-muted mb-1 text-nowrap">ستاره هتل</label>
        <select v-model="filter_data.hotel_star" class="form-select" id="analysis_filter_star" @change="sortedData">
          <option value="all">همه</option>
          <option value="1">۱ ستاره</option>
          <option value="2">۲ ستاره</option>
          <option value="3">۳ ستاره</option>
          <option value="4">۴ ستاره</option>
          <option value="5">۵ ستاره</option>
        </select>
      </div>
      <div class="col-12 col-md-3 d-flex justify-content-end order-0 order-md-1">
        <button class="btn btn-danger w-close" v-on:click="closeAnalysis">بستن</button>
      </div>
    </div>
    <!-- --- CHART --- -->
    <apexchart class="px-3 mt-5" type="bar" height="600" :options="options"
               :series="series"></apexchart>
    <!--      <div class="alert alert-warning mt-4" v-else>-->
    <!--        <p class="m-0 text-center">توری یافت نشد</p>-->
    <!--      </div>-->
  </div>
</template>

<script>
import moment_jalali from "moment-jalaali";

export default {
  name: "TourAnalysis",
  props: {
    show: Boolean,
    start_date: String,
    night_count: Number,
    loading: Boolean,
    data: Object,
    adults: Number
  },
  data() {
    return {
      range_number: 7,
      main_loading: this.loading,
      fixed_data: this.data,
      filter_data: {
        hotel_star: "all"
      },
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
          categories: []
        },
        yaxis: {
          show: false,
        },
        tooltip: {
          custom: this.customTooltip
        }
      },
      series: [{
        name: 'تور',
        data: []
      }]
    }
  },
  emits: ['changeAnalysisStatus'],
  methods: {
    setData(data) {
      let categories = [];
      let chart_data = [];
      for (let tour in this.fixed_data) {
        //  ----------
        const x_date = moment_jalali(tour).format("jYYYY/jMM/jDD");
        categories.push(x_date);
        //  ----------
        let hotels = JSON.parse(JSON.stringify(data[tour]));
        console.log(tour, hotels);
        hotels = hotels.sort((a, b) => (parseFloat(a.providers[0].price)) - (parseFloat(b.providers[0].price)));
        let appended_data;
        try {
          appended_data = {
            x: x_date,
            y: (hotels[0].providers[0].price),
            per_person: (hotels[0].providers[0].price / parseInt(this.adults)),
            hotel_name: hotels[0].hotel_name,
            provider_name: hotels[0].providers[0].provider_name,
            room_name: hotels[0].providers[0].room_name
          }
        } catch {
          appended_data = {
            x: x_date,
            y: 0,
            per_person: 0,
            hotel_name: '',
            provider_name: '',
            room_name: ''
          }
        }
        chart_data.push(appended_data);
      }
      this.options.xaxis.categories = categories;
      this.series[0].data = chart_data;
    },
    priceFilter(price) {
      return Number(price).toLocaleString();
    },
    customTooltip({dataPointIndex}) {
      return '<div class="arrow_box p-3">' +
          '<p class="text-truncate">' + this.series[0].data[dataPointIndex].hotel_name + '</p>' +
          '<p class="text-truncate">' + this.series[0].data[dataPointIndex].room_name + '</p>' +
          '<p class="text-truncate">' + this.series[0].data[dataPointIndex].provider_name + '</p>' +
          '<p class="text-truncate">هر نفر : ' + this.priceFilter(this.series[0].data[dataPointIndex].per_person) + '</p>' +
          '<p class="text-truncate">کل : ' + this.priceFilter(this.series[0].data[dataPointIndex].y) + '</p>' +
          '</div>'
    },
    closeAnalysis() {
      this.$emit('changeAnalysisStatus', false);
    },
    sortedData() {
      console.log(this.filter_data);
      // --------- filter star
      if (this.filter_data.hotel_star === "all") {
        this.setData(this.fixed_data);
      } else {
        let data = this.fixed_data;
        let result = {};
        for (let tour in data) {
          result[tour] = this.fixed_data[tour].filter(hotel => hotel.hotel_star === parseInt(this.filter_data.hotel_star));
        }
        this.setData(result);
      }
    }
  },
  created() {
    this.setData(this.data);
  }
}
</script>

<style>
.chart-main {
  overflow: hidden;
  position: fixed;
  width: 96%;
  height: 96%;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, .1);
  background: #fafafa;
  border-radius: 10px;
  transition: all .4s;
  transform: translateY(-120%);
  z-index: 10;
}

.chart-main.show {
  transform: translateY(0%);
}

.w-close {
  width: auto;
}

@media (max-width: 766px) {
  .w-close {
    width: 100%;
  }
}

</style>
