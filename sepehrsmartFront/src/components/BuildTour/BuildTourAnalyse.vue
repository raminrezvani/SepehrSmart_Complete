<template>
  <div class="p-3 chart-main show">
    <!-- --- TITLE --- -->
    <div class="row justify-content-between pb-2 border-bottom">
      <div class="col-12 col-md-9 mt-3 mt-md-0 order-1 order-md-0">
        <label for="filter_name_hotel_analysis_build_tour" class="text-muted mb-1">ستاره هتل</label>
        <select v-model="filter.star" class="form-select" id="filter_name_hotel_analysis_build_tour"
                v-on:change="filterAnalyse">
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
    <apexchart type="bar" height="600" :options="chartOptions" :series="series" v-if="show_chart"></apexchart>
  </div>
</template>

<script>
import moment_jalali from "moment-jalaali";

export default {
  name: "BuildTourAnalyse",
  props: {
    data: Object,
    adults: Number
  },
  data() {
    return {
      filter: {
        star: "all"
      },
      series: [],
      chartOptions: {
        chart: {
          height: 350,
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
      },
      show_chart: false,
      filtered_data: this.data,
    }
  },
  methods: {
    closeAnalysis() {
      return this.$emit("closeAnalysis", false);
    },
    customTooltip({seriesIndex, dataPointIndex}) {
      return '<div class="arrow_box p-3">' +
          '<p class="text-truncate">' + this.series[seriesIndex].data[dataPointIndex].hotel_name + '</p>' +
          '<p class="text-truncate">' + this.series[seriesIndex].data[dataPointIndex].room_name + '</p>' +
          '<p class="text-truncate">' + this.series[seriesIndex].data[dataPointIndex].provider + '</p>' +
          '<p class="text-truncate">هر نفر (نت) : ' + this.priceFilter(this.series[seriesIndex].data[dataPointIndex].price / this.adults) + '</p>' +
          '<p class="text-truncate">کل (نت) : ' + this.priceFilter(this.series[seriesIndex].data[dataPointIndex].price) + '</p>' +
          '</div>'
    },
    priceFilter(data) {
      return Number(data).toLocaleString();
    },
    setAnalyseData() {
      this.show_chart = false;
      this.series = [{
        name: "نام هتل",
        data: []
      }];
      this.chartOptions.xaxis.categories = [];
      for (let hotel of Object.keys(this.filtered_data)) {
        let hotel_date = moment_jalali(hotel).format("jYYYY/jMM/jDD");
        this.chartOptions.xaxis.categories.push(hotel_date);
        try {
          this.series[0].data.push({
            price: this.filtered_data[hotel][0].price,
            hotel_name: this.filtered_data[hotel][0]['hotel_name'],
            room_name: this.filtered_data[hotel][0]['room_name'],
            provider: this.filtered_data[hotel][0]['provider'],
            y: this.filtered_data[hotel][0].price,
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

      console.log(this.filtered_data)
      console.log(this.series[0].data)

      this.show_chart = true;
    },
    filterAnalyse() {
      if (this.filter.star === "all") {
        this.filtered_data = this.data;
      } else {
        let result = {};
        for (let hotel of Object.keys(this.data)) {
          result[hotel] = this.data[hotel].filter(h => parseInt(h.hotel_star) === parseInt(this.filter.star));
        }
        this.filtered_data = result;
      }
      this.setAnalyseData();
    }
  },
  created() {
    this.setAnalyseData();
  }
}
</script>

<style scoped>

</style>